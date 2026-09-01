from openai import OpenAI, APIConnectionError
import json
import time


client = OpenAI()


def get_llm_features_batch(texts):

    numbered_posts = ""

    for i, text in enumerate(texts):
        numbered_posts += f"\nPOST {i}\n{text}\n"

    prompt = f"""
You are extracting structured features from Reddit posts about Tesla.

Score each post independently.

Definitions:

investor_relevance:
Integer from 0 to 10.
How relevant the information is to Tesla investors, valuation, earnings,
profitability, growth, risk or future business performance.

importance:
Integer from 0 to 10.
How significant the information appears for Tesla as a company.

novelty:
Integer from 0 to 10.
How new or unusual the information appears based only on the post.
If there is no evidence that the information is new, score low.

expected_outcome:
Integer from -2 to 2.

-2 = strongly negative expected business or financial outcome
-1 = somewhat negative expected outcome
 0 = neutral, mixed, or no clear expected outcome
 1 = somewhat positive expected outcome
 2 = strongly positive expected outcome

expected_surprise:
Integer from 0 to 10.
How surprising the information appears relative to expectations expressed
in the post.
If expectations or surprise are not mentioned, score low.

Rules:
- Score every post separately.
- Only use information contained in that post.
- Do not use knowledge of what happened afterwards.
- Do not infer Tesla's later stock return.
- If information is insufficient, score conservatively.
- The post_index must match the POST number provided.

POSTS:
{numbered_posts}
"""

    for attempt in range(3):

        try:

            response = client.responses.create(
                model="gpt-5-nano",
                input=prompt,

                text={
                    "format": {
                        "type": "json_schema",
                        "name": "reddit_llm_features_batch",
                        "strict": True,

                        "schema": {
                            "type": "object",

                            "properties": {

                                "results": {
                                    "type": "array",

                                    "items": {
                                        "type": "object",

                                        "properties": {

                                            "post_index": {
                                                "type": "integer"
                                            },

                                            "investor_relevance": {
                                                "type": "integer",
                                                "minimum": 0,
                                                "maximum": 10
                                            },

                                            "importance": {
                                                "type": "integer",
                                                "minimum": 0,
                                                "maximum": 10
                                            },

                                            "novelty": {
                                                "type": "integer",
                                                "minimum": 0,
                                                "maximum": 10
                                            },

                                            "expected_outcome": {
                                                "type": "integer",
                                                "minimum": -2,
                                                "maximum": 2
                                            },

                                            "expected_surprise": {
                                                "type": "integer",
                                                "minimum": 0,
                                                "maximum": 10
                                            }
                                        },

                                        "required": [
                                            "post_index",
                                            "investor_relevance",
                                            "importance",
                                            "novelty",
                                            "expected_outcome",
                                            "expected_surprise"
                                        ],

                                        "additionalProperties": False
                                    }
                                }
                            },

                            "required": [
                                "results"
                            ],

                            "additionalProperties": False
                        }
                    }
                }
            )

            return json.loads(
                response.output_text
            )["results"]

        except APIConnectionError:

            print(
                f"Connection failed. "
                f"Retrying {attempt + 1}/3..."
            )

            time.sleep(5)

    raise Exception(
        "OpenAI API connection failed after 3 attempts"
    )

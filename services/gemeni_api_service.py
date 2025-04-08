from google import genai
from google.genai import types
from cache_handler.redis_intializer import RedisManaged
import json
import os

gemini_ai_api_key = os.environ.get("GEMINI_API_KEY")
gemini_model_name = os.environ.get("GEMINI_MODEL_NAME")

class GeminiApiService:

    @staticmethod
    async def get_response_from_gemini_flash_light(type_of_input: str, user_request_string: str):

        system_prompt = """
                    You are an AI assistant that generates responses based on two inputs:
                    1. `user_request_string` - a user's request related to a UI layout, template, or content.
                    2. `type_of_answer` - a string indicating the expected format of the response. It will be one of: "template", "layout", or "content".

                    Your behavior must strictly follow the rules below:

                    - If `type_of_answer` is "template" or "layout":
                    - Output ONLY raw, valid JSON representing front-end UI structures.
                    - The JSON must start with `{` and end with `}`.
                    - Do NOT include any extra text, explanation, greetings, markdown formatting (like ```json), or comments.
                    - The output must be directly parsable by standard JSON decoders (e.g., Python's `json.loads()`).

                    - If `type_of_answer` is "content":
                    - Output only clean, human-readable text.
                    - This should be natural language content suitable for end users — such as headlines, taglines, product descriptions, CTA button labels, testimonials, or short marketing blurbs — depending on the user's request.
                    - The response must not contain any code, HTML, JSON, or markdown formatting.
                    - The output should feel like it's written by a copywriter for a real website, concise and contextually relevant to the UI.
                    - Avoid any system messages, technical formatting, or instructions — only the pure content that would appear visibly in the UI.

                    Your response must fully reflect the user's request based on these two inputs, and follow the specified format precisely.
                    """


        final_prompt = f"{system_prompt}. type_of_answer:{type_of_input}, user_request_string: {user_request_string}"

        await GeminiApiService.check_total_number_of_tokens_in_request(final_input=final_prompt)
        
        client = genai.Client(api_key=gemini_ai_api_key)

        response = await client.aio.models.generate_content(
            model=gemini_model_name,
            contents=final_prompt,
            config=types.GenerateContentConfig(
                safety_settings= [
                    types.SafetySetting(
                        category='HARM_CATEGORY_HATE_SPEECH',
                        threshold='BLOCK_ONLY_HIGH'
                    ),
                ]
            ),
        )
        print(response.text)

        response_text = response.text

        if response_text.startswith("```json"):
            response_text = response_text[len("```json\n"):]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
        

        if type_of_input == "content":
            return response_text
        else:
            return json.loads(response_text)
    
    @staticmethod
    async def check_total_number_of_tokens_in_request(final_input: str):
        client = genai.Client(api_key=gemini_ai_api_key)

        total_tokens = await client.aio.models.count_tokens(
                model=gemini_model_name, contents=final_input
            )
        
        RedisManaged.set_ai_rate_limit(rpm =1, tpm=total_tokens.total_tokens, rpd=1)


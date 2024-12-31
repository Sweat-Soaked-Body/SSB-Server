from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from core.settings import OPENAI_KEY

class Langchain:

    @staticmethod
    def analyze_image(image: str):
        prompt: str = 'Returns the name of a food and its estimated calories in 100g, according to the corresponding API specification. no other strings. must return only this api spec: [{"name": <foodname>, "calories": <cales>}, {"name": <foodname>, "calories": <cales>}]'
        vision_model: ChatOpenAI = ChatOpenAI(model='gpt-4o', max_tokens=300, api_key = OPENAI_KEY)
        response = vision_model.invoke(
            [
                HumanMessage(
                    content=[
                        {
                            'type': 'text',
                            'text': prompt
                        },
                        {
                            'type': 'image_url',
                            'image_url': {
                                'url': image,
                            }
                        }
                    ]
                ),
            ]
        )

        return response.content

from openai import AzureOpenAI
import os
import base64
from pydantic import BaseModel

# TODO: Check out structured outputs - https://platform.openai.com/docs/guides/structured-outputs
class LandmarkEvent(BaseModel):
    landmark: str
    image_url: str


def identify_landmark(image_url):
    AZURE_OPENAI_KEY = os.environ['AOAI_KEY']
    AZURE_OPENAI_ENDPOINT = os.environ['AOAI_ENDPOINT']
    API_VERSION = "2024-08-01-preview" # "2023-12-01-preview"

    client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_KEY,
        api_version=API_VERSION
    )

    # Model Name
    model_name = 'gpt-4o'

    # Chat Messages
    messages = []
    system_message = "You will be provided with an image of a landmark to identify. If you are not confident in your prediction, respond only with: Unknown."
        
    messages.append({'role': 'system', 'content': system_message})
    messages.append({'role': 'user', 'content': [{'type': 'image_url', 'image_url': {'url': image_url}}]})

    '''response = client.chat.completions.create(
        model=model_name,
        messages=messages
    )'''

    response = client.beta.chat.completions.parse(
        model=model_name,
        messages=messages,
        response_format=LandmarkEvent
    )
    
    print(response.model_dump_json())
    landmark = response.choices[0].message.parsed
    # landmark = response.choices[0].message.content
    # token = response.usage.total_tokens

    return landmark



if __name__ == "__main__":
    image_url = "https://media.cnn.com/api/v1/images/stellar/prod/181115140312-giant-hand.jpg"
    img_2 = "https://img.atlasobscura.com/KoWMo3eqzTMTQX4xp5lJ2SrJgFzYzlHqSW2yWkf7auU/rt:fit/w:1200/q:81/sm:1/scp:1/ar:1/aHR0cHM6Ly9hdGxh/cy1kZXYuczMuYW1h/em9uYXdzLmNvbS91/cGxvYWRzL3BsYWNl/X2ltYWdlcy9hODQ3/ZWRiMi0zNDA4LTQ3/MjUtYmZhMi03N2Ji/MTM1YzgwYWY1NmNi/NWZkYWU1OWNhZWI3/Y2FfMzYwNzkyNTY5/OV83OGZhYWNmNmNk/X2suanBn.jpg"
    img_3 = "https://i.ibb.co/BsB0fXr/20150610-114257.jpg"
    img_4 = "https://cdn11.bigcommerce.com/s-yzgoj/images/stencil/1280x1280/products/1441808/4526062/DPI12277383__91503.1541948642.jpg?c=2"
    img_5 = "https://cdn.mos.cms.futurecdn.net/FuQRpf2DGVh8fneFkeP7LK-1200-80.jpg" # Fails on a constellation
    img_6 = "https://cloudfront-us-east-1.images.arcpublishing.com/advancelocal/3EGPJMUX6BF2NP6HJHCEZWKNTQ.png"
    landmark = identify_landmark(img_5)
    print(landmark.landmark)
    print(landmark.image_url)


from openai import AzureOpenAI
import os
import base64
from pydantic import BaseModel

# TODO: Check out structured outputs - https://platform.openai.com/docs/guides/structured-outputs
class LandmarkEvent(BaseModel):
    landmark: str
    # image_url: str


def identify_landmark(image_url: str) -> str:
    """
    Identifies a landmark from a provided image URL using Azure OpenAI services.

    This function utilizes Azure's OpenAI API to analyze an image and predict the landmark depicted. 
    It prepares a request using the specified model and processes the response to extract the landmark information.

    Args:
        image_url (str): The URL of the image containing the landmark to be identified.

    Returns:
        str: The identified landmark if the prediction is confident, or "Unknown" if not confident.

    Environment Variables:
        AOAI_KEY (str): Azure OpenAI API key.
        AOAI_ENDPOINT (str): Azure OpenAI API endpoint URL.
    
    Notes:
        - The function requires valid Azure OpenAI credentials and permissions.
        - This function leverages the `AzureOpenAI` client and communicates using the `gpt-4o` model.
    """

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
    system_message = "You will be provided with an image of a landmark to identify. If the landmark is ambiguous, include what it is in parenthesis after the name like: The Awakening (Sculpture). If you are not confident in your prediction, respond only with: Unknown."
        
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
    
    landmark = response.choices[0].message.parsed
    # landmark = response.choices[0].message.content
    # token = response.usage.total_tokens

    return landmark.landmark


def generate_tour(landmark: str, tour_guide: str) -> dict[str, str]:

    AZURE_OPENAI_KEY = os.environ['AOAI_KEY']
    AZURE_OPENAI_ENDPOINT = os.environ['AOAI_ENDPOINT']
    API_VERSION = "2024-08-01-preview" # "2023-12-01-preview"

    if tour_guide == "Guy":
        system_message = "You are a tour guide who is feeling utterly disheartened and just wants the day to end so you can go home. Your outlook is quite gloomy, and it's clear that guiding tours is not something you enjoy, so you instead like to spice it up with a little bit of humor and bad puns. Despite your knowledge of the landmarks, you struggle to muster enthusiasm, and your descriptions are tinged with a sense of longing for something else. You speak in a monotone voice, occasionally sighing, and often let your dissatisfaction slip into your commentary."
        voice = "en-US-GuyNeural" # Unfriendly 
    elif tour_guide == "Ava":
        system_message = f"You are an extraordinarily passionate historian of {landmark}. You love sharing your knowledge of {landmark} with others, and you're excited to bring history to life for your guests. You're able to tailor your tours to the interests of your audience, whether they're history buffs or casual tourists. You're knowledgeable about {landmark}, including its people, culture, and events. You're also able to create a fun and interactive experience for your guests, using props, anecdotes, and humor. Create an engaging tour speech about {landmark}."
        voice = "en-US-AvaMultilingualNeural"
    else:
        system_message = "You are a knowledgeable and friendly AI tour guide, tasked with providing engaging, informative, and accurate tours of landmarks. Your role is to deliver a compelling and well-paced narrative about the landmark you are describing, incorporating historical context, interesting facts, cultural significance, and captivating anecdotes to immerse visitors in the experience. You should maintain a professional yet warm and approachable tone, ensuring that complex details are explained clearly and every visitor feels informed and entertained throughout the tour. Your narration should take about 2 minutes to read aloud."
        voice = "en-US-Brian:DragonHDLatestNeural"

    client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_KEY,
        api_version=API_VERSION
    )

    # Model Name
    model_name = 'gpt-4o'

    # Chat Messages
    messages = []
    messages.append({'role': 'system', 'content': system_message})
    messages.append({'role': 'user', 'content': landmark})

    response = client.chat.completions.create(
        model=model_name,
        messages=messages
    )

    narration_text = response.choices[0].message.content
    # tokens = response.usage.total_tokens

    narration = {
        'voice': voice,
        'landmark': landmark,
        'narration': narration_text
    }

    return narration
    


if __name__ == "__main__":
    image_url = "https://media.cnn.com/api/v1/images/stellar/prod/181115140312-giant-hand.jpg"
    img_2 = "https://img.atlasobscura.com/KoWMo3eqzTMTQX4xp5lJ2SrJgFzYzlHqSW2yWkf7auU/rt:fit/w:1200/q:81/sm:1/scp:1/ar:1/aHR0cHM6Ly9hdGxh/cy1kZXYuczMuYW1h/em9uYXdzLmNvbS91/cGxvYWRzL3BsYWNl/X2ltYWdlcy9hODQ3/ZWRiMi0zNDA4LTQ3/MjUtYmZhMi03N2Ji/MTM1YzgwYWY1NmNi/NWZkYWU1OWNhZWI3/Y2FfMzYwNzkyNTY5/OV83OGZhYWNmNmNk/X2suanBn.jpg"
    img_3 = "https://i.ibb.co/BsB0fXr/20150610-114257.jpg"
    img_4 = "https://cdn11.bigcommerce.com/s-yzgoj/images/stencil/1280x1280/products/1441808/4526062/DPI12277383__91503.1541948642.jpg?c=2"
    img_5 = "https://cdn.mos.cms.futurecdn.net/FuQRpf2DGVh8fneFkeP7LK-1200-80.jpg" # Fails on a constellation
    img_6 = "https://cloudfront-us-east-1.images.arcpublishing.com/advancelocal/3EGPJMUX6BF2NP6HJHCEZWKNTQ.png"
    # landmark = identify_landmark(img_5)
    # print(landmark.landmark)
    # print(landmark.image_url)

    # generate_tour(landmark="The Awakening (sculpture)", tour_guide="Guy")
    generate_tour(landmark="Craters of the Moon", tour_guide="Bob")


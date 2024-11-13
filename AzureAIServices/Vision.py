from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
import os
import requests



def identify_landmark(image_url):
    KEY = os.environ["AI_MULTISERVICE_KEY"]
    URL = f"https://eastus.api.cognitive.microsoft.com/vision/v3.2/models/Landmarks/analyze"

    headers = {
        "Ocp-Apim-Subscription-Key": KEY,
    }

    body = {"url": image_url}

    # May need to check the image to determine content type
    response = requests.post(
        url=URL,
        headers=headers,
        json=body
    )

    try:
        landmark = response.json()['result']['landmarks'][0]['name']
    except:
        landmark = ""

    return landmark




if __name__ == "__main__":
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Tour_Eiffel_Wikimedia_Commons_%28cropped%29.jpg/375px-Tour_Eiffel_Wikimedia_Commons_%28cropped%29.jpg"
    image_url2 = "https://thehill.com/wp-content/uploads/sites/2/2022/08/CA_farm_08222022istock.jpg?w=1280"

    landmark = identify_landmark(image_url)
    print(landmark)
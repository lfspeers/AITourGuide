import AzureAIServices
import AzureAIServices.OpenAI
import AzureAIServices.Speech
import AzureAIServices.Vision

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/") 
async def root():
    return {"message": "Server Get Response"}

@app.post("/")
async def post(request: Request):
    json = await request.json()
    url = json['url']
    guide = json['guide']

    audio = generate_tour(url, guide)    
    return FileResponse(audio, media_type='audio/wav')

def generate_tour(image_url: str, tour_guide: str) -> str:
    vision_landmark = AzureAIServices.Vision.identify_landmark(image_url)
    openai_landmark = AzureAIServices.OpenAI.identify_landmark(image_url)
    landmark = openai_landmark

    if vision_landmark == openai_landmark:
        print("Landmark identified correctly.")
    else:
        print("Landmarks do not match. Defaulting to OpenAI landmark.")

    tour = AzureAIServices.OpenAI.generate_tour(landmark=landmark, tour_guide=tour_guide)
    audio_file = AzureAIServices.Speech.text_to_speech(text=tour['narration'], voice=tour['voice'])
    return audio_file


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=3000)

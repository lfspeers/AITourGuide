import AzureAIServices
import AzureAIServices.OpenAI
import AzureAIServices.Speech
import AzureAIServices.Vision


image_url = "https://t0.gstatic.com/licensed-image?q=tbn:ANd9GcRbJlEsYPSWPePZfdem0Da64OI4Tb15exWoL35SjVFMVBhRPebfwNZY49XgFxpzEGhG"

vision_landmark = AzureAIServices.Vision.identify_landmark(image_url)
openai_landmark = AzureAIServices.OpenAI.identify_landmark(image_url)
landmark = openai_landmark

if vision_landmark == openai_landmark:
    print("Landmark identified correctly.")
else:
    print("Landmarks do not match. Defaulting to OpenAI landmark.")


print("Generating tour...")
tour_guide = "Brian" # Guy, Ava, Brian
tour = AzureAIServices.OpenAI.generate_tour(landmark=landmark, tour_guide=tour_guide)


audio_file = AzureAIServices.Speech.text_to_speech(text=tour['narration'], voice=tour['voice'])


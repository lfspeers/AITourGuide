# AITourGuide
Azure AI Services powered tour guide.


Steps
1. Identify Landmark
    * Models
        * AI Vision - Landmark Detection
        * GPT Multimodal - Image
    * Compare responses for accuracy
        * Default to GPT model if they don't match (could also prompt the user)
    * Return
        * Landmark name
2. Select Tour Guide
    * 3 Prebuilt personas
        * System message
            * Tone, language, topics
        * Azure AI Voice
3. Generate Tour Text
    * Models
        * Any GPT-4 model
    * Parameters
        * System Message
        * Persona name
        * Landmark name
    * Return
        * Tour guide text
4. TTS Tour
    * Parameters
        * Tour guide text
    * Model
        * Speech - TTS
        * OpenAI - Whisper
    * Return
        * Audio Guided Tour
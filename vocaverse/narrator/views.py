from django.shortcuts import render
from django.http import JsonResponse
import time
import os # For environment variables, important for API keys
import requests
import json

# Import the Murf AI SDK
# You'll need to install it: pip install murf-ai
from murf import Murf
#from murf.models.text_to_speech_body import TextToSpeechBody # Uncommented
#from murf.models.export_project_body import ExportProjectBody # Uncommented


def index(request):
    """
    Renders the main index.html page for the VocaVerse application.
    This is the entry point for the web interface.
    """
    return render(request, 'narrator/index.html')

def narrate_story(request):
    """
    Handles the POST request for story narration using the Murf AI SDK.
    It takes story text and a voice ID, interacts with the Murf API
    to generate and export the audio, and returns a JSON response
    with the audio URL.
    """
    if request.method == 'POST':
        
        story_text = request.POST['story']
        voice_id = request.POST['voice'] # Now using a single voice_id directly

        if not story_text or not voice_id:
            return JsonResponse({'error': 'Story text and voice selection are required.'}, status=400)

        # Initialize Murf AI client
        # IMPORTANT: Replace "YOUR_MURF_API_KEY" with your actual Murf API key.
        # It's highly recommended to store API keys in environment variables
        # (e.g., using python-dotenv or Django settings) rather than hardcoding.
        murf_api_key = os.environ.get("MURF_API_KEY", "ap2_e2da2b7c-45e8-469d-a66e-56dc439ab83e")
        
        try:
            client = Murf(api_key=murf_api_key)

            # Step 1: Create Text to Speech project
            # The language is implicitly handled by the voice_id
            
            tts_response = client.text_to_speech.generate( text=story_text,voice_id=voice_id,)        

            audio_url = tts_response.audio_file
            
            if not audio_url:
                return JsonResponse({'error': 'Failed to create Murf project.', 'details': tts_response.error_message}, status=500)

            return render(request, 'narrator/index.html', {
                'story': story_text,                
                'audio_url': audio_url,
                'story_text': story_text
            }) 

        except Exception as e:
            # Catch any other exceptions from the SDK or network issues
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=400)
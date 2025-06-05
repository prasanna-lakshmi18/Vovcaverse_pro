from django.shortcuts import render
from django.http import JsonResponse
import time
import os # For environment variables, important for API keys
import requests

# Import the Murf AI SDK
# You'll need to install it: pip install murf-ai
from murf import Murf
#from murf.models.text_to_speech_body import TextToSpeechBody
#from murf.models.export_project_body import ExportProjectBody


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
        story_text = request.POST.get('story')
        voice_id = request.POST.get('voice') # Now using a single voice_id directly

        if not story_text or not voice_id:
            return JsonResponse({'error': 'Story text and voice selection are required.'}, status=400)

        # Initialize Murf AI client
        # IMPORTANT: Replace "YOUR_MURF_API_KEY" with your actual Murf API key.
        # It's highly recommended to store API keys in environment variables
        # (e.g., using python-dotenv or Django settings) rather than hardcoding.
        murf_api_key = os.environ.get("MURF_API_KEY", "ap2_e2da2b7c-45e8-469d-a66e-56dc439ab83e")
        
        try:
            client = MurfAI(api_key=murf_api_key)

            # Step 1: Create Text to Speech project
            # The language is implicitly handled by the voice_id
            tts_response = client.text_to_speech(
                body=TextToSpeechBody(
                    text=story_text,
                    voice_id=voice_id
                )
            )
            
            project_id = tts_response.project_id
            if not project_id:
                return JsonResponse({'error': 'Failed to create Murf project.', 'details': tts_response.error_message}, status=500)

            # Step 2: Export the project
            export_response = client.export_project(
                body=ExportProjectBody(
                    project_id=project_id,
                    format="mp3" # You can choose "wav" or "mp3"
                )
            )
            export_id = export_response.export_id
            if not export_id:
                return JsonResponse({'error': 'Failed to export Murf project.', 'details': export_response.error_message}, status=500)

            # Step 3: Poll for export status until completed and get the URL
            audio_url = None
            max_retries = 30 # Max 30 retries (e.g., 30 * 2 seconds = 60 seconds)
            retry_delay = 2 # seconds
            for i in range(max_retries):
                get_export_response = client.get_export(export_id=export_id)
                status = get_export_response.status

                if status == "completed":
                    audio_url = get_export_response.export_url
                    break
                elif status == "failed":
                    return JsonResponse({'error': 'Murf audio export failed.', 'details': get_export_response.error_message}, status=500)
                
                time.sleep(retry_delay) # Wait before polling again

            if not audio_url:
                return JsonResponse({'error': 'Murf audio export timed out or failed to complete.'}, status=500)

            # Return the audio URL
            return JsonResponse({'audio_urls': [audio_url]})

        except Exception as e:
            # Catch any other exceptions from the SDK or network issues
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=400)


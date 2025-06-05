document.getElementById('streamButton').addEventListener('click', async function() {
    // Get references to HTML elements
    const storyInput = document.getElementById('storyInput');
    const voiceSelector = document.getElementById('voiceSelector');
    const streamButton = document.getElementById('streamButton');
    const playbackArea = document.getElementById('playbackArea');
    const loadingMessage = document.getElementById('loadingMessage');
    const errorMessage = document.getElementById('errorMessage');

    // Clear previous messages and audio
    playbackArea.innerHTML = '';
    errorMessage.textContent = '';
    errorMessage.classList.add('hidden');

    // Get input values
    const story = storyInput.value;
    const voice = voiceSelector.value;

    // Basic input validation
    if (!story.trim()) {
        errorMessage.textContent = 'Please enter some story text.';
        errorMessage.classList.remove('hidden');
        return;
    }
    if (!voice) {
        errorMessage.textContent = 'Please select a voice.';
        errorMessage.classList.remove('hidden');
        return;
    }

    // Disable button and show loading message
    streamButton.disabled = true;
    loadingMessage.classList.remove('hidden');

    try {
        // Send the POST request to the Django backend
        const response = await fetch('/narrate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken') // Helper function to get CSRF token
            },
            body: new URLSearchParams({
                'story': story,
                'voice': voice // Only sending voice now, as language is implicit in voice_id
            })
        });

        // Check if the response was successful (HTTP status 2xx)
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        if (data.audio_urls && data.audio_urls.length > 0) {
            // If audio URLs are received, create and append audio elements
            data.audio_urls.forEach(url => {
                const audio = document.createElement('audio');
                audio.controls = true; // Show playback controls
                audio.src = url;
                // Optional: Automatically play the first audio
                // audio.play(); 
                playbackArea.appendChild(audio);
            });
        } else {
            errorMessage.textContent = 'No audio URLs received from the server.';
            errorMessage.classList.remove('hidden');
        }

    } catch (error) {
        // Handle any errors during fetch or JSON parsing
        console.error('Error narrating story:', error);
        errorMessage.textContent = `Error: ${error.message}. Please try again.`;
        errorMessage.classList.remove('hidden');
    } finally {
        // Re-enable button and hide loading message regardless of success or failure
        streamButton.disabled = false;
        loadingMessage.classList.add('hidden');
    }
});

/**
 * Helper function to retrieve a cookie value by name.
 * Essential for Django's CSRF protection.
 * @param {string} name - The name of the cookie to retrieve.
 * @returns {string|null} The value of the cookie, or null if not found.
 **/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

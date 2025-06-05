
# 🎙️ VocaVerse – AI-Powered Story Narrator

VocaVerse is a Django web application that uses the Murf AI API to convert written stories into lifelike audio narration. Simply enter your story, choose a voice, and get an audio file instantly!

---

## 🚀 Features

- 🎧 Text-to-Speech conversion using Murf AI
- 🗣️ Choose from various voice options
- 🔗 Get a sharable audio link
- 💡 Simple Django backend with `POST` story upload
- ✅ Clean API integration without saving to DB

---

## 🛠️ Tech Stack

- **Backend**: Django  
- **API**: Murf AI (via Python SDK)  
- **Frontend**: HTML (Django templating)  
- **Misc**: Requests, JSON, Time, OS  

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/your-username/vocaverse.git
cd vocaverse

# Install dependencies
pip install -r requirements.txt

# Install Murf SDK (if not in requirements)
pip install murf-ai

# Run the Django server
python manage.py runserver
```

---

## 🔐 API Key Setup

Set your Murf API key in environment variables:

```bash
export MURF_API_KEY="your_murf_api_key_here"
```

Or create a `.env` file:

```env
MURF_API_KEY=your_murf_api_key_here
```

Use `python-dotenv` to load it automatically.

---

## 🧠 Usage

### 1. Navigate to the Home Page

Run the server and open:

```
http://127.0.0.1:8000/
```

### 2. Submit a Story

- Enter your story text.
- Choose a `voice_id` (e.g., `en_us_john`).
- Click **Narrate**.

---

## 🧪 Backend Code Example

```python
from django.shortcuts import render
from django.http import JsonResponse
import os
from murf import Murf

def narrate_story(request):
    if request.method == 'POST':
        story_text = request.POST['story']
        voice_id = request.POST['voice']

        murf_api_key = os.environ.get("MURF_API_KEY")
        client = Murf(api_key=murf_api_key)

        tts_response = client.text_to_speech.generate(
            text=story_text,
            voice_id=voice_id
        )

        audio_url = tts_response.audio_file
        return JsonResponse({'audio_urls': [audio_url]})
```

---

## 🌐 Frontend Integration (`index.html`)

```html
<form method="POST" id="narrateForm">
  <textarea name="story" placeholder="Enter your story..."></textarea>
  <select name="voice">
    <option value="en_us_john">John</option>
    <option value="en_us_emma">Emma</option>
  </select>
  <button type="submit">Narrate</button>
</form>

<audio id="audioPlayer" controls style="display:none;"></audio>

```

---

## 🗃 Example Voice IDs

- `en_us_john`
- `en_us_emma`
- `en_uk_brian`

Refer to [Murf API Docs](https://docs.murf.ai/) for full list.

---

## 🤝 Contributing

Pull requests are welcome! If you'd like to improve the UI, add voice previews, or support multiple languages — go for it 🚀

---

## 📄 License

MIT License — feel free to use, modify, and share!

---

## 📢 Credits

- [Murf AI](https://murf.ai/) for the TTS magic.  
- Built with ❤️ by [Prasanna Lakshmi]

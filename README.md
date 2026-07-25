# Guitar Tab Transcriber

A full-stack web application that transcribes audio files into guitar tablature using deep learning.

🎸 **[Try it live →](https://guitar-tab-transcriber.netlify.app/)**

---

## About

Guitar Tab Transcriber analyses an uploaded audio file and converts the detected melody into ASCII guitar tablature. It uses [Basic Pitch](https://basicpitch.spotify.com/) by Spotify for pitch and onset detection, maps each note to the most playable fret position across all six strings, and renders the result directly in the browser.

The transcriber works best on clean, isolated melody tracks. For best results, use [splitter.ai](https://splitter.ai/) to separate your audio into individual components before uploading.

> **Disclaimer:** The transcriber is not 100% accurate. Due to the complexity of audio analysis, it may occasionally detect extra notes or artifacts. Use the output as a guide and apply your own musical judgement.

---

## Features

- **Audio upload** - drag and drop or click to browse. Supports `.mp3`, `.wav`, `.flac`, `.ogg`, `.m4a`
- **Octave shift** - slider control to shift the detected melody up or down by up to 2 octaves
- **Deep learning transcription** - uses Basic Pitch (Spotify) for pitch and onset detection
- **Harmonic filtering** - custom algorithm suppresses overtones and phantom notes
- **Position-aware fingering** - maps notes to the most playable fret positions across all six strings
- **In-browser tab rendering** - ASCII tablature rendered directly in the browser with monospace formatting
- **Download as .txt** - export the tab as a plain text file
- **Async processing** - long-running transcription jobs run in the background with live polling

---

## Recommended Workflow

For the cleanest results:

1. Find or record the audio you want to transcribe
2. Go to [splitter.ai](https://splitter.ai/) and upload your track
3. Download the isolated melody/lead component
4. Upload that file to Guitar Tab Transcriber
5. Adjust the octave shift if notes seem too high or too low
6. Download or copy the generated tab

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, TypeScript, Tailwind CSS, Vite |
| Backend | Python, FastAPI, uvicorn |
| ML / Audio | Basic Pitch (Spotify), librosa |
| Frontend Hosting | Netlify |
| Backend Hosting | Render |

---

## Project Structure

```
guitar-tab-transcriber/
├── frontend/                         # React + TypeScript frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── Hero.tsx              # Title, subtitle, tip banner
│   │   │   ├── UploadSection.tsx     # File upload, octave controls, polling
│   │   │   ├── TabDisplay.tsx        # ASCII tab renderer
│   │   │   ├── DownloadButton.tsx    # Client-side .txt download
│   │   │   ├── LoadingAnimation.tsx  # Note → fret animation
│   │   │   └── Footer.tsx            # Footer with GitHub link
│   │   ├── App.tsx                   # Root component, state management
│   │   └── main.tsx
│   ├── index.html
│   └── vite.config.ts
│
├── backend/                          # Python FastAPI backend
│   ├── main.py                       # FastAPI entry point, routes, job management
│   ├── transcription.py              # Note detection, harmonic filtering, fingering logic
│   ├── tab_writer.py                 # ASCII tab grid builder
│   ├── config.py                     # Guitar tuning, thresholds, display constants
│   ├── audio.py                      # Audio validation helpers
│   ├── temp/                         # Temporary uploaded audio files (auto-cleaned)
│   ├── Procfile                      # Render start command
│   ├── runtime.txt                   # Python version pin
│   └── requirements.txt
│
└── README.md
```

---

## Running Locally

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

> Make sure `BACKEND_URL` in `UploadSection.tsx` points to `http://localhost:8000` when running locally.

---

## Python Version

This project requires **Python 3.11**. The `basic-pitch` library has limited Python version support - refer to their [documentation](https://github.com/spotify/basic-pitch) for the latest compatibility info.

---

## Dependencies

```
librosa
basic-pitch
fastapi
uvicorn
python-multipart
setuptools
```
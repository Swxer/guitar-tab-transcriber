import os
import uuid
import shutil
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from config import SUPPORTED_EXTENSIONS, MAX_FILE_SIZE
from transcription import note_to_tab, filter_harmonics
from tab_writer import create_ascii_tabs, build_tab_for_api

from basic_pitch.inference import predict, Model, ICASSP_2022_MODEL_PATH

basic_pitch_model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global basic_pitch_model
    print("Loading Basic Pitch model...")
    basic_pitch_model = Model(ICASSP_2022_MODEL_PATH)
    print("Model ready.")
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

jobs = {}

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

def run_pipeline(job_id: str, file_path: str, octave_shift: int):
    try:
        _, __, note_events = predict(file_path, basic_pitch_model)

        note_events = filter_harmonics(note_events)
        mapped_notes, song_length = note_to_tab(note_events, octave_shift)

        if not mapped_notes:
            jobs[job_id] = {"status": "error", "message": "No notes detected. Try a cleaner audio file or adjust the octave shift."}
            return

        output_path = os.path.join(TEMP_DIR, f"{job_id}.txt")
        create_ascii_tabs(mapped_notes, song_length, output_path)

        tab_lines = build_tab_for_api(mapped_notes, song_length)

        jobs[job_id] = {
            "status": "done",
            "tab": tab_lines,
            "output_path": output_path
        }

    except Exception as e:
        jobs[job_id] = {"status": "error", "message": str(e)}

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@app.post("/transcribe")
async def transcribe(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    octave_shift: int = Form(0)
):
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        return {"error": "File too large. Please upload a file under 10MB."}
    
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        return {"error": f"Unsupported file format: {ext}"}

    job_id = str(uuid.uuid4())
    temp_path = os.path.join(TEMP_DIR, f"{job_id}{ext}")

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    jobs[job_id] = {"status": "processing"}

    background_tasks.add_task(run_pipeline, job_id, temp_path, octave_shift)

    return {"job_id": job_id}


@app.get("/status/{job_id}")
def get_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        return {"status": "not_found"}

    return {
        "status": job["status"],
        "tab": job.get("tab"),
        "message": job.get("message")
    }


@app.get("/download/{job_id}")
def download_tab(job_id: str):
    job = jobs.get(job_id)
    if not job or job["status"] != "done":
        return {"error": "Tab not ready or job not found"}

    output_path = job.get("output_path")
    if not output_path or not os.path.exists(output_path):
        return {"error": "Output file not found"}

    return FileResponse(
        path=output_path,
        filename="tab.txt",
        media_type="text/plain"
    )

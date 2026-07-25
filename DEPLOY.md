# Deployment Guide

This document contains everything needed to run and redeploy the Guitar Tab Transcriber.
I'm not gonna remember anything if I revisit this project haha.

---

## Architecture

| Service | Platform | URL |
|---|---|---|
| Frontend | Netlify (auto-deploys from `main`) | https://guitar-tab-transcriber.netlify.app |
| Backend | GCP Cloud Run | https://guitar-tab-transcriber-531130921984.us-central1.run.app |

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

> Make sure `BACKEND_URL` in `frontend/src/components/UploadSection.tsx` points to `http://localhost:8000` when running locally, and restore the GCP URL before pushing.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

---

## Redeploying Backend to GCP Cloud Run

Run these commands from inside the `backend/` folder with `venv` active.

### Step 1 — Authenticate

```bash
gcloud auth login
gcloud config set project project-84038f5c-e763-41de-8bb
```

### Step 2 — Build the Docker image

```bash
gcloud builds submit --tag gcr.io/project-84038f5c-e763-41de-8bb/guitar-tab-transcriber . --service-account=projects/project-84038f5c-e763-41de-8bb/serviceAccounts/cloud-run-sa@project-84038f5c-e763-41de-8bb.iam.gserviceaccount.com --default-buckets-behavior=REGIONAL_USER_OWNED_BUCKET
```

### Step 3 — Deploy to Cloud Run

```bash
gcloud run deploy guitar-tab-transcriber --image gcr.io/project-84038f5c-e763-41de-8bb/guitar-tab-transcriber --region us-central1 --allow-unauthenticated --memory 2Gi --port 8080 --max-instances 1 --service-account=cloud-run-sa@project-84038f5c-e763-41de-8bb.iam.gserviceaccount.com
```

### Step 4 — Update frontend if the URL changed

If GCP gives you a new service URL, update `BACKEND_URL` in `frontend/src/components/UploadSection.tsx` and push to GitHub. Netlify auto-deploys.

---

## Redeploying Frontend to Netlify

Netlify auto-deploys whenever you push to `main`. No manual steps needed.

If you need to reconnect the repo:
1. Go to [netlify.com](https://netlify.com)
2. Add new site → Import from GitHub
3. Base directory: `frontend`
4. Build command: `npm run build`
5. Publish directory: `frontend/dist`

---

## GCP Project Details

| Field | Value |
|---|---|
| Project ID | `project-84038f5c-e763-41de-8bb` |
| Project Number | `531130921984` |
| Region | `us-central1` |
| Service Account | `cloud-run-sa@project-84038f5c-e763-41de-8bb.iam.gserviceaccount.com` |
| Container Registry | `gcr.io/project-84038f5c-e763-41de-8bb/guitar-tab-transcriber` |

---

## Monitoring

- **GCP Cloud Run logs** — [console.cloud.google.com](https://console.cloud.google.com) → Cloud Run → guitar-tab-transcriber → Logs
- **GCP Metrics** — same page → Metrics tab (memory, CPU, request count)
- **Netlify deploys** — [netlify.com](https://netlify.com) → guitar-tab-transcriber → Deploys

---

## Notes

- GCP Cloud Run free tier: 2 million requests/month, resets monthly. Will not cost anything for a low traffic portfolio project.
- Set a budget alert in GCP Billing to get notified before any charges occur.
- Cloud Run scales to zero when idle — first request after inactivity has a cold start delay of ~10-30 seconds.
- The keep-alive ping in `UploadSection.tsx` fires every 10 minutes to reduce cold starts while the page is open.
- Basic Pitch (TensorFlow) uses ~800MB RAM during inference. The 2GB limit gives comfortable headroom.
- Do NOT push `venv/` to GitHub. The `.gcloudignore` excludes it from GCP builds too.
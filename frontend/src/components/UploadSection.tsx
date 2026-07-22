import { useState, useRef } from "react"

type Props = {
  status: 'idle' | 'processing' | 'done' | 'error'
  setStatus: (status: "idle" | "processing" | "done" | "error") => void
  setJobId: (jobId: string | null) => void
  setTab: (tab: string[][]) => void
  setErrorMessage: (message: string | null) => void
}

const BACKEND_URL = "http://localhost:8000"
const POLLING_INTERVAL = 2000

function UploadSection({ status, setStatus, setJobId, setTab, setErrorMessage }: Props) {
  return <div>Upload Section</div>
}

export default UploadSection
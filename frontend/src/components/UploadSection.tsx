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

  const [file, setFile] = useState<File | null>(null)
  const [octaveShift, setOctaveShift] = useState<number>(0)
  const [isDragging, setIsDragging] = useState<boolean>(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    if (e.target.files?.[0])  
      setFile(e.target.files[0])
  }

  function handleDrop(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault()
    setIsDragging(false)
    if (e.dataTransfer.files?.[0])
      setFile(e.dataTransfer.files[0])
  }

  function handleDragOver(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault()
    setIsDragging(true)
  }

  function handleDragLeave(e: React.DragEvent<HTMLDivElement>) {
    setIsDragging(false)
  }

  function pollStatus(jobId: string) {
    const interval = setInterval(
      async () => {
        try {
          const response = await fetch(`${BACKEND_URL}/status/${jobId}`)
          const data = await response.json()
          if (data.status === "done") {
            clearInterval(interval)
            setJobId(jobId)
            setTab(data.tab)
            setStatus("done")
          } else if (data.status === "error") {
            clearInterval(interval)
            setErrorMessage(data.message && 'Something went wrong')
            setStatus("error")
          }
        } catch (error) {
          clearInterval(interval)
          setErrorMessage('Could not reach the server')
          setStatus("error")
        }
      }, POLLING_INTERVAL)
  }

  async function handleSubmit() {
    if (!file) return

    const formData = new FormData()
    formData.append("file", file)
    formData.append("octave_shift", octaveShift.toString())

    setStatus("processing")

    try {
      const res = await fetch(`${BACKEND_URL}/transcribe`, {
        method: 'POST',
        body: formData,
      })

      const data = await res.json()

      if (data.error) {
        setErrorMessage(data.error)
        setStatus("error")
        return
      }

      pollStatus(data.job_id)
    } catch {
      setErrorMessage('Could not reach the server. Is the backend running?')
      setStatus("error")
    }

  }

  const isProcessing = status === "processing"

  return (
    <div className="w-full max-w-lg flex flex-col gap-6">

      {/* Drop zone */}
      <div
        onClick={() => fileInputRef.current?.click()}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`
          border-2 border-dashed rounded-xl p-12
          flex flex-col items-center justify-center gap-3
          cursor-pointer transition-colors duration-200
          ${isDragging
            ? 'border-violet-400 bg-violet-950'
            : 'border-gray-600 bg-gray-900 hover:border-gray-400'
          }
        `}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".mp3,.wav,.flac,.ogg,.m4a"
          onChange={handleFileChange}
          className="hidden"
        />

        <p className="text-gray-400 text-sm">
          {file ? file.name : 'Drag and drop your audio file here, or click to browse'}
        </p>
        <p className="text-gray-600 text-xs">Supports .mp3, .wav, .flac, .ogg, .m4a</p>
      </div>

      {/* Octave shift */}
      <div className="flex flex-col gap-2">
        <label className="text-sm text-gray-400">
          Octave Shift: <span className="text-white font-medium">{octaveShift}</span>
        </label>
        <input
          type="range"
          min={-2}
          max={2}
          value={octaveShift}
          onChange={(e) => setOctaveShift(Number(e.target.value))}
          className="w-full accent-violet-500"
        />
        <div className="flex justify-between text-xs text-gray-600">
          <span>-2 (lower)</span>
          <span>0 (none)</span>
          <span>+2 (higher)</span>
        </div>
      </div>

      <button
        onClick={handleSubmit}
        disabled={!file || isProcessing}
        className={`
          w-full py-3 rounded-xl font-semibold text-sm transition-colors duration-200
          ${!file || isProcessing
            ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
            : 'bg-violet-600 hover:bg-violet-500 text-white cursor-pointer'
          }
        `}
      >
        {isProcessing ? 'Transcribing...' : 'Transcribe'}
      </button>

    </div>
  )
}

export default UploadSection
import { useState } from "react"
import UploadSection from './components/UploadSection'
import TabDisplay from './components/TabDisplay'
import DownloadButton from './components/DownloadButton'
import Footer from './components/Footer'
import Hero from "./components/Hero"

type Status = "idle" | "processing" | "done" | "error"

function App() {

  const [status, setStatus] = useState<Status>("idle")
  const [jobId, setJobId] = useState<string | null>(null)
  const [tab, setTab] = useState<string[][]>([])
  const [errorMessage, setErrorMessage] = useState<string | null>(null)

  return (
    <div className="min-h-screen bg-gray-950 text-white flex flex-col items-center py-16 px-4">
      <Hero />

      <UploadSection 
        status={status}
        setStatus={setStatus} 
        setJobId={setJobId} 
        setTab={setTab} 
        setErrorMessage={setErrorMessage} 
      />

      {status === "processing" && (
        <p className="mt-8 text-gray-400 animate-pulse">Processing...</p>
      )}

      {status === 'error' && (
        <p className="mt-8 text-red-400">{errorMessage ?? 'Something went wrong.'}</p>
      )}

      {status === "done" && (
        <>
          <TabDisplay tab={tab} />
          <DownloadButton jobId={jobId} tab={tab} />
        </>
      )}

      <Footer />
    </div>
  )
}

export default App

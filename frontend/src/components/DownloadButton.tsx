type Props = {
  jobId: string | null
}

function DownloadButton({ jobId }: Props) {
  function handleDownload() {
    if (!jobId) return
    window.open(`http://localhost:8000/download/${jobId}`, '_blank')
  }

  return (
    <div className="mt-6 mb-16">
      <button
        onClick={handleDownload}
        className="px-6 py-3 bg-gray-800 hover:bg-gray-700 text-white text-sm font-semibold rounded-xl transition-colors duration-200 cursor-pointer"
      >
        Download as .txt
      </button>
    </div>
  )
}

export default DownloadButton
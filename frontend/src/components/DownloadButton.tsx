type Props = {
  jobId: string | null
  tab: string[][]
}

function DownloadButton({ jobId, tab }: Props) {
  function handleDownload() {
    if (!tab || tab.length === 0) return

    // Convert tab chunks into plain text
    const content = tab
      .map(chunk => chunk.join('\n'))
      .join('\n\n')

    // Create a blob and trigger download
    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'tab.txt'
    a.click()
    URL.revokeObjectURL(url)
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
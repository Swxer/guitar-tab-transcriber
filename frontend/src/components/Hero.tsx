function Hero() {
  return (
    <>
      <h1 className="text-4xl font-bold mb-2">Guitar Tab Transcriber</h1>
      <p className="text-gray-400 mb-12">Upload an audio file and get the transcribed tab instantly.</p>


      <div className="w-full max-w-lg bg-gray-900 border border-gray-700 rounded-xl p-4 mb-8 text-sm text-gray-400">
        <p className="font-semibold text-gray-300 mb-1">For best results</p>
        <p>
          Use{' '}
          <a
            href="https://splitter.ai"
            target="_blank"
            rel="noopener noreferrer"
            className="text-violet-400 hover:text-violet-300 underline"
          >
            splitter.ai
          </a>
          {' '}to isolate the melody from your track before uploading. The transcriber works best on clean, single-instrument audio.
        </p>
      </div>
    </>
  )
}

export default Hero
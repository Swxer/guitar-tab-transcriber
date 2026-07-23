function Footer() {
  return (
    <footer className="mt-16 mb-8 text-center text-gray-600 text-xs">
      <p>
        Built by{' '}
        <a
          href="https://github.com/Swxer"
          target="_blank"
          rel="noopener noreferrer"
          className="text-gray-500 hover:text-gray-300 underline"
        >
          Steven L. Nguyen
        </a>
        {' '}·{' '}
        <a
          href="https://github.com/Swxer/guitar-tab-transcriber"
          target="_blank"
          rel="noopener noreferrer"
          className="text-gray-500 hover:text-gray-300 underline"
        >
          View on GitHub
        </a>
      </p>
    </footer>
  )
}

export default Footer
import { useEffect, useState } from 'react'

const NOTE_MAPPINGS: Record<string, { fret: number; string: string }[]> = {
  'E2': [{ fret: 0, string: 'E string' }],
  'F2': [{ fret: 1, string: 'E string' }],
  'G2': [{ fret: 3, string: 'E string' }],
  'A2': [{ fret: 5, string: 'E string' }, { fret: 0, string: 'A string' }],
  'B2': [{ fret: 7, string: 'E string' }, { fret: 2, string: 'A string' }],
  'C3': [{ fret: 8, string: 'E string' }, { fret: 3, string: 'A string' }],
  'D3': [{ fret: 10, string: 'E string' }, { fret: 5, string: 'A string' }, { fret: 0, string: 'D string' }],
  'E3': [{ fret: 12, string: 'E string' }, { fret: 7, string: 'A string' }, { fret: 2, string: 'D string' }],
  'F3': [{ fret: 8, string: 'A string' }, { fret: 3, string: 'D string' }],
  'G3': [{ fret: 10, string: 'A string' }, { fret: 5, string: 'D string' }, { fret: 0, string: 'G string' }],
  'A3': [{ fret: 12, string: 'A string' }, { fret: 7, string: 'D string' }, { fret: 2, string: 'G string' }],
  'B3': [{ fret: 9, string: 'D string' }, { fret: 4, string: 'G string' }, { fret: 0, string: 'B string' }],
  'C4': [{ fret: 10, string: 'D string' }, { fret: 5, string: 'G string' }, { fret: 1, string: 'B string' }],
  'D4': [{ fret: 12, string: 'D string' }, { fret: 7, string: 'G string' }, { fret: 3, string: 'B string' }],
  'E4': [{ fret: 9, string: 'G string' }, { fret: 5, string: 'B string' }, { fret: 0, string: 'e string' }],
  'F4': [{ fret: 10, string: 'G string' }, { fret: 6, string: 'B string' }, { fret: 1, string: 'e string' }],
  'G4': [{ fret: 12, string: 'G string' }, { fret: 8, string: 'B string' }, { fret: 3, string: 'e string' }],
  'A4': [{ fret: 10, string: 'B string' }, { fret: 5, string: 'e string' }],
  'B4': [{ fret: 12, string: 'B string' }, { fret: 7, string: 'e string' }],
}

const NOTES = Object.keys(NOTE_MAPPINGS)

function randomFrom<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)]
}

function LoadingAnimation() {
  const [note, setNote] = useState('')
  const [fret, setFret] = useState('')
  const [guitarString, setGuitarString] = useState('')
  const [showColdStartMessage, setShowColdStartMessage] = useState(false)

  useEffect(() => {
    function update() {
      const selectedNote = randomFrom(NOTES)
      const selectedMapping = randomFrom(NOTE_MAPPINGS[selectedNote])

      setNote(selectedNote)
      setFret(`fret ${selectedMapping.fret}`)
      setGuitarString(selectedMapping.string)
    }

    update()
    const interval = setInterval(update, 1800)
    const coldStartTimer = setTimeout(() => setShowColdStartMessage(true), 20000)

    return () => {
      clearInterval(interval)
      clearTimeout(coldStartTimer)
    }
      
  }, [])

  return (
    <div className="mt-8 flex flex-col items-center gap-4">
      <div className="flex items-center gap-4 font-mono text-lg animate-pulse">
        <span className="text-violet-400">{note}</span>
        <span className="text-gray-600">→</span>
        <div className="flex flex-col gap-1">
          <span className="text-green-400">{fret}</span>
          <span className="text-blue-400">{guitarString}</span>
        </div>
      </div>

      {!showColdStartMessage ? (
        <p className="text-gray-500 text-lg animate-pulse">Transcribing your audio...</p>
      ) : (
        <p className="text-gray-500 text-lg animate-pulse">
          Still warming up, the server may be waking from sleep. Hang tight...
        </p>
      )}
    </div>
  )
}

export default LoadingAnimation
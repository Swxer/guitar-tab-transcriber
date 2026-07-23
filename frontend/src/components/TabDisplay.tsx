type Props = {
  tab: string[][]
}

function TabDisplay({ tab }: Props) {
 return (
    <div className="w-full max-w-4xl mt-12 flex flex-col gap-6">
      <h2 className="text-xl font-semibold text-white">Your Tab</h2>
      {tab
        .filter(chunk => chunk.some(line => /\d/.test(line))) // only keep chunks with at least one number
        .map((chunk, i) => (
          <div key={i} className="overflow-x-auto bg-gray-900 rounded-xl p-6">
            {chunk.map((line, j) => (
              <pre key={j} className="text-green-400 text-sm font-mono leading-6">
                {line}
              </pre>
            ))}
          </div>
        ))}
    </div>
  )
}

export default TabDisplay
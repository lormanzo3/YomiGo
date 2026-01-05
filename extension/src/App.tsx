import React, { useState } from 'react'

interface Token {
  surface: string
  reading: string
  dictionary_form: string
  part_of_speech: string
  definitions: string[]
  is_phrase?: boolean
}

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [extractedText, setExtractedText] = useState<string>('')
  const [tokens, setTokens] = useState<Token[]>([])
  const [isLoading, SetIsLoading] = useState<boolean>(false)

  function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
    }
  }

  async function handleUpload() {
    if (!selectedFile) return

    SetIsLoading(true)

    const formData = new FormData()
    formData.append('image', selectedFile)

    const ocrResponse = await fetch('http://127.0.0.1:8000/ocr', {
      method: 'POST',
      body: formData,
    })

    const ocrData = await ocrResponse.json()
    setExtractedText(ocrData.text)

    const parseResponse = await fetch('http://127.0.0.1:8000/parse', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: ocrData.text }),
    })

    const parseData = await parseResponse.json()
    setTokens(parseData.tokens)

    SetIsLoading(false)
  }

  return (
    <div>
      <h1>YomiGo</h1>

      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
      />

      {selectedFile && <p>Selected: {selectedFile.name}</p>}

      <button onClick={handleUpload} disabled={!selectedFile || isLoading}>
        {isLoading ? 'Processing...' : 'Extract Text'}
      </button>

      {extractedText && (
        <div>
          <h2>Extracted Text:</h2>
          <p>{extractedText}</p>
        </div>
      )}

      {tokens.length > 0 && (
          <div>
            <h2>Word Breakdown:</h2>
            {tokens.map((token, index) => (
              <div key={index}>
                <strong>{token.surface}</strong>
                {token.reading && <span> ({token.reading})</span>}
                {token.definitions.length > 0 && (
                  <ul>
                    {token.definitions.map((def, i) => (
                      <li key={i}>{def}</li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    )
  }

export default App

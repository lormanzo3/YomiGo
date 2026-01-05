import React, { useState } from 'react'

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [extractedText, setExtractedText] = useState<string>('')
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

    const response = await fetch('http://127.0.0.1:8000/ocr', {
      method: 'POST',
      body: formData,
    })

    const data = await response.json()
    setExtractedText(data.text)
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
    </div>
  )
}

export default App

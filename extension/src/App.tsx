import React, { useState } from 'react'

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
    }
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
    </div>
  )
}

export default App

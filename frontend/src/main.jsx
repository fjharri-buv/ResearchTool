import React from 'react'
import { createRoot } from 'react-dom/client'

function App() {
  return (
    <div style={{ fontFamily: 'sans-serif', padding: '1rem' }}>
      <h1>Research Assistant</h1>
      <p>Frontend scaffold complete. Milestone 2 will implement Library UI.</p>
    </div>
  )
}

createRoot(document.getElementById('root')).render(<App />)

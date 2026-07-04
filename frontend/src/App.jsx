import { useState } from 'react'
import './App.css'
import backgroundImg from './src/assets/3d-style-black-background-with-paper-layer_206725-669.avif';

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!input.trim()) return

    // Add user message to UI
    const userMessage = { role: 'user', content: input }
    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setLoading(true)
    
    

    try {
      // Ping your FastAPI Docker container
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: userMessage.content }),
      })
      
      const data = await response.json()
      
      // Add AI response to UI
      setMessages((prev) => [...prev, { role: 'assistant', content: data.answer }])
    } catch (error) {
      setMessages((prev) => [...prev, { role: 'assistant', content: '🚨 Error connecting to the backend API.' }])
    }
    
    setLoading(false)
  }

  return (
    <div className={`chat-container flex flex-col justify-center items-center gap-4 p-4 lg:px-60 sm:px-20 w-full  min-h-screen bg-[url(${backgroundImg})] bg-cover  `}>
      <h1 className='flex justify-center justify-items-center'>🎓<p className=' bg-linear-to-r from-blue-500 to-indigo-700 text-transparent text-5xl font-extrabold bg-clip-text '> COMSATS RAG Assistant</p></h1>
      
    
      <div className="  rounded-2xl flex flex-col gap-4 p-6  w-full mx-10 min-h-100 max-h-100  scrollbar-none overflow-y-scroll scroll-smooth  shadow-gray-500/10 bg-gray-900/10 shadow-2xl ring-2 ring-white/10 backdrop-blur-md ">
        
        {messages.map((msg, idx) => (
          
          <>
          <div key={idx} >
            <div className={`font-bold text-white  ${msg.role === 'user' ? 'ml-auto self-start w-fit ' : 'mr-auto self-start w-fit '}`} >{msg.role === 'user' ? 'You: ' : 'Assistant: '}</div>
            <div className={`message ${msg.role === 
            'user' ? 'user-msg': 'AI-msg'}`}> 
              {msg.content}
            </div>         
          </div>
          </>
        ))}
        {loading && (
          <div className="flex flex-col items-start animate-fade-in-up">
             <span className="text-white font-bold mb-1">
              Assistant:
            </span>
            <div className="AI-msg flex gap-2 items-center p-4 ">
              <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.15s' }}></div>
              <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.3s' }}></div>
            </div>
          </div>
        )}
      </div>

      
   
    <form onSubmit={sendMessage} className="input-form flex w-full gap-2 p-4 float-bottom ">
        <input 
          type="text" 
          className='input-field '
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about the handbook..."
          disabled={loading}
        />
        <button type="submit" className='btn-primary ' disabled={loading}>Send</button>
      </form>
    </div>
  )
}

export default App
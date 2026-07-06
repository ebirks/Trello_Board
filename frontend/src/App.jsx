import { useState, useEffect } from 'react'
import axios from 'axios'

function App() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [token, setToken] = useState(localStorage.getItem('token') || '')

  const [boards, setBoards] = useState([])
  const [newBoardTitle, setNewBoardTitle] = useState('')

    const fetchBoards = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/boards/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      setBoards(response.data)
    } catch (error) {
      console.error("Failed to fetch boards", error)
    }
  }

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      fetchBoards()
    }
  }, [token])

  const handleLogin = async (e) => {
    e.preventDefault()
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/token/', {
        username: username,
        password: password
      })
      setToken(response.data.access)
      localStorage.setItem('token', response.data.access)
    } catch (error) {
      alert('Invalid credentials!')
    }
  }

    const handleCreateBoard = async (e) => {
    e.preventDefault()
    try {
      await axios.post('http://127.0.0.1:8000/api/boards/', {
        title: newBoardTitle
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setNewBoardTitle('')
      fetchBoards()
    } catch (error) {
      console.error("Failed to create board", error)
    }
  }

  const handleLogout = () => {
    setToken('')
    localStorage.removeItem('token')
    setBoards([])
  }

  if (token) {
    return (
      <div style={{ padding: '20px' }}>
        <h2>Cardify</h2>
        <button onClick={handleLogout}>Logout</button>

        <hr />

        <h3>Your Boards</h3>

        {/* Create Board Form */}
        <form onSubmit={handleCreateBoard} style={{ marginBottom: '20px' }}>
          <input
            type="text"
            placeholder="New board title"
            value={newBoardTitle}
            onChange={(e) => setNewBoardTitle(e.target.value)}
            required
          />
          <button type="submit">Add Board</button>
        </form>

        {/* Display Boards */}
        <div style={{ display: 'flex', gap: '20px' }}>
          {boards.map(board => (
            <div key={board.id} style={{ border: '1px solid black', padding: '20px', width: '200px' }}>
              <h4>{board.title}</h4>
              <p>{board.description || 'No description'}</p>
            </div>
          ))}
        </div>
      </div>
    )
  }

  // If not logged in, show the Login Form
  return (
    <div style={{ padding: '20px' }}>
      <h2>Login to Trello Clone</h2>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <br />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <br />
        <button type="submit">Login</button>
      </form>
    </div>
  )
}

export default App
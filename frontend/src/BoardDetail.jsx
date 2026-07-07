import { useState, useEffect } from 'react'
import axios from 'axios'

function BoardDetail({ boardId, token, goBack }) {
  const [columns, setColumns] = useState([])
  const [newColumnTitle, setNewColumnTitle] = useState('')

  const [cards, setCards] = useState([])
  const [cardInputs, setCardInputs] = useState({})

  const fetchColumns = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/columns/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      setColumns(response.data.filter(col => col.board === parseInt(boardId)))
    } catch (error) {
      console.error("Failed to fetch columns", error)
    }
  }

  const fetchCards = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/cards/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      setCards(response.data)
    } catch (error) {
      console.error("Failed to fetch cards", error)
    }
  }

  useEffect(() => {
    fetchColumns()
    fetchCards()
  }, [boardId])

  const handleAddColumn = async (e) => {
    e.preventDefault()
    try {
      await axios.post('http://127.0.0.1:8000/api/columns/', {
        title: newColumnTitle,
        board: boardId,
        position: columns.length
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setNewColumnTitle('')
      fetchColumns()
    } catch (error) {
      console.error("Failed to create column", error)
    }
  }

  const handleDeleteColumn = async (columnId) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/columns/${columnId}/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      fetchCards()
      fetchColumns()
    } catch (error) {
      console.error("Failed to delete column", error)
    }
  }

  const handleAddCard = async (e, columnId) => {
    e.preventDefault()
    const title = cardInputs[columnId]

    try {
      await axios.post('http://127.0.0.1:8000/api/cards/', {
        title: title,
        column: columnId,
        position: 0
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })

      setCardInputs({ ...cardInputs, [columnId]: '' })
      fetchCards()
    } catch (error) {
      console.error("Failed to create card", error)
    }
  }

  const handleDeleteCard = async (cardId) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/cards/${cardId}/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      fetchCards()
    } catch (error) {
      console.error("Failed to delete card", error)
    }
  }

  return (
    <div style={{ padding: '20px' }}>
      <button onClick={goBack} style={{ marginBottom: '20px' }}>&larr; Back to Boards</button>
      <h2>Board ID: {boardId}</h2>

      <div style={{ display: 'flex', gap: '20px', alignItems: 'flex-start' }}>

        {columns.map(col => (
          <div key={col.id} style={{ backgroundColor: '#f4f5f7', borderRadius: '5px', padding: '10px', width: '250px' }}>

            {/* Flex container for the title and the X button */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h4>{col.title}</h4>
              <button
                onClick={() => handleDeleteColumn(col.id)}
                style={{ border: 'none', background: 'none', color: 'red', cursor: 'pointer', fontWeight: 'bold' }}
              >
                X
              </button>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '5px', marginBottom: '10px' }}>
              {cards.filter(card => card.column === col.id).map(card => (
                <div key={card.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: 'white', padding: '8px', borderRadius: '3px', boxShadow: '0 1px 0 rgba(9,30,66,.25)' }}>
                  <span>{card.title}</span>
                  <button
                    onClick={() => handleDeleteCard(card.id)}
                    style={{ border: 'none', background: 'none', color: 'red', cursor: 'pointer', fontWeight: 'bold' }}
                  >
                    X
                  </button>
                </div>
              ))}
            </div>

            <form onSubmit={(e) => handleAddCard(e, col.id)}>
              <input
                type="text"
                placeholder="Add a card..."
                value={cardInputs[col.id] || ''} // Use empty string if undefined
                onChange={(e) => setCardInputs({ ...cardInputs, [col.id]: e.target.value })}
                style={{ width: '90%', marginBottom: '5px' }}
              />
              <button type="submit">Add Card</button>
            </form>
          </div>
        ))}

        <div style={{ backgroundColor: '#ebecf0', borderRadius: '5px', padding: '10px', width: '250px' }}>
          <form onSubmit={handleAddColumn}>
            <input
              type="text"
              placeholder="Enter column title..."
              value={newColumnTitle}
              onChange={(e) => setNewColumnTitle(e.target.value)}
              required
              style={{ width: '90%', marginBottom: '5px' }}
            />
            <button type="submit">Add Column</button>
          </form>
        </div>

      </div>
    </div>
  )
}

export default BoardDetail
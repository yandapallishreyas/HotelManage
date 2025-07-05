import React, { useState } from 'react'
import BookingForm from './components/BookingForm'
import Confirmation from './components/Confirmation'

function App() {
  const [confirmed, setConfirmed] = useState(false)
  const [details, setDetails] = useState(null)
  return (
    <div className="container mt-5">
      {confirmed
        ? <Confirmation details={details} />
        : <BookingForm setConfirmed={setConfirmed} setDetails={setDetails} />}
    </div>
  )
}

export default App

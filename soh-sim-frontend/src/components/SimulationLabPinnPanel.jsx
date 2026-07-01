import React, { useState } from 'react'
import axios from 'axios'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

const SimulationLabPinnPanel = () => {
  const [inputParams, setInputParams] = useState({})
  const [predictions, setPredictions] = useState(null)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setInputParams({ ...inputParams, [name]: value })
  }

  const handleSubmit = async () => {
    try {
      const response = await axios.post('/api/ai_sim/predict', inputParams)
      if (response.data.success) {
        setPredictions(response.data.predictions)
      }
    } catch (error) {
      console.error('Error submitting prediction:', error)
    }
  }

  return (
    <div>
      <h1>SimulationLab PINN Panel</h1>
      <form
        onSubmit={(e) => {
          e.preventDefault()
          handleSubmit()
        }}
      >
        <div>
          <label htmlFor="param1">Parameter 1:</label>
          <input type="text" id="param1" name="param1" onChange={handleInputChange} />
        </div>
        <div>
          <label htmlFor="param2">Parameter 2:</label>
          <input type="text" id="param2" name="param2" onChange={handleInputChange} />
        </div>
        {/* Add more parameters as needed */}
        <button type="submit">Submit</button>
      </form>

      {predictions && (
        <div>
          <h2>Predictions</h2>
          <LineChart width={600} height={300} data={predictions.soh}>
            <XAxis dataKey="name" />
            <YAxis />
            <CartesianGrid strokeDasharray="3 3" />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="value" stroke="#8884d8" activeDot={{ r: 8 }} />
          </LineChart>
          <LineChart width={600} height={300} data={predictions.rte}>
            <XAxis dataKey="name" />
            <YAxis />
            <CartesianGrid strokeDasharray="3 3" />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="value" stroke="#82ca9d" activeDot={{ r: 8 }} />
          </LineChart>
        </div>
      )}
    </div>
  )
}

export default SimulationLabPinnPanel

import './App.css'
import { useEffect, useState } from 'react'
import { useRef } from 'react'

function App() {
  const [campaigns, setCampaigns] = useState([])
  const fileInputRef = useRef(null)

  useEffect(() => {
    fetch('http://127.0.0.1:8000/campaigns')
      .then(response => response.json())
      .then(data => {
      console.log("CAMPAIGN DATA:", data)
      setCampaigns(data.campaigns)
    })
  }, [])

  const [selectedCampaignId, setSelectedCampaignId] = useState("")

  const handleCampaignChange = (event) => {
    setSelectedCampaignId(event.target.value)
  }

  const [file, setFile] = useState(null)

  const handleFileChange = (event) => {
    setFile(event.target.files[0])
  }

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file to upload.")
      return
    }

    if (!selectedCampaignId) {
      alert("Please select a campaign.")
      return
    }

    const formData = new FormData()
    formData.append("file", file)
    formData.append("campaign_id", selectedCampaignId)

    try {
      const response = await fetch('http://127.0.0.1:8000/contacts/upload', {
        method: 'POST',
        body: formData,
      })

      if (response.ok) {
        alert("File uploaded successfully.")
      } else {
        const errorData = await response.json()
        alert(`Error uploading file: ${errorData.detail}`)
      }
    } catch (error) {
      console.error("Error uploading file:", error)
      alert("An error occurred while uploading the file.")
    }
  }

  return (
    <>
      <div>
        <h1>Your Voice</h1>
      </div>
      <nav>
        <ul type="none">
          <li><a href="/">Home</a></li>
          <li><a href="/analytics">Analytics</a></li>
        </ul>
      </nav>
        
      <select>
          <option value="">Select Campaign</option>
          {campaigns.map((campaign) => (
            <option key={campaign.id} value={campaign.id}>
              {campaign.name}
            </option>
          ))}
      </select>

      <input
        ref={fileInputRef}
        type="file"
        accept=".csv,.xlsx"
        onChange={handleFileChange}
        style={{ display: "none" }}
      />

      <button onClick={() => fileInputRef.current.click()}>
        Upload Contacts
      </button>
    </>
  )
}

export default App
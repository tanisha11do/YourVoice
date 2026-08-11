# YourVoice – NGO Survey & Community Needs Assessment Platform

YourVoice is an AI-powered community needs assessment platform designed to help NGOs conduct surveys through automated voice calls and analyze the collected responses.

The platform allows NGO administrators to:

- Create and select campaigns
- Upload contact lists through CSV/XLSX files
- Associate contacts with a specific campaign
- Conduct AI-powered voice surveys
- Store structured call responses in Supabase
- Analyze campaign-level survey data through an analytics dashboard

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │    React Frontend   │
                    │                     │
                    │   Admin Dashboard   │
                    └──────────┬──────────┘
                               │
                               │ HTTP Requests
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │                     │
                    │     REST API        │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐         ┌─────────────────┐
        │    Supabase     │         │      CALL-E     │
        │                 │         │                 │
        │    Campaigns    │         │   AI Voice      │
        │    Contacts     │         │    Surveys      │
        │    Calls        │         │                 │
        │    Issues       │         │   Structured    │
        │                 │         │    Results      │
        └─────────────────┘         └─────────────────┘
```

---

# ✨ Features

## 👩‍💼 Admin Dashboard

The admin dashboard provides a centralized interface for NGO administrators to manage survey campaigns.

Administrators can:

- View available campaigns
- Select a campaign
- Upload contact lists
- Associate contacts with a selected campaign
- View campaign analytics

---

## 📋 Campaign Management

Campaign information is retrieved dynamically from the backend rather than being hardcoded in the frontend.

The React frontend requests campaign information from:

```http
GET /campaigns
```

The FastAPI backend retrieves the campaign information from Supabase.

Example response:

```json
{
  "campaigns": [
    {
      "id": "11440de5-e354-4582-b8c5-48b836a79e93",
      "name": "YourVoice Community Needs Assessment"
    }
  ]
}
```

The campaign `id` is used internally while the campaign `name` is displayed to the administrator.

---

# 📞 Contact Upload

Administrators can upload contact lists for a selected campaign.

Supported formats:

- CSV
- XLSX

Example CSV:

```csv
name,phone
Rahul Sharma,+919876543210
Priya Das,+919876543211
Amit Kumar,+919876543212
```

The selected campaign ID and uploaded file are sent to the FastAPI backend using multipart form data.

```text
POST /contacts/upload

campaign_id
file
```

The backend processes the file and stores the contacts in Supabase.

---

# 🤖 AI Voice Survey

CALL-E is used to conduct automated voice-based surveys.

The backend prepares a call payload containing:

- Survey task
- Recipient phone number
- Region
- Locale
- Result schema
- Campaign metadata

CALL-E returns a structured result from the completed conversation.

---

# 📊 Structured Survey Results

Survey responses can contain:

- Consent
- Whether the participant needs help
- Previous assistance
- Follow-up request
- Additional notes
- Identified issues
- Issue category
- Issue description
- Issue severity
- Issue duration

The structured results are stored in Supabase.

---

# 🗄️ Database

Supabase is used as the primary database.

The current database structure consists of:

```text
campaigns
    │
    ├───────────────┐
    │               │
    ▼               ▼
contacts          calls
                    │
                    ▼
                  issues
```

## Campaigns

Stores survey campaigns.

Important fields:

```text
id
name
```

---

## Contacts

Stores people who need to be surveyed.

Important fields:

```text
id
campaign_id
name
phone
```

Each contact belongs to a campaign through `campaign_id`.

---

## Calls

Stores completed CALL-E survey results.

Important fields include:

```text
id
calle_call_id
campaign_id
phone
consent
needs_help
previous_assistance
follow_up_requested
additional_notes
status
```

Duplicate CALL-E results are prevented using the `calle_call_id`.

---

## Issues

Stores individual issues identified during completed calls.

Important fields include:

```text
id
call_id
category
description
severity
duration
```

Each issue is associated with a completed call using `call_id`.

---

# 🔄 Contact Upload Flow

```text
                    Admin
                      │
                      │ Select Campaign
                      ▼
               React Frontend
                      │
                      │ campaign_id
                      │
                      │ Select CSV/XLSX
                      ▼
                 File State
                      │
                      │ Click Upload
                      ▼
                  FormData
                 ┌───────────────┐
                 │ campaign_id   │
                 │ file          │
                 └───────┬───────┘
                         │
                         ▼
                     FastAPI
                         │
                         ▼
          upload_contacts_to_supabase()
                         │
                         ▼
                  Supabase
                         │
                         ▼
                    contacts
```

---

# 🔄 Campaign Retrieval Flow

```text
React Frontend
      │
      │ GET /campaigns
      ▼
FastAPI
      │
      │ Query campaigns table
      ▼
Supabase
      │
      │ campaigns
      ▼
FastAPI
      │
      │ JSON response
      ▼
React
      │
      │ setCampaigns()
      ▼
Campaign Dropdown
```

The frontend does not hardcode campaign names.

Instead:

```text
Supabase
   ↓
FastAPI
   ↓
React state
   ↓
<select>
   ↓
Campaign name displayed
```

---

# 🌐 Frontend

The frontend is built using:

- React
- Vite
- JavaScript
- CSS
- Fetch API

The React application communicates with FastAPI using HTTP requests.

Example:

```javascript
fetch("http://127.0.0.1:8000/campaigns")
```

Campaigns returned by FastAPI are stored in React state.

Example:

```javascript
const [campaigns, setCampaigns] = useState([])
```

The selected campaign is stored separately:

```javascript
const [selectedCampaignId, setSelectedCampaignId] = useState("")
```

The selected contact file is stored in:

```javascript
const [file, setFile] = useState(null)
```

---

# 🧩 React Data Flow

The campaign selection follows this flow:

```text
Campaign API
     ↓
campaigns state
     ↓
campaigns.map()
     ↓
<select>
     ↓
Admin selects campaign
     ↓
handleCampaignChange()
     ↓
selectedCampaignId
```

The file selection follows:

```text
Choose Contact File
        ↓
Browser File Picker
        ↓
handleFileChange()
        ↓
file state
```

The upload follows:

```text
selectedCampaignId
        +
file
        ↓
FormData
        ↓
POST /contacts/upload
        ↓
FastAPI
        ↓
Supabase
```

---

# 🔧 Backend

The backend is built using **FastAPI**.

## API Endpoints

### Get Campaigns

```http
GET /campaigns
```

Returns the campaigns available in Supabase.

Example:

```json
{
  "campaigns": [
    {
      "id": "11440de5-e354-4582-b8c5-48b836a79e93",
      "name": "YourVoice Community Needs Assessment"
    }
  ]
}
```

---

### Upload Contacts

```http
POST /contacts/upload
```

Accepts multipart form data containing:

```text
campaign_id
file
```

The file can be a CSV or XLSX contact list.

---

# 🤖 CALL-E Integration

The backend contains a CALL-E client responsible for creating and retrieving voice calls.

The call payload contains:

```text
task
recipient
result_schema
metadata
```

The recipient information contains:

```text
phone
region
locale
```

Campaign information is included in metadata so that calls can be associated with the appropriate campaign.

---

# 💾 Saving Completed Calls

When a CALL-E call is completed, the structured result is extracted and stored in Supabase.

The application checks whether the CALL-E call has already been stored using:

```text
calle_call_id
```

If the call already exists, the application avoids inserting it again.

This prevents duplicate survey records.

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

Example:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_PUBLISHABLE_KEY=your_supabase_publishable_key
CALLE_API_KEY=your_calle_api_key
```

Do **not** commit `.env` to GitHub.

Add the following to `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
node_modules/
*.pyc
```

---

# 📁 Project Structure

```text
YourVoice/
│
├── app/
│   │
│   ├── api.py
│   ├── calle_client.py
│   ├── config.py
│   ├── prompts.py
│   ├── schemas.py
│   │
│   ├── supabase/
│   │   └── supabase_client.py
│   │
│   └── frontend/
│       │
│       ├── package.json
│       ├── vite.config.js
│       │
│       └── src/
│           ├── App.jsx
│           ├── App.css
│           ├── main.jsx
│           └── index.css
│
├── tests/
│   └── test_supabase.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone <your-repository-url>
cd YourVoice
```

---

## 2. Create a Python virtual environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

---

## 3. Install backend dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install frontend dependencies

Navigate to the React application:

```bash
cd app/frontend
```

Install the dependencies:

```bash
npm install
```

---

# ▶️ Running the Application

The backend and frontend should be run separately.

## Start FastAPI

From the project root:

```bash
python -m uvicorn app.api:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Start React

Open another terminal.

Navigate to:

```bash
cd app/frontend
```

Run:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

# 🔗 CORS Configuration

During local development, React and FastAPI run on different origins:

```text
Frontend:
http://localhost:5173

Backend:
http://127.0.0.1:8000
```

FastAPI therefore needs CORS middleware configured to allow the React frontend to make requests.

Example development configuration:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

For production, the allowed origins should be restricted to the actual deployed frontend domain.

---

# 🧪 Testing

Run the backend tests using:

```bash
pytest
```

The project currently contains tests covering Supabase-related functionality.

---

# 📈 Analytics

The analytics dashboard is designed to provide campaign-level insights from collected survey responses.

Planned metrics include:

- Total contacts
- Total calls
- Completed calls
- Calls requiring assistance
- Follow-up requests
- Issues identified
- Issues by category
- Issues by severity
- Campaign response rate

Example conceptual dashboard:

```text
┌────────────────────────────────────────────────────┐
│ Campaign Analytics                                 │
├────────────┬────────────┬────────────┬────────────┤
│ Contacts   │ Calls      │ Need Help  │ Follow-ups │
│    500     │    420     │    180     │     95     │
└────────────┴────────────┴────────────┴────────────┘

              Issues by Category

        Education       ███████████
        Healthcare      ████████
        Employment      ██████
        Housing        █████
```

The analytics will be based on actual campaign data from Supabase rather than hardcoded values.

---

# 🔒 Security Considerations

The current project is being developed as a prototype.

Before production deployment, the following should be implemented:

- Admin authentication
- Authorization
- Role-based access control
- Secure API endpoints
- Input validation
- File validation
- File size limits
- Phone number validation
- Duplicate contact handling
- Secure secret management
- Production CORS configuration
- Supabase Row Level Security policies

Sensitive credentials such as API keys must never be committed to the repository.

---

# 📌 Current Development Status

## Completed

- [x] Project structure
- [x] FastAPI backend
- [x] Supabase connection
- [x] Campaign database integration
- [x] Campaign retrieval API
- [x] React frontend setup
- [x] React → FastAPI communication
- [x] CORS configuration
- [x] Dynamic campaign dropdown
- [x] Campaign selection state
- [x] CSV file selection
- [x] XLSX file support
- [x] Contact upload API
- [x] Contact storage in Supabase
- [x] CALL-E client integration
- [x] Structured CALL-E result processing
- [x] Duplicate CALL-E call protection
- [x] Basic Supabase tests

## In Progress

- [ ] Complete admin dashboard UI
- [ ] Campaign creation UI
- [ ] Contact upload UI refinement
- [ ] Analytics API
- [ ] Analytics dashboard
- [ ] Charts and visualizations
- [ ] Authentication
- [ ] Authorization
- [ ] Production deployment

---

# 🔮 Future Improvements

## Campaign Management

- Create campaigns from the admin dashboard
- Edit campaigns
- Archive campaigns
- View campaign history

## Contact Management

- Validate uploaded contacts
- Detect duplicate phone numbers
- Preview files before upload
- Show invalid rows
- Download an error report
- Support larger contact lists

## Calling

- Start calls from the dashboard
- Track call progress
- Retry failed calls
- Display completed and pending calls
- Monitor campaign progress

## Analytics

- Real-time campaign statistics
- Interactive charts
- Issue category analysis
- Severity distribution
- Follow-up analysis
- Campaign comparison
- Export reports

## AI Insights

- Automatic campaign summaries
- Identify recurring community issues
- Detect emerging trends
- Generate actionable recommendations
- Summarize qualitative responses

## Security

- Admin login
- Role-based permissions
- Audit logs
- Secure production deployment

---

# 🎯 Project Goal

YourVoice aims to reduce the operational burden on NGOs conducting community surveys by combining:

```text
AI Voice Agents
       +
Structured Data Collection
       +
Campaign Management
       +
Centralized Database
       +
Analytics
       ↓
Actionable Community Insights
```

The goal is to transform large-scale voice-based conversations into structured information that NGOs can use to understand community needs and make better-informed decisions.

---

# 👩‍💻 Development

YourVoice is currently under active development.

The architecture is intentionally modular so that the following components can evolve independently:

```text
React
  ↓
FastAPI
  ↓
Service Logic
  ↓
Supabase / CALL-E
```

This makes it possible to expand the platform from a prototype into a production-ready NGO survey and community intelligence platform.
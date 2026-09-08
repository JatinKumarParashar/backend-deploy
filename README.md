# Spotify Governed AI Memory Engine  (https://spotify-ai-memory-j4tu.onrender.com)

A FastAPI backend for a personalized Spotify-style listening experience. The service accepts natural-language listening requests, extracts context such as activity, mood, artist, podcast topic, and exclusions, stores user-controlled memory in SQLite, and returns recommendations from Spotify when credentials are configured.

The frontend can be built with React and communicates with this service over HTTP.

## Contributors
1. Jatin Kumar
2. Aryan Gupta
3. B. Harsha Sai
## Features

- OTP-based demo registration and user login
- Natural-language personalized music and podcast requests
- User memory for artist, mood, activity, podcast topic, and exclusions
- Explicit memory editing, pausing, personalization controls, export, and purge
- Temporal graph facts stored in SQLite for memory provenance and corrections
- Spotify Web API search with a deterministic fallback when credentials are absent
- Interactive OpenAPI documentation through FastAPI Swagger UI
- CORS enabled for browser-based React clients

## Architecture

```text
React client or other HTTP client
                |
                v
        FastAPI application
          backend/main.py
                |
       +--------+---------+
       |                  |
       v                  v
 SQLite profile,     Spotify Web API
 history, graph     or local fallback
       |
       v
 Personalized response with tracks,
 context, memory state, and latency
```

## Request Workflow

1. The React client sends a request containing a `user_id` and natural-language `message` to `POST /ai/personalized-chat`.
2. The API loads the user's current profile and control flags from SQLite.
3. The intent resolver identifies activity, mood, artist or genre, podcast topic, and excluded genres using the request text.
4. If personalization is enabled, the service combines the request with the user's saved preferences.
5. Unless memory is paused, the service updates the active profile, history, and temporal graph facts.
6. The service searches Spotify using configured credentials. Without credentials, it returns a Spotify search URL as a fallback.
7. The response includes the generated explanation, recommended tracks, resolved context, memory controls, and retrieval latency.

## Project Structure

```text
backend-deploy/
|
|-- backend/
|   |-- main.py          FastAPI app, routes, intent resolution, Spotify search
|   |-- database.py      Reusable SQLite memory and chat-history helpers
|   |-- embeddings.py    Sentence-transformer embedding helper
|   |-- vector_db.py     ChromaDB persistence and similarity search helper
|   |-- graph_memory.py  Optional Neo4j graph adapter
|   `-- readme.txt       Backend architecture notes
|
|-- requirements.txt     Python dependencies
|-- .env                 Local secrets and service configuration
|-- spotify_memory.db    SQLite database created or used at runtime
|-- make_spotify_memory_deck.py
|                       Presentation-generation script
|-- spotify_memory_engine_analysis*.pptx
|                       Generated presentation files
`-- README.md            Project documentation
```

The React frontend is not currently checked into this folder. It should call the API using the base URL `http://127.0.0.1:8000` during local development.

## Setup

From the project root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If the virtual environment already exists, activate it and install the requirements:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Start the API

Run this from the `backend` directory:

```powershell
cd backend
..\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload
```

The API will be available at:

- Base URL: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

Stop the development server with `Ctrl+C`.

## Environment Variables

Create a `.env` file in the project root when real Spotify or Neo4j access is required:

```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
ADMIN_SECRET_KEY=your_admin_secret
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_neo4j_password
```

Spotify credentials are optional. If they are missing or Spotify is unavailable, the API returns a fallback search result. `ADMIN_SECRET_KEY` is required for the `Admin / Developer` login role. Neo4j is optional and is used only by the standalone graph adapter.

Never commit real credentials to source control.

## API Endpoints

### Authentication

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/auth/send-otp` | Generate a demo OTP for an email or phone identifier |
| `POST` | `/auth/register` | Register a user with the generated OTP |
| `POST` | `/auth/login` | Log in a user or admin/developer |

### Memory and Privacy

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/memory/{user_id}` | Read the active memory profile |
| `GET` | `/memory/graph/{user_id}` | Read active temporal graph facts |
| `POST` | `/memory/update-field` | Manually update an allowed profile field |
| `POST` | `/memory/toggle-control` | Pause memory or enable/disable personalization |
| `GET` | `/memory/export/{user_id}` | Export profile, graph facts, and history |
| `POST` | `/memory/purge/{user_id}` | Delete the user's memory, history, and graph facts |

### AI and Spotify

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/ai/personalized-chat` | Resolve a listening request and return recommendations |
| `GET` | `/ai/retrieve-ranked-memory` | Return recent ranked memory documents |
| `GET` | `/spotify/search` | Search for tracks directly |
| `GET` | `/mcp/tools` | Return the available memory-tool manifest |

## React Integration

Set the API base URL in the React application:

```javascript
const API_BASE_URL = "http://127.0.0.1:8000";

const response = await fetch(`${API_BASE_URL}/ai/personalized-chat`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    user_id: "user_42",
    message: "Give me something for a coding session without rap"
  })
});

const data = await response.json();
```

The response contains `ai_dj_response`, `recommended_tracks`, `context_package`, `retrieval_latency_ms`, `memory_paused`, and `personalization_enabled`.

## Example Requests

Send an OTP:

```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:8000/auth/send-otp `
  -ContentType "application/json" `
  -Body '{"phone_or_email":"demo@example.com"}'
```

Ask for personalized recommendations:

```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:8000/ai/personalized-chat `
  -ContentType "application/json" `
  -Body '{"user_id":"user_42","message":"music for a workout without metal"}'
```

## Data and Privacy Notes

- The API creates `spotify_memory.db` in the process working directory.
- Memory is saved only when `memory_paused` is false.
- Personalization can be disabled independently from memory collection.
- `/memory/export/{user_id}` supports subject-access style exports.
- `/memory/purge/{user_id}` removes the profile, history, and temporal graph records for a user.
- This is a demo authentication flow. OTPs are returned as `demo_otp`; production use requires a real delivery provider, secure authentication, authorization, validation, and secret management.

## Troubleshooting

### `No module named uvicorn`

Activate the project virtual environment and install the requirements:

```powershell
..\.venv\Scripts\Activate.ps1
python -m pip install -r ..\requirements.txt
```

### Spotify results are fallback results

Add valid Spotify credentials to `.env` and restart Uvicorn. The API intentionally falls back to a Spotify search URL when credentials are missing or the Spotify request fails.

### Port 8000 is already in use

Start on another port:

```powershell
python -m uvicorn main:app --reload --port 8001
```

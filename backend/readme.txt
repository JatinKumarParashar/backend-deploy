                 USER
                   │
                   ▼
          ┌─────────────────┐
          │   Streamlit UI  │
          │  frontend/app.py│
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │     FastAPI     │
          │   backend/      │
          │    main.py      │
          └────────┬────────┘
                   │
             ┌─────┴─────┐
             ▼           ▼
       Structured      Memory
          Data        Processing
             │           │
             ▼           ▼
       database.py   embeddings.py
                         │
                         ▼
                    vector_db.py
                         │
                         ▼
                    ChromaDB
                         │
                         │
              ┌──────────┘
              ▼
       graph_memory.py
              │
              ▼
         Knowledge
           Graph
              │
              ▼
       Relevant Memories
              │
              ▼
           Gemini
              │
              ▼
    Personalized Response
              │
              ▼
          Streamlit
              │
              ▼
             USER



             #architecture


             spotify-ai/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── embeddings.py
│   ├── vector_db.py
│   └── graph_memory.py
│
├── frontend/
│   ├── app.py
│   ├── pages/
│   │   ├── home.py
│   │   ├── chat.py
│   │   ├── memories.py
│   │   ├── recommendations.py
│   │   ├── privacy.py
│   │   └── developer_dashboard.py
│   │
│   └── components/
│       ├── sidebar.py
│       ├── memory_card.py
│       ├── recommendation_card.py
│       └── chat_box.py
│
├── memory_pipeline/
│   ├── __init__.py
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── authentication.py
│   │   └── authorization.py
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   └── ingestion.py
│   │
│   ├── extraction/
│   │   ├── __init__.py
│   │   └── memory_extraction.py
│   │
│   ├── retrieval/
│   │   ├── __init__.py
│   │   └── memory_retrieval.py
│   │
│   ├── recommendation/
│   │   ├── __init__.py
│   │   └── recommendation_engine.py
│   │
│   └── context/
│       ├── __init__.py
│       └── context_composer.py
│
├── mcp/
│   ├── search_memory.py
│   ├── add_explicit_preference.py
│   ├── correct_memory.py
│   ├── delete_memory.py
│   └── explain_memory_use.py
│
├── data/
│   └── .gitkeep
│
├── chroma_db_data/
│
├── tests/
│   ├── test_api.py
│   ├── test_memory.py
│   ├── test_embeddings.py
│   └── test_recommendation.py
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── docker-compose.yml
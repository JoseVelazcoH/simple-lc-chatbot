# LangChain Chatbot

A simple chatbot built with LangChain and Streamlit with conversational memory.

## Setup

1. **Install dependencies**
   ```bash
   uv sync
   ```

2. **Configure environment**

   Create a `.env` file in the project root:
   ```python
   GROQ_API_KEY=your_api_key_here
   ```

3. **Run the application**
   ```bash
   uv run streamlit run streamlit_app.py
   ```

The chatbot will be available at `http://localhost:8501`

## Features

- Conversational memory using LangGraph
- Message history with token-based trimming
- Web interface built with Streamlit

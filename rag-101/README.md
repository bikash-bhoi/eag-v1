# RAG-101: IPL Match Analysis System

This project implements a Retrieval-Augmented Generation (RAG) system for analyzing IPL cricket match data. The system uses a combination of document processing, vector search, and language models to provide insights about IPL matches. Data Source : https://www.iplt20.com/news/match-reports

## Setup

1. Install dependencies:

    `uv add beautifulsoup4 tqdm Pillow markitdown`

2. Refresh Indexes with new data:

    `uv run mcp_server_ipl.py`

3. Run Agent

    `uv run agent.py`
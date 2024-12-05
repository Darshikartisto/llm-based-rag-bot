# LLM-based RAG Search with Gemini and Serper

## Overview

This project implements a **Retrieval-Augmented Generation (RAG)** search system that combines the power of **Gemini** (a language model) and **Serper** (a web scraping tool) to provide accurate and relevant answers. The system scrapes data from the top 5 search results on the web, combines them, and uses **Gemini** to generate the best possible response.

### Features:
- **Streamlit Interface**: Easy-to-use input for entering queries.
- **Serper Web Scraping**: Scrapes the top 5 search results to gather relevant information.
- **Gemini LLM**: Combines the scraped data and generates a well-structured response.
- **Loading Spinner**: A loading animation appears while fetching results.
- **Error Handling**: Graceful error handling for connection issues or invalid queries.

## Requirements

To run the project, you'll need the following Python libraries:

- `streamlit`
- `requests`
- `serper` (for web scraping)
- `gemini` (for the language model)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/llm-rag-search.git
   cd llm-rag-search


https://github.com/user-attachments/assets/b2a23c17-9fb6-4a48-a745-c56f6691d67a


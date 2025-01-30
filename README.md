# AI Knowledge Navigator 🧭

## Overview

AI Knowledge Navigator is an intelligent news aggregation and analysis system that provides daily tech news digests with AI-powered insights. The system leverages AI models through the Hugging Face Inference API to fetch, process, and analyze tech news articles, generating summaries and deriving key insights across different technology domains.

## Features

- **News Aggregation**: Fetches latest tech news from four reliable sources:
    - TechCrunch (https://techcrunch.com/)
    - Ars Technica (https://arstechnica.com/)
    - MIT Technology Review (https://www.technologyreview.com/)
    - AI News (https://www.artificialintelligence-news.com/)
- **AI-Powered Processing**:
    - Generates concise, factual summaries using Facebook's BART model
    - Extracts key insights using Google's Gemma model
- **Categorization**: Automatically categorizes articles into relevant tech domains:
    - AI & Machine Learning 🤖
    - Business 💼
    - Cybersecurity 🔒
    - Innovation 🔬
    - General Tech 💻
- **Interactive Web Interface**: Clean, intuitive Streamlit-based dashboard for news exploration

## Tech Stack

- **Backend**: Python
- **Web Framework**: Streamlit
- **Database**: SQLite
- **AI Models**:
    - facebook/bart-large-cnn (for summaries)
    - google/gemma-2-2b-it (for insights)
- **Key Libraries**:
    - feedparser (RSS feed parsing)
    - huggingface_hub (AI model integration)
    - beautifulsoup4 (content cleaning)
    - python-dotenv (configuration management)

## Requirements

- Python 3.7 or higher
- Anaconda or virtualenv (for environment management)
- Required Python packages (see `requirements.txt`)

## Project Structure

```
knowledge_navigator/
├── app/
│   ├── __init__.py
│   ├── streamlit_app.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── processor.py
│   │   └── aggregator.py
│   └── database/
│       ├── __init__.py
│       └── models.py
├── run.py
└── requirements.txt

```

## Setup

1. **Clone the Repository**:
    
    ```bash
    git clone <https://github.com/yourusername/knowledge_navigator.git>
    cd knowledge_navigator
    
    ```
    
2. **Create a Virtual Environment** (optional but recommended):
    
    ```bash
    conda create -n knowledge_navigator python=3.8
    conda activate knowledge_navigator
    
    ```
    
    Or, if using virtualenv:
    
    ```bash
    python -m venv knowledge_navigator
    source knowledge_navigator/bin/activate  # On macOS/Linux
    knowledge_navigator\\Scripts\\activate  # On Windows
    
    ```
    
3. **Install Required Packages**:
    
    ```bash
    pip install -r requirements.txt
    
    ```
    
4. **Set Up Environment Variables**:
    - `HUGGINGFACE_API_KEY`: Your Hugging Face API key (required for accessing AI models)
    - Create a `.env` file in the root directory of the project and add your API keys and database URL:
    
    ```
    # API Keys
    HUGGINGFACE_API_KEY=your_huggingface_api_key
    
    # Database
    DATABASE_URL=sqlite:///./knowledge_navigator.db
    ```
    

## Usage

1. **Run the Application**
    
    ```bash
    python run.py
    
    ```
    
2. **Launch the Streamlit web interface:**
    
    ```bash
    streamlit run app/streamlit_app.py
    
    ```
    
3. **Access the dashboard at** `http://localhost:8501`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
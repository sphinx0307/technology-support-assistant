# Technology Support Assistant

A local, document-grounded conversational assistant that uses Retrieval-Augmented Generation (RAG) to answer technology questions from a supplied document collection.

The system indexes text documents, retrieves relevant passages with semantic vector search, and uses a locally running Mistral model through Ollama to generate an answer based on the retrieved context.

## Features

- Ingests `.txt` files from a document folder.
- Splits documents into overlapping chunks using `RecursiveCharacterTextSplitter`.
- Generates embeddings with Ollama's `nomic-embed-text` model.
- Stores and searches embeddings with FAISS.
- Retrieves the top five relevant chunks for each question.
- Uses Mistral through Ollama to generate a context-grounded response.
- Keeps an in-memory conversation history for follow-up questions.
- Uses a fallback response when the assistant says the documents do not contain enough information.

## Architecture

```text
Documents/*.txt
      |
      v
ingest.py: load and split documents
      |
      v
Ollama nomic-embed-text embeddings
      |
      v
FAISS vector index
      |
      v
chatbot.py: retrieve top-k relevant chunks
      |
      v
Mistral via Ollama + conversation history
      |
      v
Grounded response
```

See [`docs/architecture-explanation.pdf`](docs/architecture-explanation.pdf) for the architecture explanation and [`docs/sample-conversation.txt`](docs/sample-conversation.txt) for an example session.

## Technology stack

- Python
- LangChain document loaders, text splitters, and FAISS integration
- FAISS CPU
- Ollama
- `nomic-embed-text` for embeddings
- Mistral for response generation

## Repository structure

```text
technology-support-assistant/
├── chatbot.py
├── ingest.py
├── requirements.txt
├── README.md
├── .gitignore
├── Documents/
│   ├── api_development.txt
│   ├── fastapi_guide.txt
│   ├── git_guide.txt
│   ├── machine_learning_intro.txt
│   └── The_Python_Tutorial.txt
└── docs/
    ├── architecture-explanation.pdf
    └── sample-conversation.txt
```

The FAISS index is generated locally by `ingest.py` and is not included in this repository. This avoids committing generated binary artifacts and the pickle-based metadata file. Rebuild the index from the documents before starting the chatbot.

## Prerequisites

- Python 3.10 or later
- [Ollama](https://ollama.com/) installed and running
- The `mistral` and `nomic-embed-text` Ollama models downloaded

Pull the required models:

```bash
ollama pull mistral
ollama pull nomic-embed-text
```

## Setup

Create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the assistant

**Important:** The original `ingest.py` contains a machine-specific Windows path in `DOC_FOLDER`. Before running it on your machine, update that path to the location of this repository's `Documents` folder. The source scripts are preserved as provided during repository preparation.

Then run:

```bash
python ingest.py
python chatbot.py
```

Enter technology-related questions at the prompt. Type `exit` to quit.

Example questions:

- `What is Python?`
- `What is FastAPI?`
- `Does FastAPI support async operation?`
- `What does Git do?`
- `Who won FIFA World Cup 2022?`

The last question is outside the document scope and is intended to demonstrate the fallback response.

## Limitations

- The conversation history is stored in memory and resets when the program exits.
- The current ingestion script uses a hard-coded local folder path that must be updated on another machine.
- The response is only as reliable as the retrieved passages and model behavior; a prompt instruction alone cannot guarantee that hallucinations are eliminated.
- The chatbot does not currently display source-document citations alongside answers.
- Model downloads and inference require local storage and compute resources.

## Data and attribution

The text files in `Documents/` are part of the supplied project materials and are described in the original project notes as educational and technical resources. Before redistributing them publicly, verify the original sources' licenses and attribution requirements. If redistribution is not permitted, remove those text files from the public repository and document how users can obtain authorized copies.

## License

No license has been added. Add a license only after confirming that you have the right to license all material included in the repository.

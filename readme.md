# Secure Notes Server

A FastAPI project for managing secure notes.

## Requirements

- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/)

## Setup

1. **Clone the repository:**
  ```bash
  git clone https://github.com/your-username/secure-notes-server.git
  cd secure-notes-server
  ```

2. **Create a virtual environment:**
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```

3. **Install dependencies:**
  ```bash
  pip install -r requirements.txt
  ```

## Running the FastAPI Server

```bash
uvicorn main:app


```devenv
fastapi dev main.py

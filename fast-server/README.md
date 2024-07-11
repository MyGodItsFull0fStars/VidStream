# FastAPI Server

## Installation

Create Anaconda Python environment:

```bash
conda create -n myenv python=3.11
```

Activate environment:

```bash
conda activate myenv
```

Install FastAPI and Uvicorn:

```bash
pip install fastapi uvicorn
```

Start FastAPI server:

```bash
uvicorn main:app --reload
```
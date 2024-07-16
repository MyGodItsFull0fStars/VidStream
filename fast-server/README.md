# FastAPI Server

## Installation

### Anaconda Python Environment

Install Anaconda or [Miniconda](https://docs.anaconda.com/miniconda/).

### Create Python Environment

Create Anaconda Python environment:

```bash
conda create -n server python=3.11
```

Activate environment:

```bash
conda activate server
```

Install Pydantic for data models:

```bash
conda install pydantic -c conda-forge
```

Install FastAPI and Uvicorn:

```bash
pip install fastapi uvicorn yt-dlp pytest
```

Start FastAPI server:

```bash
fastapi dev main.py

# or

uvicorn main:app --reload
```

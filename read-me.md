# RAG Application Setup Guide

This guide provides instructions for setting up, configuring, and running the Agent Development Kit (ADK) RAG application locally.

## 🛠️ Setup & Installation

### 1. Create a Virtual Environment
Create a new Python virtual environment to isolate project dependencies:

```bash
python -m venv .venv
```

> **Note for Ubuntu/Debian users:** If the command above fails, you may need to install the `venv` package for your specific Python version first:
> ```bash
> sudo apt update
> sudo apt install python3.12-venv
> python3 -m venv .venv
> ```

### 2. Activate the Environment

**On macOS / Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```bash
.venv\Scripts\activate
```

### 3. Install Dependencies
With the virtual environment active, install the required packages:

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

Before running the application, you need to define your RAG corpus source. 

Create a `.env` file in the root directory of the project and add the following variable:
```env
RAG_CORPUS="your_corpus_value_here"
```

## 🚀 Running the Application

Start the ADK web server bound to all network interfaces on port 8000:

```bash
adk web . --host 0.0.0.0 --port 8000
```

---

## 🧪 RAG Test Questions

Use the following sample questions to evaluate the Retrieval-Augmented Generation (RAG) capabilities. 

**Reference Document:** [RAG Testing Google Doc](https://docs.google.com/document/d/1JpcOajfhXXaKjkhWfgnMAGOfSWVqiTlkTmx-0M4gfn4/edit?tab=t.0)

| Question | Expected Answer |
| :--- | :--- |
| What is the capital of India? | New Delhi |
| Which river is known as the "Ganga" in India? | The Ganges River |
| What is the national animal of India? | The Royal Bengal Tiger |
| What is the national bird of India? | The Indian Peafowl |
| What is the national flower of India? | The Lotus |
| Which is the largest state in India by area? | Rajasthan |
| Which is the smallest state in India by area? | Goa |
| What is the national tree of India? | The Banyan Tree |
| What is the national sport of India? | Field Hockey |
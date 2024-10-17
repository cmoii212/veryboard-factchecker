# VeriBoard: An Automated Fact-Checking Application

VeriBoard is an automated fact-checking application that leverages advanced Natural Language Processing (NLP) models and techniques to verify factual claims. It identifies claims within text, gathers evidence from various sources, analyzes relationships using NLP models, and presents the verification results to the user.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Usage](#usage)
  - [1. Start the Backend Server](#1.-start-the-backend-server)
  - [2. Serve the Frontend](#2.-serve-the-frontend)
- [File Explanations](#file-explanations)
- [Technologies Used](#technologies-used)
- [Acknowledgments](#acknowledgments)
- [Disclaimer](#Disclaimer)

---

## Project Overview

VeriBoard automates the fact-checking process by:

- **Identifying Claims**: Detects factual claims within input text.
- **Gathering Evidence**: Retrieves evidence from web searches and knowledge graphs.
- **Analyzing Relationships**: Uses NLP models to assess the relationship between claims and evidence.
- **Verifying Claims**: Classifies claims as "Supported," "Refuted," or "Not Enough Information."
- **Presenting Results**: Displays the verification results and evidence sources to the user.

---

## Features

- **User-Friendly Interface**: Intuitive frontend design for easy interaction.
- **Advanced NLP Models**: Incorporates state-of-the-art models for claim detection and verification.
- **Evidence Retrieval**: Utilizes web search APIs and knowledge graphs to gather supporting evidence.
- **Transparency**: Provides evidence links used in the verification process.
- **Evaluation Script**: Includes a script to evaluate the application's performance using the LIAR dataset.

---

## Project Structure

VeriBoard/
├── backend/
│   ├── app.py
│   ├── evaluate_app.py
│   ├── requirements.txt
│   ├── models/
│   │   ├── \_\_init\_\_.py
│   │   ├── ensemble_claim_detection_model.py
│   │   ├── advanced_claim_verification_model.py
│   │   ├── multi_hop_reasoning_model.py
│   │   └── question_answering_model.py
│   ├── utils/
│   │   ├── \_\_init\_\_.py
│   │   ├── text_retrieval.py
│   │   ├── text_preprocessing.py
│   │   ├── evidence_retrieval.py
│   │   ├── relevance_filtering.py
│   │   ├── similarity.py
│   │   └── knowledge_graph.py
│   └── data/
│       └── liar_dataset.tsv
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── index.js
│   └── img/
│       ├── logo.png
│       └── user.png
└── README.md

---

## Installation

### Prerequisites

- **Python 3.7 or higher**
- **Node.js and npm** (optional, if using additional frontend tooling)
- **Virtual Environment Tool**: `venv` or `conda`
- **Git** (optional, for cloning the repository)

### Backend Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/VeriBoard.git
cd VeriBoard/backend
```

#### 2. Create a Python Virtal Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```
#### 4. Set Up Environment Variables

In the .env file in the backend folder.

```bash
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_google_cse_id
```

#### 5. Download spacy Model
```bash
python -m spacy download en_core_web_sm
```

## Usage

### 1. Start the Backend Server

```bash
cd veryboard/backend
python app.py
```

The backend server will start on http://localhost:5000.

### 2. Serve the Frontend

You can serve the frontend using a simple HTTP server.

```bash
cd ../frontend
python -m http.server 8000
```

Or, launch ```the index.html``` directly with a web brownser.

## File Explanations

### app.py
- The main Flask application that handles incoming requests, processes claims, retrieves evidence, performs verification, and returns results to the frontend.
### evaluate_app.py
- A script to evaluate the application's performance using the LIAR dataset.
- Processes each claim in the dataset, compares predicted labels with ground truth, and computes evaluation metrics.
### requirements.txt
- Lists all the Python dependencies required for the backend application.
### models/
- Contains the implementations of various NLP models used in the application.

    - ensemble_claim_detection_model.py: Detects factual claims in the input text.
    - advanced_claim_verification_model.py: Verifies claims against evidence and classifies them.
    - multi_hop_reasoning_model.py: Performs multi-hop reasoning over multiple evidence sources.
    - question_answering_model.py: Extracts answers from evidence passages using QA models.
    - \_\_init\_\_.py: Indicates that models is a Python package.
### utils/
- Contains utility functions for text processing, evidence retrieval, and other supporting tasks.

    - text_retrieval.py: Functions to retrieve text content from URLs.
    - text_preprocessing.py: Preprocesses text by cleaning and splitting into sentences.
    - evidence_retrieval.py: Retrieves evidence using web search APIs.
    - relevance_filtering.py: Filters relevant evidence passages.
    - similarity.py: Calculates similarity scores between texts.
    - knowledge_graph.py: Queries knowledge graphs (e.g., Wikidata) for additional evidence.
    - \_\_init\_\_.py: Indicates that utils is a Python package.
### data/
- Contains the dataset used for evaluation.

    - liar_dataset.tsv: The LIAR dataset file containing labeled claims.

## Technologies Used
- Python 3: Programming language used for the backend.
- Flask: Web framework for building the backend API.
- Spacy: NLP library for text processing.
- Transformers (Hugging Face): Library for state-of-the-art NLP models.
- Google Custom Search API: For retrieving web search results as evidence.
- Wikidata SPARQL Endpoint: For querying knowledge graphs.
- HTML5, CSS3, JavaScript: Technologies used for building the frontend.
- Material Icons: Icon library used in the frontend design.

## Acknowledgments

- LIAR Dataset: A benchmark dataset for fake news detection.
- Hugging Face: Providing access to numerous NLP models.
- Spacy: For powerful text preprocessing capabilities.
- Google: For the Custom Search API used in evidence retrieval.
- Wikidata: For the SPARQL endpoint used in querying knowledge graphs.

## Disclaimer

This application is for educational and research purposes during the workshop event of EPSI Paris 2024/2025.
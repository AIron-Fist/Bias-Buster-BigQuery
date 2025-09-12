# Bias-Buster-BigQuery

## Overview

The Bias Intelligence Dashboard is a Python application built with Gradio that leverages Google Cloud’s BigQuery and Gemini models to analyze news articles for various forms of bias. It provides a user-friendly interface to explore topics, view a summary of biases, and visualize sentiment and bias scores.

## Impact and Innovation

- **Promoting Digital Literacy**  
  Empowers users to become more critical consumers of news by exposing framing, selection, and other biases in media coverage.

- **Objective Analysis**  
  Automates bias detection with the Gemini model, providing a consistent framework across multiple articles to reveal coverage patterns that manual review might miss.

- **Data-Driven Insights**  
  Uses BigQuery to handle large news-article datasets efficiently and offers forecasting and visualizations of bias trends and sentiment distributions.

## Prerequisites

Before running this application, you need:

- **Google Cloud Project** with billing enabled  
- **BigQuery API** enabled in your Google Cloud Project  
- **Vertex AI API** enabled in your Google Cloud Project  
- **Service Account** with roles:  
  - BigQuery Data Editor  
  - BigQuery Job User  
  - BigQuery Read Session User  
  - Vertex AI User  
- **Python 3.8+** and libraries listed in `requirements.txt`

## Setup Instructions

### Google Cloud Setup

1. **Create a BigQuery Dataset**  
   In your Google Cloud project, create a dataset named `bias_buster_dataset`.

2. **Create a BigQuery Table**  
   Within `bias_buster_dataset`, create a table named `news_articles_placeholder` with columns:  
   - `title` (STRING)  
   - `author` (STRING)  
   - `published` (DATETIME)  
   - `sentiment` (STRING)  
   - `topics` (ARRAY<STRING>)  
   - `text` (STRING)

3. **Create a Gemini Model**  
   In BigQuery, run:

   ```sql
   CREATE OR REPLACE MODEL `bias_buster_dataset.gemini_flash_model`
   REMOTE WITH CONNECTION `us-central1.YOUR_CONNECTION_ID`
   OPTIONS(
     endpoint = 'gemini-1.5-flash-preview-0514'
   );
   ```

   Replace `YOUR_CONNECTION_ID` with your BigQuery-Vertex AI connection ID.

### Local Environment Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-org/Bias-Buster-BigQuery.git
   cd Bias-Buster-BigQuery
   ```

2. **Set Credentials**

   On Linux/macOS:

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
   ```

   On Windows (Command Prompt):

   ```cmd
   set GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\keyfile.json"
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Launch the dashboard:

```bash
python app.py
```

The terminal will display a local URL (e.g., `http://127.0.0.1:7860`)—open it in your browser to access the Bias Intelligence Dashboard.

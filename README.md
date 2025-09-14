# Bias Intelligence Dashboard  
## See Beyond the Story: Bias Under the Lens. Powered by BigQuery & Gemini

---

## Overview

The Bias Intelligence Dashboard is a Gradio-based Python application that leverages Google Cloud’s BigQuery and Gemini LLM to analyze news articles for various forms of bias. Users can explore topics, review bias summaries, and visualize sentiment and bias scores in an interactive dashboard.

---

## Impact and Innovation

- **Promoting Digital Literacy**  
  Exposes framing, selection, and other biases to empower critical news consumption.

- **Objective Analysis**  
  Uses Gemini LLM (`ML.GENERATE_TEXT`) for consistent, automated bias detection across hundreds of articles.

- **Data-Driven Insights**  
  Scales with BigQuery and BigFrames to forecast bias trends and visualize sentiment distributions.

---

## Data Flow

1. **Data Ingestion**  
   - Download Webhose news snapshots locally via Python.  
   - Upload consolidated JSONL to Google Cloud Storage.

2. **Data Processing & Analysis**  
   1. BigQuery Load Job imports JSONL into  
      `bias_buster_dataset.news_articles_placeholder`.  
   2. SQL scripts flatten & clean nested fields.  
   3. `ML.GENERATE_TEXT` (Gemini) extracts nine bias categories & scores.  
   4. BigFrames forecasts bias-score trends over time.

3. **UI & Visualization**  
   - Gradio frontend queries BigQuery for bias scores, forecasts, and excerpts.  
   - Interactive charts and drill-downs enable exploration.

---

## Metrics

- **Time-to-Insight**  
  Reduced manual review from ~2 hours to ~12 seconds for a 10-article batch.

- **Discovery Rate of Nuanced Bias (DRNB)**  
  ```text
  DRNB = (# subtle-bias flags by tool)
         ÷ (human-annotated subtle-bias flags)
  ```  
  100 % improvement vs. manual on a 200-article ground truth set.

- **User Engagement**  
  Future “Session Depth” will track average detail-view clicks per dashboard session.

---

## Prerequisites

- Google Cloud project **bias-buster-471818** with billing enabled  
- BigQuery API enabled  
- Vertex AI API enabled  
- Service account JSON key with roles:  
  - BigQuery Data Editor  
  - BigQuery Job User  
  - BigQuery Read Session User  
  - Vertex AI User  
- Python 3.8+ and the libraries in `requirements.txt`  
- `git`, Google Cloud SDK, and `gsutil` installed locally

---

## Setup Instructions

### 1. Google Cloud Setup

1. **Create BigQuery dataset**  
   ```bash
   bq mk --dataset bias-buster-471818:bias_buster_dataset
   ```

2. **Create Gemini model**  
   In the BigQuery editor, run:
   ```sql
   CREATE OR REPLACE MODEL `bias_buster_dataset.gemini_flash_model`
   REMOTE WITH CONNECTION `us-central1.YOUR_CONNECTION_ID`
   OPTIONS (
     endpoint = 'gemini-1.5-flash-preview-0514'
   );
   ```
   Replace `YOUR_CONNECTION_ID` with your BigQuery–Vertex AI connection ID.

---

### 2. Data Acquisition & Loading

#### Step 1: Download the Data

1. Visit the Webhose free-news repo:  
   https://github.com/Webhose/free-news-datasets  
2. Download a snapshot (e.g., “Crime, Law and Justice”) as ZIP.

#### Step 2: Consolidate & Upload to GCS

1. Unzip into `News_Datasets/`.  
2. Merge JSON files into one JSONL:
   ```python
   import json, glob

   data = []
   for path in glob.glob("News_Datasets/*.json"):
       with open(path) as f:
           data.extend(json.load(f))

   with open("consolidated_articles.json", "w") as out:
       for rec in data:
           out.write(json.dumps(rec) + "\n")
   ```
3. Upload to GCS:
   ```bash
   gsutil cp consolidated_articles.json \
     gs://your-gcs-bucket-name/consolidated_articles.json
   ```

#### Step 3: Load into BigQuery

```bash
bq load \
  --autodetect \
  --source_format=NEWLINE_DELIMITED_JSON \
  bias_buster_dataset.news_articles_placeholder \
  gs://your-gcs-bucket-name/consolidated_articles.json
```

---

### 3. Local Environment Setup

1. **Clone the repo**  
   ```bash
   git clone https://github.com/your-org/Bias-Buster-BigQuery.git
   cd Bias-Buster-BigQuery
   ```

2. **Set environment variables**  
   - **Linux/macOS**  
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
     export GOOGLE_CLOUD_PROJECT="bias-buster-471818"
     export BIGFRAMES_LOCATION="us-central1"
     ```
   - **Windows (PowerShell)**  
     ```powershell
     $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\service-account.json"
     $env:GOOGLE_CLOUD_PROJECT        = "bias-buster-471818"
     $env:BIGFRAMES_LOCATION          = "us-central1"
     ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

 ```

---

## 4. Running the Application

```bash
python app.py
```

Open the URL printed in your terminal (e.g., `http://127.0.0.1:7860`) to access the Bias Intelligence Dashboard.  
```bash
# Example:
# Running on local URL:  http://127.0.0.1:7860
```
```

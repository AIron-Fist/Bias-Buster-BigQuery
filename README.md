# Bias Intelligence Dashboard  
See Beyond the Story: Bias Under the Lens. Powered by BigQuery & Gemini

An interactive notebook that uses Google Cloud’s BigQuery and the Gemini LLM to analyze news articles for various forms of bias. Explore topics, get automated bias summaries, and view interactive visualizations of sentiment and bias-score forecasts.

---

## Impact and Innovation

- Promoting Digital Literacy: Identifies framing, selection, and other biases to help users critically evaluate news.  
- Objective Analysis: Leverages Gemini via BigQuery’s `ML.GENERATE_TEXT` for consistent, automated bias detection.  
- Data-Driven Insights: Scales with BigQuery and BigFrames to forecast bias trends and visualize sentiment distributions.  

---

## Prerequisites

- Google Cloud project **bias-buster-471818** with billing enabled  
- BigQuery API and Vertex AI API enabled  
- Service account JSON key with roles:  
  - BigQuery Data Editor  
  - BigQuery Job User  
  - BigQuery Read Session User  
  - Vertex AI User  
- Python 3.8+ and Git installed  
- Google Cloud SDK (`gcloud`, `bq`, `gsutil`)  
- Python libraries from `requirements.txt`  

---

## 1. Google Cloud Setup

### 1.1 Create BigQuery Dataset  
```bash
bq --location=us-central1 mk \
  --dataset bias-buster-471818:bias_buster_dataset
```

### 1.2 Create Remote Gemini Model  
In BigQuery console, run (replace `YOUR_CONN` with your connection ID, e.g. `bias_buster`):  
```sql
CREATE OR REPLACE MODEL
  `bias-buster-471818.bias_buster_dataset.gemini_flash_model`
REMOTE WITH CONNECTION
  `us-central1.YOUR_CONN`
OPTIONS (
  endpoint = 'gemini-2.0-flash-001'
);
```

---

## 2. Data Acquisition & Loading

### 2.1 Download & Merge  
1. Download the ZIP from Webhose:  
   https://github.com/Webhose/free-news-datasets/blob/master/News_Datasets/Crime%2C%20Law%20and%20Justice_negative_20250511073514.zip  
2. Unzip into `News_Datasets/` locally.  
3. Merge all JSON files into one JSONL via a small Python script:  
   ```python
   import glob, json

   with open('consolidated_articles.jsonl', 'w') as out:
       for path in glob.glob('News_Datasets/*.json'):
           for record in json.load(open(path)):
               out.write(json.dumps(record) + '\n')
   ```

### 2.2 Upload to GCS  
```bash
gsutil cp consolidated_articles.jsonl gs://YOUR_BUCKET/
```

### 2.3 Load into BigQuery  
```bash
bq --location=us-central1 load \
  --project_id=bias-buster-471818 \
  --autodetect \
  --source_format=NEWLINE_DELIMITED_JSON \
  bias_buster_dataset.news_articles_placeholder \
  gs://YOUR_BUCKET/consolidated_articles.jsonl
```

---

## 3. Local Environment Setup

```bash
git clone https://github.com/AIron-Fist/Bias-Buster-BigQuery.git
cd Bias-Buster-BigQuery
pip install -r requirements.txt
```

Set the service-account key environment variable:

- macOS / Linux  
  ```bash
  export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
  ```
- Windows (cmd)  
  ```cmd
  set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\key.json
  ```

---

## 4. Running the Dashboard Notebook

1. In your project directory, start Jupyter:  
   ```bash
   python -m notebook
   ```
2. In the browser file explorer, open **Bias_Buster_BigQuery.ipynb**.  
3. Run all cells to launch the Gradio dashboard interface.  
4. Copy the local URL (e.g., http://127.0.0.1:8888) into your browser to interact with the Bias Intelligence Dashboard.

---

You’re ready to explore media bias with real-world news data, powered end-to-end by BigQuery, Gemini, and BigFrames.

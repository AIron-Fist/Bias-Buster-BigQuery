### Bias Intelligence Dashboard

See Beyond the Story: Bias Under the Lens. Powered by BigQuery & Gemini

The Bias Intelligence Dashboard is an interactive tool that uses Google Cloud's BigQuery and the Gemini LLM to analyze news articles for various forms of bias. Users can explore different topics, get a summary of identified biases, and view interactive visualizations of sentiment and bias scores.

-----

### Impact and Innovation

  * **Promoting Digital Literacy:** The dashboard identifies framing, selection, and other biases to help users critically evaluate news.
  * **Objective Analysis:** It uses the Gemini LLM (via BigQuery's `ML.GENERATE_TEXT` function) to provide consistent and automated bias detection across many articles.
  * **Data-Driven Insights:** The system scales with BigQuery and BigFrames to forecast bias trends and visualize sentiment distribution in the data.

-----

### Prerequisites

  * **Google Cloud Project**: A Google Cloud project with billing enabled, specifically `bias-buster-471818`.
  * **APIs**: Both the **BigQuery API** and **Vertex AI API** must be enabled.
  * **Service Account**: A JSON key file for a service account with the following IAM roles:
      * BigQuery Data Editor
      * BigQuery Job User
      * BigQuery Read Session User
      * Vertex AI User
  * **Software**:
      * Python 3.8+
      * The libraries listed in `requirements.txt`
      * `git`
      * Google Cloud SDK and `gsutil`

-----

### Setup Instructions

#### 1\. Google Cloud Setup

  * **Create BigQuery Dataset**: Use the `bq` command-line tool to create the dataset for the project.
    ```bash
    bq mk --dataset bias-buster-471818:bias_buster_dataset
    ```
  * **Create Gemini Model**: Open the BigQuery editor and run the following SQL command. Be sure to replace `YOUR_CONNECTION_ID` with your BigQuery–Vertex AI connection ID.
    ```sql
    CREATE OR REPLACE MODEL `bias_buster_dataset.gemini_flash_model`
    REMOTE WITH CONNECTION `us-central1.YOUR_CONNECTION_ID`
    OPTIONS (
      endpoint = 'gemini-1.5-flash-preview-0514'
    );
    ```

#### 2\. Data Acquisition & Loading

  * **Download Data**: Visit the Webhose free-news repo to download a news snapshot (e.g., “Crime, Law and Justice”) as a ZIP file.

  * **Consolidate & Upload**:

      * Unzip the files into a directory like `News_Datasets/`.
      * Run a Python script to merge the individual JSON files into a single `JSONL` file.
      * Upload the consolidated `JSONL` file to a Google Cloud Storage (GCS) bucket.

  * **Load into BigQuery**: Load the `JSONL` file from GCS into the `news_articles_placeholder` table.

    ```bash
    bq load \
      --autodetect \
      --source_format=NEWLINE_DELIMITED_JSON \
      bias_buster_dataset.news_articles_placeholder \
      gs://your-gcs-bucket-name/consolidated_articles.json
    ```

#### 3\. Local Environment Setup

  * **Clone Repository**: Clone the project repository and change into the directory.
    ```bash
    git clone https://github.com/AIron-Fist/Bias-Buster-BigQuery.git
    cd Bias-Buster-BigQuery
    ```
  * **Install Dependencies**: Install the required Python libraries using `pip`.
    ```bash
    pip install -r requirements.txt
    ```

#### 4\. Running the Dashboard

To run the dashboard, you must execute the provided Jupyter Notebook.

  * Start a Jupyter server in your project directory:
    ```bash
    python -m notebook
    ```
  * Open the `Bias_Buster_BigQuery.ipynb` file in your web browser from the Jupyter file explorer.
  * Execute the cell within the notebook to launch the Gradio dashboard.

The dashboard will provide a URL (e.g., `http://127.0.0.1:7860`) that you can open in your browser to start using the tool.

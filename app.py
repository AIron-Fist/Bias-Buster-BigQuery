import gradio as gr
import pandas as pd
import plotly.express as px
from google.cloud import bigquery

# 🔑 BigQuery Setup
project_id = "bias-buster-471818"
dataset_id = "bias_buster_dataset"
source_table = "news_articles_placeholder"
client = bigquery.Client(project=project_id)

# 🧠 Run Generative AI SQL on Selected Article
def run_bias_analysis(article_id):
    query = f"""
    SELECT
      uuid,
      title,
      author,
      published,
      sentiment,
      AI.GENERATE_INT(
        STRUCT(
          CONCAT("Rate the political bias of this article from -10 (liberal) to +10 (conservative): ", text) AS prompt
        ),
        connection_id => "projects/{project_id}/locations/us-central1/connections/bias_buster",
        endpoint => "gemini-2.5-pro"
      ) AS bias_score,
      AI.GENERATE(
        STRUCT(
          CONCAT("Explain the political bias in this article. Include tone, framing, and language choices. Article: ", text) AS prompt
        ),
        connection_id => "projects/{project_id}/locations/us-central1/connections/bias_buster",
        endpoint => "gemini-2.5-pro"
      ) AS bias_explanation
    FROM `{project_id}.{dataset_id}.{source_table}`
    WHERE uuid = '{article_id}'
    LIMIT 1
    """
    result_df = client.query(query).to_dataframe()
    if result_df.empty:
        return "No article found.", None, None

    row = result_df.iloc[0]
    explanation = row['bias_explanation'].get('result') if isinstance(row['bias_explanation'], dict) else str(row['bias_explanation'])
    score = row['bias_score'].get('result') if isinstance(row['bias_score'], dict) else row['bias_score']
    return f"📰 **{row['title']}**\n\n✍️ Author: {row['author']}\n📅 Published: {row['published']}\n📉 Bias Score: {score}", explanation, score

# 📊 Load Article Options
def get_article_options():
    query = f"""
    SELECT uuid, title
    FROM `{project_id}.{dataset_id}.{source_table}`
    WHERE LENGTH(text) > 300
    ORDER BY published DESC
    LIMIT 50
    """
    df = client.query(query).to_dataframe()
    return {f"{row['title'][:80]}...": row['uuid'] for _, row in df.iterrows()}

# 🎛️ Gradio UI
with gr.Blocks(title="Bias Intelligence Dashboard") as demo:
    gr.Markdown("## 🧠 Bias Intelligence Dashboard")
    gr.Markdown("Select an article to run live bias analysis using BigQuery’s Generative AI SQL.")

    article_selector = gr.Dropdown(label="🗂 Choose Article", choices=[], interactive=True)
    refresh_button = gr.Button("🔄 Refresh Articles")
    run_button = gr.Button("🚀 Run Bias Analysis")

    bias_summary = gr.Markdown()
    bias_explanation = gr.Textbox(label="🧠 Bias Explanation", lines=10)
    bias_score_plot = gr.Plot(label="📉 Bias Score")

    def refresh_articles():
        return get_article_options()

    def run_analysis(selected_uuid):
        summary, explanation, score = run_bias_analysis(selected_uuid)
        fig = px.bar(x=["Bias Score"], y=[score], range_y=[-10, 10], color=["Bias Score"], color_discrete_sequence=["salmon"])
        fig.update_layout(title="Bias Score", yaxis_title="Score", height=300)
        return summary, explanation, fig

    refresh_button.click(fn=refresh_articles, outputs=article_selector)
    run_button.click(fn=run_analysis, inputs=article_selector, outputs=[bias_summary, bias_explanation, bias_score_plot])

demo.launch()

# CORD-19 Metadata Analysis

This repository contains a Jupyter notebook and a Streamlit app for basic analysis of the CORD-19 `metadata.csv` file.

Files:
- `CORD19_Analysis.ipynb`: Notebook with step-by-step analysis and visualizations suitable for Colab.
- `streamlit_app.py`: Lightweight Streamlit app to explore the cleaned metadata interactively.
- `requirements.txt`: Python dependencies.

Quickstart (local):

1. Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Download `metadata.csv` (put it in the repository root). A small sample is available in the repo notebook via wget.

4. Run the Streamlit app:

```bash
streamlit run streamlit_app.py
```

Quickstart (Google Colab):

- Open `CORD19_Analysis.ipynb` in Colab.
- Install packages in a cell using `!pip install -r requirements.txt` or the explicit pip installs.
- Download `metadata.csv` inside Colab using `!wget -O metadata.csv <sample-or-kaggle-url>`.
- For running Streamlit in Colab, use a tunnelling service (e.g., `ngrok`) — there are many guides online. The notebook is designed primarily for exploration; Streamlit works best locally.

Notes:
- The notebook uses a small sample metadata file by default (sample-metadata.csv). If you use the full Kaggle `metadata.csv`, expect longer processing times.
- If you need help configuring Kaggle API access to download the official dataset, ask and I can add step-by-step instructions.

Enjoy exploring the CORD-19 metadata!
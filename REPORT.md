# Student Performance Analyzer — Detailed Project Report

**Group:** 07  
**Date:** May 25, 2026  

## 1) Project overview
This project predicts a student’s **grade category** (A, B, C, D, Fail) using demographic, behavioral, and academic features. The workflow covers data exploration, preprocessing, model training/evaluation, and simple deployment interfaces (Flask + Gradio).

## 2) Repository structure
- `student_performance_classification.ipynb` — End‑to‑end ML workflow (EDA → preprocessing → modeling → evaluation → deployment).
- `student_performance_grade.csv` — Classification dataset (target: `Grade`).
- `app.py` — Flask inference API using a saved model pipeline.
- `app_flask.py` — Flask API using a saved model + preprocessor pair.
- `generate_presentation.py` — PowerPoint generation script (uses EDA/evaluation images).
- `requirements.txt` — Python dependencies.

## 3) Data summary
- **Target:** `Grade` (A, B, C, D, Fail)
- **Features:** numeric, ordinal, nominal, and binary columns (study habits, attendance, GPA, etc.).
- **Imbalance:** majority classes (A/B) dominate; D/Fail are rare.

## 4) Workflow summary (Notebook)
### Step 1 — Data loading & initial exploration
- Loads `student_performance_grade.csv` and inspects shape, dtypes, missing values, and class distribution.

### Step 2 — Exploratory Data Analysis (EDA)
- Class distribution plots
- Numerical distributions
- Correlation heatmap
- Categorical count plots
- Grade vs key numeric features

### Step 3 — Preprocessing
- **Numerical:** median imputation + standard scaling
- **Ordinal:** `OrdinalEncoder` with explicit order
- **Nominal:** `OneHotEncoder` (drop first)
- **Binary:** ordinal encode (No/Yes)
- Stratified train/test split
- SMOTE used in specific pipelines to reduce class imbalance

### Step 4 — Modeling
- Baseline models: Logistic Regression, KNN, Random Forest, Gradient Boosting (CV weighted F1)
- Tuned Random Forest using `GridSearchCV`
- Imbalance strategy comparison (no SMOTE vs SMOTE vs class‑weighted)
- LightGBM & XGBoost baselines (clean reporting)
- Feature pruning experiment (drop lowest‑importance original features)

### Step 5 — Evaluation
- Classification report
- Confusion matrix
- Feature importance plot

### Step 6 — Deployment
- Model pipeline is serialized to `model_classification.pkl`
- Flask endpoints for JSON prediction requests

## 5) Recent results (summary)
- Overall **accuracy ~0.73**, **weighted F1 ~0.73** on the test set
- Minority classes (D/Fail) have low recall due to heavy imbalance
- LightGBM & XGBoost are similar to tuned RF (baseline performance)

> Note: exact values will vary by random seed, split, and training conditions.

## 6) Deployment interfaces
### Flask API (`app.py`)
- Loads `model_classification.pkl`
- `/predict` endpoint accepts JSON payload and returns:
  - `predicted_grade`
  - `grade_probabilities`

### Flask API (`app_flask.py`)
- Loads `model_classification.pkl` + `preprocessor_classification.pkl`
- Manually maps binary values and transforms inputs before inference

## 7) Presentation generation
- `generate_presentation.py` compiles a PPTX summary using saved EDA/evaluation images:
  - `eda_grade_dist.png`
  - `eda_num_distributions.png`
  - `eda_correlation_heatmap.png`
  - `eval_clf_confusion_matrix.png`
  - `eval_clf_feature_importance.png`

## 8) How to run
### 1) Environment setup
- Create and activate a venv (already supported in this repo)
- Install dependencies:
  - `pip install -r requirements.txt`

### 2) Run the notebook
- Open `student_performance_classification.ipynb`
- Execute steps sequentially (1 → 6)

### 3) Run Flask API
- `python app.py`
- POST JSON to `http://127.0.0.1:5000/predict`

### 4) Generate presentation
- `python generate_presentation.py`
- Output: `Student_Performance_Presentation_Group_07.pptx`

## 9) Known limitations & next steps
- Severe class imbalance causes low recall for D/Fail
- Improve minority performance via:
  - more data for rare classes
  - cost‑sensitive learning or stronger reweighting
  - class aggregation (e.g., D+Fail)
- Calibrate probabilities for better interpretability

---
**End of report**

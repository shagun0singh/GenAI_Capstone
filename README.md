# Property Price Prediction: Machine Learning Project

This project implements a robust machine learning pipeline to predict property prices using **Random Forest Regression**. It features a comprehensive data preprocessing workflow and an interactive **Streamlit** web application for real-time valuations.

## 📌 Problem Definition
Real estate pricing is driven by dynamic factors like location, size, and property type. This project frames property price prediction as a **regression task**, aiming to provide automated, data-driven valuations to eliminate human bias and improve efficiency.

## 📊 Dataset Overview
The model is trained on a dataset of property listings with the following characteristics:
- **Total Clean Observations**: 417,561
- **Features Selected**: 9 (Physical, Geographical, and Categorical)
- **Target Variable**: `saleEstimate_currentPrice` (Continuous numeric)

### Feature Categories:
- **Physical**: Bedrooms, bathrooms, floor area (sqm), living rooms.
- **Geographical**: Latitude, longitude.
- **Categorical**: Tenure (Freehold/Leasehold), Property Type (Flat, Detached, Semi-Detached, Terraced).

## ⚙️ Methodology & Preprocessing
A rigorous preprocessing pipeline was implemented to ensure data quality:
1.  **Missing Data**: Handled using **Median** (numeric) and **Mode** (categorical) imputation.
2.  **Feature Engineering**: Simplified property types and tenures to reduce cardinality and prevent overfitting.
3.  **Categorical Encoding**: Applied **One-Hot Encoding** for model compatibility.
4.  **Target Transformation**: Applied **Log Transformation** (`np.log`) to the target price to normalize the right-skewed distribution.
5.  **Scaling**: Used `StandardScaler` to ensure all features contribute equally to the model.

## 🤖 Model selection & Performance
A **Random Forest Regressor** was chosen for its ability to capture non-linear relationships and its robustness against overfitting.

### Configuration:
- `n_estimators`: 20
- `max_depth`: 15
- `n_jobs`: -1 (Parallel processing)

### Evaluation Results:
| Metric | Value | Description |
| :--- | :--- | :--- |
| **R² Score** | **0.9291** | Explains ~93% of price variance |
| **RMSE** | **0.1718** | ~8-9% average error margin |
| **MAE** | **0.1133** | Minimal absolute error magnitude |

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Download Dataset
Download the [Kaggle House Price Data](https://www.kaggle.com/datasets/jakewright/house-price-data) and place the CSV file in the `data/` folder.

### 3. Train the Model
```bash
python train_model.py
```

### 4. Run the Web App
```bash
streamlit run app.py
```

## 👥 Team Contributions
- **Shagun Singh**: Data Cleaning, Preprocessing, and Feature Engineering.
- **Pratyaksha Shastri**: Model Selection, Hyperparameter Tuning, and Training.
- **Shiva Sharma**: Model Evaluation, Performance Analysis, and Reporting.
- **Yogesh Mishra**: Web App Development (Streamlit), Model Deployment, and Optimization.

---
*Developed as part of the **Generative AI** course at **Newton School of Technology**.*

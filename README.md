# Ho Chi Minh City Planning and Real Estate Data Modeling & Analysis Project

This project builds a complete process (End-to-End Data Science Pipeline) from raw data collection, cleaning, imputation, exploratory analysis (EDA) to building a prediction/classification model related to the Real Estate market in Ho Chi Minh City combining Urban Planning information.

## 📁 Process Flow & Project Structure

The implementation process is divided into stages corresponding to the Jupyter Notebook files below. You should run them in order to ensure data continuity:

### Phase 1: Data Collection (Data Crawling)

*`bds_crawler.ipynb`: Use **Selenium**and **undiscovered-chromedriver**to automate the collection of real estate information (price, area, location, amenities...) from social network news sources/real estate websites and export the raw data file `data_bds.csv`.
* `process_crawler.ipynb`: Process for processing coordinates from raw data:
    1. Read a CSV file containing standard geographic coordinates `WGS84` (Google Maps).
    2. Convert the coordinate system to **VN2000**standard (meridian axis 105°, zone 48 in Ho Chi Minh City).
    3. Call the API from the system `thongtinquyhoach.hochiminhcity.gov.vn` to extract the specific land type (residential land, industrial land, commercial land...) corresponding to each real estate.

### Phase 2: Data Preprocessing (Data Preprocessing)
*`02_0_data_cleaning.ipynb`: Explores raw data structure, unifies data formats, normalizes units of measurement, removes noise, and splits dataset into `Train` and `Test`. The results are saved in the `data_output/1_data_cleaned_train.csv` and `1_data_cleaned_test.csv` folders.
* `02_1_data_imputation_tree.ipynb`:Handling missing data (Missing Values) and encoding features (Ordinal Encoding) optimally for Tree-based models such as Random Forest, XGBoost, LightGBM. The result is saved as `2_data_preprocessed_tree_train.csv`.
* `02_2_data_imputation_linear.ipynb`: Handle deficiencies, apply categorical variable encoding (OneHot/Ordinal), normalize the digital data scale (**StandardScaler /MinMaxScaler**) and apply Log transformation (`log1p`) to the target variable to optimize Linear Models. The result is saved as `3_data_preprocessed_linear_train.csv`.

### Phase 3: Analysis & Machine Learning (EDA & Modeling)
*`EDA.ipynb`: In-depth data discovery analysis. Visualize the supply-demand relationship, volatility and standard deviation of prices in Central Districts (District 1, etc.), check multicollinearity via VIF (Variance Inflation Factor) and draw word cloud charts (WordCloud).
*`modelling.ipynb`: Test and train Machine Learning models. Use Pipeline to manage models, evaluate performance based on advanced metrics (Classification Report, ROC-AUC score, etc.).

---

## Instructions for installing and running the project

### Step 1: Install necessary libraries
Open Terminal/Command Prompt in the project's directory and run the following command to automatically install the entire environment:
```bash
pip install -r requirement.txt
```

### Step 2: Run notebooks in order
Navigate to the `notebooks/` folder and execute:
```bash
jupyter notebook notebooks/
```

Run the notebooks in the numbered order (01 → 02 → 03 → 04) to ensure data continuity through the pipeline.

### Step 3: Launch the Streamlit web app
```bash
streamlit run app/app.py
```

### Step 4 (Optional): Docker deployment
```bash
docker build -t ds108 .
docker run -p 8501:8501 ds108
```

---

## 📂 Updated Project Structure

```
DS108/
├── app/
│   ├── app.py                    # Streamlit dashboard (EDA + price prediction)
│   └── utils.py                  # Model & data loading, prediction logic
├── data/
│   ├── raw/
│   │   └── Final_Merged_2605_quyhoach.csv
│   ├── processed/                # Cleaned train/test CSVs
│   └── codebook.csv              # Variable definitions & allowed values
├── data_output/                  # Notebook output CSVs
├── models/
│   ├── model.pkl                 # Trained model
│   └── features.pkl              # Feature columns for inference
├── notebooks/
│   ├── 01_0_bds_crawler.ipynb
│   ├── 01_0_bds_crawler_clean.ipynb
│   ├── 01_1_quyhoach_crawler.ipynb
│   ├── 01_1_quyhoach_crawler_clean.ipynb
│   ├── 02_0_data_cleaning.ipynb
│   ├── 02_0_data_cleaning_executed.ipynb
│   ├── 02_1_data_imputation_tree.ipynb
│   ├── 02_2_data_imputation_linear.ipynb
│   ├── 03_eda_and_feature_selection.ipynb
│   ├── 04_modeling.ipynb
│   ├── 04_modeling_clean.ipynb
│   ├── LLM_test/                 # Experimental LLM notebooks
│   │   ├── mistral_7b.ipynb
│   │   ├── qwen_3b.ipynb
│   │   ├── qwen_7b.ipynb
│   │   └── yi_1.5_6b_chat.ipynb
│   ├── env.example               # Environment template for crawlers
│   └── data_output/              # Generated CSVs from notebooks
├── data_cleaning_pipeline.ipynb  # Standalone OOP cleaning pipeline
├── Dockerfile
├── requirement.txt
└── README.md
```

---

## 🔬 Modeling Details

The project evaluates **8 models** across two separate preprocessing pipelines:

| Model | Type | Preprocessing |
|-------|------|---------------|
| Random Forest | Tree-based | Tree pipeline (Ordinal encoding) |
| Gradient Boosting | Tree-based | Tree pipeline |
| XGBoost | Tree-based | Tree pipeline |
| LightGBM | Tree-based | Tree pipeline |
| Linear Regression | Linear | Linear pipeline (OneHot + Scaling + log1p) |
| Ridge Regression | Linear | Linear pipeline |
| Lasso Regression | Linear | Linear pipeline |
| ElasticNet | Linear | Linear pipeline |

**Target variable:** `Khoảng giá` (billions VND)

**Evaluation metrics:** R² Score, MAE, MSE, MAPE, RMSLE

---

## 📊 Web App Features

Run `streamlit run app/app.py` to open the dashboard with two tabs:

1. **Trực quan hóa EDA** (EDA Visualization)
   - District filter
   - Price distribution histogram (with KDE)
   - Scatter plot: area vs. price by land type
   - Key metrics cards (total listings, average price, unique land types)

2. **Dự báo Giá BĐS** (Price Prediction)
   - Input: area, district, land type, number of amenities
   - Output: predicted price in billions VND
   - Powered by the trained model loaded from `models/model.pkl`

---

## 🗂️ Data Codebook

Key variables from `data/codebook.csv`:

| Variable | Type | Description |
|----------|------|-------------|
| `Diện tích` | float | Land area (m²), range [1 — 990] |
| `Khoảng giá` | float | **Target** — price in billions VND |
| `Số phòng ngủ` | float | Bedrooms [1 — 100] |
| `Pháp lý` | object | Legal status: Sổ hồng / Sổ đỏ / không có |
| `Nội thất` | object | Interior: Trống / Cơ bản / Đầy đủ / Cao cấp |
| `Quan_Huyen` | object | District (24 categories) |
| `Dien_Tich_Lo` | float | Registered plot area (m²), 20.4% missing |
| `Ty_Le_Dat_O` | float | % residential planning zone, 20.6% missing |
| `Ty_Le_Giao_Thong` | float | % transport planning zone, 20.6% missing |
| `khoang_cach_trung_tam` | float | Distance to city center (km) |

---

## 📦 Dependencies

All required packages are listed in `requirement.txt`:

- **Scraping:** selenium, undetected-chromedriver, requests, beautifulsoup4
- **Data:** pandas, numpy, scipy
- **Visualization:** matplotlib, seaborn, plotly
- **ML:** scikit-learn, xgboost, lightgbm, category-encoders, statsmodels
- **App:** streamlit, joblib
- **Utilities:** tqdm, python-dotenv
- **LLM:** openai, torch, transformers
- **Notebook:** notebook, ipykernel

---

## 🔧 Environment Variables

For the crawler notebooks, copy `notebooks/env.example` to `.env`:

```bash
BASE_URL=https://batdongsan.com.vn/ban-nha-dat-tp-hcm
TARGET_SAMPLES=3500
PAGE_DELAY=2
CLOUDFLARE_TIMEOUT=30
# ... see env.example for full list
```

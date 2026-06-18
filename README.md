# DS108 — HCMC Real Estate Price Prediction

An end-to-end pipeline for collecting, cleaning, preprocessing, and modeling real estate data in Ho Chi Minh City, with the goal of classifying the price range (`Khoảng giá`) of each property.

---

## Directory Structure

```
DS108/
├── data/
│   └── raw/                          # Raw collected data
│   └── processed/                    # Processed data
├── notebook/
│   ├── 01_0_bds_crawler_clean.ipynb
│   ├── 01_1_quyhoach_crawler_clean.ipynb
│   ├── 02_0_data_cleaning.ipynb
│   ├── 02_1_data_transformation_tree.ipynb
│   ├── 02_2_data_transformation_linear.ipynb
│   ├── 03_eda_and_feature_selection.ipynb
│   └── 04_modeling.ipynb
├── data_output/                    # Output data after each step
├── requirement.txt
└── README.md
```

---

## Pipeline Execution Order

The pipeline follows a linear order, branching at the preprocessing step and converging at the model training step:

```
01_0  →  01_1  →  02_0  →┬→  02_1  →  03 (Tree branch)   →┐
                           └→  02_2  →  03 (Linear branch) →┘→  04
```

> **Note:** `03_eda_and_feature_selection.ipynb` is run **separately for each branch** (Tree and Linear), and `04_modeling.ipynb` uses outputs from both branches 02_1 and 02_2.

---

## Notebook Descriptions

### 1. Data Collection

#### `01_0_bds_crawler_clean.ipynb` — Real Estate Data Scraping
- Scrapes property listings from real estate websites.
- Preliminary cleaning of raw data: removes duplicates, standardizes formats.
- **Output:** initial cleaned raw real estate data.

#### `01_1_quyhoach_crawler_clean.ipynb` — Urban Planning Data Scraping
- Scrapes land-use planning data in HCMC (residential ratio, transport ratio, park ratio, etc.).
- Merges planning information by geographic coordinates into the real estate dataset.
- **Output:** data enriched with planning features.

---

### 2. Cleaning & Preprocessing

#### `02_0_data_cleaning.ipynb` — Data Cleaning & Feature Engineering
- Standardizes categorical variable domains (`Pháp lý`, `Nội thất`, `Hướng nhà`, etc.).
- Handles units (`Diện tích`, `Đường vào`, ...) and removes outliers.
- Feature engineering: creates `total_rooms`, `distance_to_center`, `hem_xe_hoi`, `gan_*` flags (near market, school, hospital, park).
- Splits train/test at a fixed ratio.
- **Output:** `data_output/1_data_cleaned_train.csv`, `data_output/1_data_cleaned_test.csv`

> From this point, the pipeline **splits into 2 independent branches** depending on the model type used in the next step.

---

#### Branch A — For Tree-based Models

##### `02_1_data_transformation_tree.ipynb`
- **Ordinal Encoding** for `Pháp lý` and `Nội thất` (preserves ordinal ranking).
- **Target Encoding** for address variables (`Quận/Huyện`, `Phường/Xã`, `Tên đường`) with appropriate smoothing to avoid overfitting.
- No scaling required since decision trees are insensitive to scale.
- **Output:** `data_output/2_data_preprocessed_tree_train.csv`, `data_output/2_data_preprocessed_tree_test.csv`

---

#### Branch B — For Linear-based Models

##### `02_2_data_transformation_linear.ipynb`
- **Ordinal Encoding** for `Pháp lý` and `Nội thất`.
- **Target Encoding** for address variables.
- **Log Transform + StandardScaler** for heavily right-skewed numeric features (`Diện tích`, `Đường vào`, `total_rooms`).
- **MinMaxScaler / RobustScaler** for other numeric features.
- Prepares data to meet the normality assumptions of linear models.
- **Output:** `data_output/2_data_preprocessed_linear_train.csv`, `data_output/2_data_preprocessed_linear_test.csv`

---

### 3. EDA & Feature Selection

#### `03_eda_and_feature_selection.ipynb` *(run twice, once per branch)*
- Analyzes distribution, correlation, and feature importance.
- Selects the optimal feature set for each branch (tree or linear).
- Visualizes target variable distribution (`Khoảng giá`).
- **Input:** output from `02_1` or `02_2` respectively.

---

### 4. Modeling

#### `04_modeling.ipynb` — Model Training & Evaluation
- Trains classification models for both processed branches.
- Compares results between tree-based and linear-based approaches.
- Evaluates performance using: Accuracy, F1-Score, Confusion Matrix.
- **Input:** output from step `03` of both branches.

---

## Environment Setup

```bash
pip install -r requirement.txt
```

Key libraries used in this project:

- `pandas`, `numpy` — Data processing
- `scikit-learn` — Modeling & preprocessing
- `category_encoders` — Target Encoding
- `matplotlib`, `seaborn`, `plotly` — Visualization
- `scipy`, `statsmodels` — Statistical analysis

---

## Target Variable

`Khoảng giá` — Price range classification of real estate (multi-class classification problem).

---

## Notes

- Notebooks must be run **in order** since each step depends on the output of the previous one.
- The `data_output/` directory must exist before running from `02_0` onward.
- Notebook `03` must be run **twice separately**: once pointing to the Tree branch data, once to the Linear branch data.

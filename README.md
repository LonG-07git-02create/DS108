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
pip install -r requirements.txt
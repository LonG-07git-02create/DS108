import pandas as pd
import joblib
import streamlit as st
from pathlib import Path

# =====================================
# PATH CONFIG
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "app" / "model.pkl"
FEATURE_PATH = BASE_DIR / "app" / "features.pkl"

DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "1_data_cleaned_train.csv"
)

# =====================================
# LOAD MODEL
# =====================================

@st.cache_resource
def load_model():
    try:
        return joblib.load(MODEL_PATH)

    except FileNotFoundError:
        st.error(f"❌ Không tìm thấy model:\n{MODEL_PATH}")
        return None

    except Exception as e:
        st.error(f"❌ Lỗi load model:\n{e}")
        return None


# =====================================
# LOAD FEATURE LIST
# =====================================

@st.cache_resource
def load_features():

    try:
        return joblib.load(FEATURE_PATH)

    except FileNotFoundError:
        st.error(f"❌ Không tìm thấy features:\n{FEATURE_PATH}")
        return None

    except Exception as e:
        st.error(f"❌ Lỗi load features:\n{e}")
        return None


# =====================================
# LOAD DATA FOR EDA
# =====================================

@st.cache_data
def load_data():

    try:
        return pd.read_csv(DATA_PATH)

    except FileNotFoundError:
        st.error(f"❌ Không tìm thấy data:\n{DATA_PATH}")
        return pd.DataFrame()

    except Exception as e:
        st.error(f"❌ Lỗi load data:\n{e}")
        return pd.DataFrame()


# =====================================
# PREPARE INPUT
# =====================================

def prepare_input(user_input: dict):

    feature_columns = load_features()

    if feature_columns is None:
        raise Exception(
            "Không load được features.pkl"
        )

    input_df = pd.DataFrame([user_input])

    missing_cols = [
        col
        for col in feature_columns
        if col not in input_df.columns
    ]

    if missing_cols:
        raise Exception(
            f"Thiếu feature: {missing_cols}"
        )

    input_df = input_df[feature_columns]

    return input_df


# =====================================
# PREDICT
# =====================================

def predict_price(user_input: dict):

    model = load_model()

    if model is None:
        raise Exception(
            "Model chưa được load."
        )

    input_df = prepare_input(user_input)

    prediction = model.predict(input_df)[0]

    return float(prediction)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils import (
    load_model,
    load_data,
    predict_price
)

st.set_page_config(
    page_title="BĐS & Quy hoạch TP.HCM",
    layout="wide"
)

# =========================
# LOAD ASSETS
# =========================

model = load_model()
df = load_data()

if model is None or df.empty:
    st.stop()

# =========================
# TITLE
# =========================

st.title("📊 Hệ thống Phân tích & Dự báo Bất động sản TP.HCM")
st.markdown("---")

# =========================
# SIDEBAR
# =========================

menu = st.sidebar.radio(
    "Chọn chức năng",
    [
        "📈 Trực quan hóa EDA",
        "🔮 Dự báo Giá BĐS"
    ]
)

# =====================================================
# TAB EDA
# =====================================================

if menu == "📈 Trực quan hóa EDA":

    st.header("Khám phá dữ liệu")

    if "quan" in df.columns:

        districts = ["Tất cả"] + sorted(df["quan"].dropna().unique())

        selected_district = st.selectbox(
            "Quận/Huyện",
            districts
        )

        if selected_district == "Tất cả":
            filtered_df = df
        else:
            filtered_df = df[
                df["quan"] == selected_district
            ]

    else:
        filtered_df = df

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Tổng số tin",
        f"{len(filtered_df):,}"
    )

    if "gia" in filtered_df.columns:
        col2.metric(
            "Giá trung bình",
            f"{filtered_df['gia'].mean():.2f} tỷ"
        )

    if "loai_dat" in filtered_df.columns:
        col3.metric(
            "Loại quy hoạch",
            filtered_df["loai_dat"].nunique()
        )

    st.markdown("## Phân bố giá")

    if "gia" in filtered_df.columns:

        fig, ax = plt.subplots(figsize=(10,4))

        sns.histplot(
            filtered_df["gia"],
            kde=True,
            ax=ax
        )

        st.pyplot(fig)

    st.markdown("## Giá theo diện tích")

    if (
        "dien_tich" in filtered_df.columns
        and
        "gia" in filtered_df.columns
    ):

        fig2, ax2 = plt.subplots(figsize=(10,5))

        sns.scatterplot(
            data=filtered_df,
            x="dien_tich",
            y="gia",
            hue="loai_dat"
            if "loai_dat" in filtered_df.columns
            else None,
            alpha=0.7,
            ax=ax2
        )

        st.pyplot(fig2)

# =====================================================
# TAB PREDICTION
# =====================================================

else:

    st.header("🔮 Dự báo giá bất động sản")

    col1, col2 = st.columns(2)

    with col1:

        dien_tich = st.number_input(
            "Diện tích (m²)",
            10.0,
            10000.0,
            60.0
        )

        quan = st.selectbox(
            "Quận/Huyện",
            sorted(df["quan"].dropna().unique())
            if "quan" in df.columns
            else ["Quận 1"]
        )

    with col2:

        loai_dat = st.selectbox(
            "Loại đất",
            sorted(df["loai_dat"].dropna().unique())
            if "loai_dat" in df.columns
            else ["Đất ở"]
        )

        tien_ich = st.slider(
            "Số tiện ích xung quanh",
            0,
            20,
            3
        )

    if st.button("🚀 Dự báo"):

        input_df = pd.DataFrame(
            [{
                "dien_tich": dien_tich,
                "quan": quan,
                "loai_dat": loai_dat,
                "tien_ich": tien_ich
            }]
        )

        try:

            prediction = predict_price(
                model,
                input_df
            )

            st.success("Dự báo thành công")

            st.metric(
                label="💰 Giá dự báo",
                value=f"{prediction:,.2f} tỷ VNĐ"
            )

            st.balloons()

        except Exception as e:

            st.error(str(e))
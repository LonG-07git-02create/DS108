# Dự án Phân tích & Mô hình hóa Dữ liệu Bất động sản và Quy hoạch TP.HCM

Dự án này xây dựng một quy trình trọn gói (End-to-End Data Science Pipeline) từ bước thu thập dữ liệu thô, làm sạch, xử lý khuyết thiếu (imputation), phân tích khám phá (EDA) cho đến xây dựng mô hình dự đoán/phân loại liên quan đến thị trường Bất động sản tại TP.HCM kết hợp thông tin Quy hoạch đô thị.

## 📁 Luồng Xử lý & Cấu trúc Dự án

Quy trình thực hiện được chia thành các giai đoạn tương ứng với các file Jupyter Notebook dưới đây. Bạn nên chạy theo thứ tự để đảm bảo tính liên tục của dữ liệu:

### Giai đoạn 1: Thu thập dữ liệu (Data Crawling)
* `bds_crawler.ipynb`: Sử dụng **Selenium** và **undetected-chromedriver** để tự động hóa việc thu thập thông tin bất động sản (giá, diện tích, vị trí, tiện ích...) từ các nguồn tin đăng mạng xã hội/website bất động sản và xuất ra file dữ liệu thô `data_bds.csv`.
* `quyhoach_crawler.ipynb`: Quy trình xử lý tọa độ từ dữ liệu thô:
    1. Đọc file CSV chứa tọa độ địa lý chuẩn `WGS84` (Google Maps).
    2. Chuyển đổi hệ tọa độ sang chuẩn **VN2000** (Kinh tuyến trục 105°, múi 48 tại TP.HCM).
    3. Gọi API từ hệ thống `thongtinquyhoach.hochiminhcity.gov.vn` để trích xuất loại đất cụ thể (đất ở, đất công nghiệp, đất thương mại...) tương ứng với từng bất động sản.

### Giai đoạn 2: Tiền xử lý dữ liệu (Data Preprocessing)
* `02_0_data_cleaning.ipynb`: Khám phá cấu trúc dữ liệu thô, đồng nhất định dạng dữ liệu, chuẩn hóa đơn vị đo lường, loại bỏ nhiễu và chia tập dữ liệu thành `Train` và `Test`. Kết quả được lưu tại thư mục `data_output/1_data_cleaned_train.csv` và `1_data_cleaned_test.csv`.
* `02_1_data_imputation_tree.ipynb`: Xử lý dữ liệu bị thiếu (Missing Values) và mã hóa đặc trưng (Ordinal Encoding) tối ưu cho các mô hình dạng Cây (Tree-based models như Random Forest, XGBoost, LightGBM). Kết quả lưu thành `2_data_preprocessed_tree_train.csv`.
* `02_2_data_imputation_linear.ipynb`: Xử lý khuyết thiếu, áp dụng mã hóa biến phân loại (OneHot/Ordinal), chuẩn hóa thang đo dữ liệu số (**StandardScaler / MinMaxScaler**) và áp dụng phép biến đổi Log (`log1p`) lên biến mục tiêu để tối ưu cho các mô hình Tuyến tính (Linear Models). Kết quả lưu thành `3_data_preprocessed_linear_train.csv`.

### Giai đoạn 3: Phân tích & Học máy (EDA & Modelling)
* `EDA.ipynb`: Phân tích khám phá dữ liệu chuyên sâu. Trực quan hóa mối quan hệ cung-cầu, sự biến động và độ lệch chuẩn của giá cả tại các Quận trung tâm (Quận 1, v.v.), kiểm tra đa cộng tuyến qua hệ số VIF (Variance Inflation Factor) và vẽ biểu đồ đám mây từ ngữ (WordCloud).
* `modelling.ipynb`: Thử nghiệm, huấn luyện các mô hình Machine Learning. Sử dụng Pipeline để quản lý mô hình, đánh giá hiệu năng dựa trên các chỉ số nâng cao (Classification Report, ROC-AUC score, v.v.).

---

## 🚀 Hướng dẫn cài đặt và chạy dự án

### Bước 1: Cài đặt thư viện cần thiết
Mở Terminal/Command Prompt trong thư mục của dự án và chạy lệnh sau để tự động cài đặt toàn bộ môi trường:
```bash
pip install -r requirements.txt
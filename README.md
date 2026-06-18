# DS108 — Dự báo Khoảng giá Bất động sản TP.HCM

Dự án xây dựng pipeline hoàn chỉnh để thu thập, làm sạch, tiền xử lý và mô hình hóa dữ liệu bất động sản tại TP.HCM, với mục tiêu phân loại khoảng giá (`Khoảng giá`) của từng căn nhà.

---

## Cấu trúc thư mục

```
DS108/
├── data/
│   └── raw/                          # Dữ liệu thô thu thập được
│   └── processed/                    # Dữ liệu sau xử lý
├── notebook/
│   ├── 01_0_bds_crawler_clean.ipynb
│   ├── 01_1_quyhoach_crawler_clean.ipynb
│   ├── 02_0_data_cleaning.ipynb
│   ├── 02_1_data_transformation_tree.ipynb
│   ├── 02_2_data_transformation_linear.ipynb
│   ├── 03_eda_and_feature_selection.ipynb
│   └── 04_modeling.ipynb
├── data_output/                    # Dữ liệu đầu ra sau từng bước xử lý
├── requirement.txt
└── README.md
```

---

## Thứ tự chạy Pipeline

Pipeline được tổ chức theo thứ tự tuyến tính, rẽ nhánh ở bước tiền xử lý rồi hội tụ về bước huấn luyện mô hình:

```
01_0  →  01_1  →  02_0  →┬→  02_1  →  03 (nhánh Tree)    →┐
                           └→  02_2  →  03 (nhánh Linear)  →┘→  04
```

> **Lưu ý:** File `03_eda_and_feature_selection.ipynb` được chạy **lần lượt cho từng nhánh** (Tree và Linear) và `04_modeling.ipynb` được chạy bằng output của cả hai nhánh 02_1 và 02_2.

---

## Mô tả các Notebook

### 1. Thu thập dữ liệu

#### `01_0_bds_crawler_clean.ipynb` — Thu thập dữ liệu bất động sản
- Crawl dữ liệu rao bán nhà đất từ các trang web bất động sản.
- Làm sạch sơ bộ dữ liệu thô: loại bỏ bản ghi trùng lặp, chuẩn hóa định dạng.
- **Output:** dữ liệu BĐS thô đã làm sạch ban đầu.

#### `01_1_quyhoach_crawler_clean.ipynb` — Thu thập dữ liệu quy hoạch
- Crawl dữ liệu quy hoạch sử dụng đất tại TP.HCM (tỷ lệ đất ở, đất giao thông, công viên, v.v.).
- Kết hợp thông tin quy hoạch theo tọa độ địa lý vào dữ liệu BĐS.
- **Output:** dữ liệu đã được bổ sung các đặc trưng quy hoạch.

---

### 2. Làm sạch & Tiền xử lý

#### `02_0_data_cleaning.ipynb` — Làm sạch & Kỹ thuật đặc trưng
- Chuẩn hóa miền giá trị các biến phân loại (`Pháp lý`, `Nội thất`, `Hướng nhà`, v.v.).
- Xử lý đơn vị (`Diện tích`, `Đường vào`, ...) và loại bỏ outlier.
- Kỹ thuật đặc trưng (feature engineering): tạo thêm `total_rooms`, `distance_to_center`, `hem_xe_hoi`, các cờ `gan_*` (gần chợ, trường học, bệnh viện, công viên).
- Tách train/test theo tỷ lệ cố định.
- **Output:** `data_output/1_data_cleaned_train.csv`, `data_output/1_data_cleaned_test.csv`

> Từ đây, pipeline **tách thành 2 nhánh độc lập** tùy theo loại mô hình sẽ sử dụng ở bước sau.

---

#### Nhánh A — Dành cho mô hình dựa trên Cây quyết định (Tree-based)

##### `02_1_data_transformation_tree.ipynb`
- **Ordinal Encoding** cho `Pháp lý` và `Nội thất` (giữ nguyên thứ tự thứ hạng).
- **Target Encoding** cho các biến địa chỉ (`Quận/Huyện`, `Phường/Xã`, `Tên đường`) với `smoothing` phù hợp để tránh overfitting.
- Không cần chuẩn hóa (scaling) vì cây quyết định không nhạy cảm với thang đo.
- **Output:** `data_output/2_data_preprocessed_tree_train.csv`, `data_output/2_data_preprocessed_tree_test.csv`

---

#### Nhánh B — Dành cho mô hình tuyến tính (Linear-based)

##### `02_2_data_transformation_linear.ipynb`
- **Ordinal Encoding** cho `Pháp lý` và `Nội thất`.
- **Target Encoding** cho các biến địa chỉ.
- **Log Transform + StandardScaler** cho các đặc trưng số lệch phải nặng (`Diện tích`, `Đường vào`, `total_rooms`).
- **MinMaxScaler / RobustScaler** cho các đặc trưng số khác.
- Chuẩn bị dữ liệu đáp ứng giả định phân phối chuẩn của mô hình tuyến tính.
- **Output:** `data_output/2_data_preprocessed_linear_train.csv`, `data_output/2_data_preprocessed_linear_test.csv`

---

### 3. EDA & Lựa chọn đặc trưng

#### `03_eda_and_feature_selection.ipynb` *(chạy 2 lần, mỗi lần cho 1 nhánh)*
- Phân tích phân phối, tương quan và mức độ quan trọng của đặc trưng.
- Lựa chọn tập feature phù hợp với từng nhánh (tree hoặc linear).
- Trực quan hóa phân phối biến mục tiêu (`Khoảng giá`).
- **Input:** output của `02_1` hoặc `02_2` tương ứng.

---

### 4. Mô hình hóa

#### `04_modeling.ipynb` — Huấn luyện & Đánh giá mô hình
- Huấn luyện các mô hình phân loại cho cả hai nhánh đã xử lý.
- So sánh kết quả giữa tree-based và linear-based.
- Đánh giá hiệu năng bằng các chỉ số: Accuracy, F1-Score, Confusion Matrix.
- **Input:** output của bước `03` từ cả 2 nhánh.

---

## Cài đặt môi trường

```bash
pip install -r requirement.txt
```

Các thư viện chính được sử dụng trong dự án:

- `pandas`, `numpy` — Xử lý dữ liệu
- `scikit-learn` — Mô hình hóa & tiền xử lý
- `category_encoders` — Target Encoding
- `matplotlib`, `seaborn`, `plotly` — Trực quan hóa
- `scipy`, `statsmodels` — Phân tích thống kê

---

## Biến mục tiêu

`Khoảng giá` — Phân loại khoảng giá của bất động sản (bài toán phân loại đa lớp).

---

## Lưu ý khi chạy

- Các notebook phải được chạy **theo đúng thứ tự** vì mỗi bước phụ thuộc vào output của bước trước.
- Thư mục `data_output/` phải tồn tại trước khi chạy từ `02_0` trở đi.
- Notebook `03` cần được chạy **riêng biệt hai lần**: một lần trỏ vào dữ liệu nhánh Tree, một lần trỏ vào dữ liệu nhánh Linear.

import pandas as pd, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read with default encoding
df_default = pd.read_csv('D:/DS108/notebook/data_output/2_data_preprocessed_tree_train.csv')
print(f"Default encoding columns: {list(df_default.columns)}", flush=True)
print(f"TARGET_COL in df_default: {'Khoảng giá' in df_default.columns}", flush=True)

# Read with utf-8
df_utf8 = pd.read_csv('D:/DS108/notebook/data_output/2_data_preprocessed_tree_train.csv', encoding='utf-8')
print(f"UTF-8 columns match: {list(df_default.columns) == list(df_utf8.columns)}", flush=True)
print(f"UTF-8 TARGET_COL in df_utf8: {'Khoảng giá' in df_utf8.columns}", flush=True)

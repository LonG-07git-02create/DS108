import json

with open('D:/DS108/notebook/03_eda_and_feature_selection.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

cell6 = nb['cells'][11]  # Cell 6
print(f"Cell 6 execution_count: {cell6.get('execution_count')}")
print(f"Cell 6 outputs count: {len(cell6.get('outputs', []))}")
for i, out in enumerate(cell6.get('outputs', [])):
    print(f"  Output {i} type: {out.get('output_type')}")
    if 'data' in out:
        for k in out['data']:
            val = out['data'][k]
            if isinstance(val, str) and len(val) > 100:
                print(f"    {k}: {val[:100]}... (len={len(val)})")
            else:
                print(f"    {k}: {str(val)[:100]}")

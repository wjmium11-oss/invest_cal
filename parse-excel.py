import zipfile
import xml.etree.ElementTree as ET
import json
import re
import sys
import os

excel_path = "./건강기능식품DB.xlsx"
out_json_path = "./nutrition-search.json"

if not os.path.exists(excel_path):
    print(f"Error: {excel_path} file not found in the current directory.")
    sys.exit(1)

def clean_float(val):
    if val is None:
        return 0.0
    val_str = str(val).strip()
    if not val_str or val_str == "None" or val_str == "해당없음":
        return 0.0
    try:
        return float(val_str)
    except ValueError:
        # Try to find a numeric part
        m = re.search(r"[-+]?\d*\.\d+|\d+", val_str)
        if m:
            return float(m.group(0))
        return 0.0

def parse_times(val):
    if val is None:
        return 1
    val_str = str(val).strip()
    if not val_str or val_str == "None" or val_str == "해당없음":
        return 1
    m = re.search(r"\d+", val_str)
    if m:
        n = int(m.group(0))
        return n if n >= 1 else 1
    return 1

print("Parsing XLSX...")
try:
    with zipfile.ZipFile(excel_path) as z:
        # 1. Load shared strings
        shared_strings = []
        if "xl/sharedStrings.xml" in z.namelist():
            print("Reading shared strings...")
            xml_content = z.read("xl/sharedStrings.xml")
            root = ET.fromstring(xml_content)
            # Namespace
            ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
            for t in root.findall(f".//{ns}t"):
                shared_strings.append(t.text if t.text is not None else "")
        print(f"Loaded {len(shared_strings)} shared strings.")

        # 2. Parse sheet1.xml
        print("Reading sheet1.xml...")
        xml_content = z.read("xl/worksheets/sheet1.xml")
        root = ET.fromstring(xml_content)
        ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
        
        rows = []
        for row in root.findall(f".//{ns}row"):
            row_data = {}
            for cell in row.findall(f"{ns}c"):
                r_attr = cell.get("r")
                if not r_attr:
                    continue
                # Extract column letter part
                col_letter = re.match(r"([A-Z]+)", r_attr).group(1)
                col_idx = 0
                for char in col_letter:
                    col_idx = col_idx * 26 + (ord(char) - ord('A') + 1)
                col_idx -= 1
                
                val_el = cell.find(f"{ns}v")
                val = val_el.text if val_el is not None else None
                t = cell.get("t")
                if t == "s" and val is not None:
                    val = shared_strings[int(val)]
                row_data[col_idx] = val
            rows.append(row_data)
except Exception as e:
    print("Error during zip/xml parsing:", e)
    sys.exit(1)

print(f"Read {len(rows)} raw rows.")

if not rows:
    print("No rows found in sheet1.")
    sys.exit(1)

# Extract headers from the first row
header_row = rows[0]
headers = []
max_col = max(header_row.keys()) if header_row else 0
for i in range(max_col + 1):
    headers.append(header_row.get(i))

# Find column indexes for needed attributes
cols_map = {
    "name": "식품명",
    "times": "1일섭취횟수",
    "ca": "칼슘(mg)",
    "fe": "철(mg)",
    "vitA": "비타민A(μg RAE)",
    "b1": "티아민(mg)",
    "b2": "리보플라빈(mg)",
    "b6": "비타민 B6 / 피리독신(mg)",
    "b12": "비타민 B12(μg)",
    "folate": "엽산(μg DFE)",
    "niacin": "니아신(mg)",
    "vitC": "비타민 C(mg)",
    "vitD": "비타민 D(μg)",
    "vitE": "비타민 E(mg α-TE)",
    "vitK2": "비타민 K2(μg)",
    "omega3": "EPA와 DHA의 합(mg)",
    "mg": "마그네슘(mg)",
    "zn": "아연(mg)",
    "se": "셀레늄(μg)",
    "cu": "구리(μg)",
    "mn": "망간(mg)"
}

idx_map = {}
for key, col_name in cols_map.items():
    if col_name in headers:
        idx_map[key] = headers.index(col_name)
    else:
        print(f"Warning: Column '{col_name}' not found in headers!")

# Parse data rows
trimmed = []
for r in rows[1:]:
    name = r.get(idx_map.get("name"))
    if not name or str(name).strip() in ("None", "식품명", ""):
        continue
    
    item = {
        "name": str(name).strip(),
        "times": parse_times(r.get(idx_map.get("times"))) if "times" in idx_map else 1
    }
    
    # Add other nutrients
    for key in idx_map:
        if key in ("name", "times"):
            continue
        val = r.get(idx_map[key])
        item[key] = clean_float(val)
        
    trimmed.append(item)

print(f"Processed {len(trimmed)} items.")

# Save to output path
with open(out_json_path, "w", encoding="utf-8") as f:
    json.dump(trimmed, f, ensure_ascii=False, indent=2)
print(f"Finished writing {out_json_path} successfully!")

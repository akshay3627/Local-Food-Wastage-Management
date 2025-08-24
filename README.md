# 🍲 Local Food Wastage Management System

## 📌 Overview
This project helps manage local food wastage by connecting **Providers** (donors) and **Receivers** (consumers).  
It includes a database, data cleaning, SQL schema, and an interactive **Streamlit dashboard**.

---

## 📂 Folder Structure
```
local_food_wastage/
│
├─ data/
│   ├─ providers_data.csv          # Raw data
│   ├─ receivers_data.csv
│   ├─ food_listings_data.csv
│   ├─ claims_data.csv
│   ├─ providers_clean.csv         # Cleaned data (ready for DB)
│   ├─ receivers_clean.csv
│   ├─ food_listings_clean.csv
│   └─ claims_clean.csv
│
├─ sql/
│   ├─ schema.sql                  # Database schema
│   └─ queries.sql                 # SQL queries (15 queries)
│
├─ app/
│   └─ streamlit_app.py            # Streamlit dashboard
│
├─ notebooks/
│   └─ data_cleaning.py            # Script to clean raw CSVs
│
├─ load_db.py                      # Script to create & load database
├─ food_wastage.db                 # SQLite database (auto-generated)
├─ requirements.txt                # Python dependencies
└─ README.md                       # Documentation
```

---

## ⚙️ Setup Instructions

### 1. Clone / Copy Project
```bash
cd D:\local_food_wastage
```

### 2. Create Virtual Environment (Windows)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

`requirements.txt` should contain:
```
pandas
streamlit
plotly
```

---

## 🧹 Phase 1: Data Preparation
1. Place your **raw CSVs** inside `data/`.  
   Example: `providers_data.csv`, `receivers_data.csv`, etc.  

2. Run cleaning script:
```bash
python notebooks/data_cleaning.py
```
This will generate:
- `providers_clean.csv`  
- `receivers_clean.csv`  
- `food_listings_clean.csv`  
- `claims_clean.csv`  

---

## 🗄️ Phase 2: Database Creation
1. Apply schema and load data:
```bash
python load_db.py
```
✅ Expected Output:
```
Schema applied successfully
Loaded Providers from providers_clean.csv
Loaded Receivers from receivers_clean.csv
Loaded Food_Listings from food_listings_clean.csv
Loaded Claims from claims_clean.csv
🎉 Database created successfully at food_wastage.db
```

---

## 📊 Phase 3: Run Dashboard
Start Streamlit:
```bash
streamlit run app/streamlit_app.py
```

You will get a local URL:
```
Local URL: http://localhost:8501
```

Open in your browser.

---

## 🚀 Features
- **Dashboard** → Overview, food type analysis, claims pie chart, expiry alerts  
- **SQL Queries (15)** → Interactive insights on providers, receivers, claims  
- **Manage Listings** → Add, update, delete food listings  
- **Manage Claims** → Create and update claims  
- **Providers & Receivers** → Manage and add participants  

---

## 📸 Screenshots

### 🔹 Dashboard (Live Metrics + Charts)
![Dashboard Screenshot](<img width="1366" height="768" alt="Screenshot (4)" src="https://github.com/user-attachments/assets/f4468fd6-f816-4456-82a9-bb2a179ffcf4" />
![Dashboard Screenshot](<img width="1366" height="768" alt="Screenshot (10)" src="https://github.com/user-attachments/assets/a5d26fc1-46a1-486b-9433-41a12648bce9" />

![Dashboard Screenshot](<img width="1366" height="768" alt="Screenshot (11)" src="https://github.com/user-attachments/assets/fd7a355f-1d12-4d15-aab3-25ef79d713cd" />


### 🔹 SQL Queries Page
![Queries Screenshot<img width="1366" height="768" alt="Screenshot (5)" src="https://github.com/user-attachments/assets/1f29a041-6249-4cf9-bb33-5ff6b6c6c63c" />


### 🔹 Manage Listings
![Manage Listings Screenshot](<img width="1366" height="768" alt="Screenshot (6)" src="https://github.com/user-attachments/assets/6c5be5bd-11af-48e1-9faa-d86f9b4b7f6e" />


### 🔹 Manage Claims
![Manage Claims Screenshot](<img width="1366" height="768" alt="Screenshot (8)" src="https://github.com/user-attachments/assets/6cc9ba03-51ac-4279-950e-1d49a04eb2e2" />


### 🔹 Providers & Receivers
![Providers Screenshot](<img width="1366" height="768" alt="Screenshot (9)" src="https://github.com/user-attachments/assets/2b86e042-416a-4d70-ab4d-36ee7eb7cd46" />


---

## 📝 Notes
- If schema mismatch errors happen → delete `food_wastage.db` and re-run `load_db.py`.
- Always run project from **root folder** (`D:\local_food_wastage`).
- Make sure your `food_wastage.db` is up-to-date before starting Streamlit.

---

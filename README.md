# Autonomous-Insider-Threat-Detection-via-Digital-Footprint
AI-powered Insider Threat Detection system that analyzes digital footprints using machine learning and behavioral analytics to identify suspicious user activities in real time.
Insider Threat Detection System (AI + Rule-Based)

An advanced Insider Threat Detection System built using Machine Learning (Isolation Forest) combined with Rule-Based Detection, with an interactive Streamlit Dashboard for security monitoring.

This project analyzes enterprise activity logs (CERT r4.2 dataset format) to detect suspicious user behavior such as:
High data exfiltration
Suspicious SFTP usage
Remote VM access from unknown locations
Abnormal working hours
Behavioral anomalies using ML

# Project Architecture

Raw Dataset (CERT r4.2)                                                                                                                                            
        ↓                                                                                                                                                          
load_data.py
        ↓
preprocess.py
        ↓
features.py
        ↓
train_model.py
        ↓
detect.py
        ↓
Streamlit Dashboard (dashboard.py)

# Project Structure

.
├── load_data.py          # Convert CSV logs to Parquet format
├── preprocess.py         # Clean & normalize raw data
├── features.py           # Generate user-day behavioral features
├── train_model.py        # Train Isolation Forest model
├── detect.py             # Generate alerts (ML + Rules)
├── dashboard.py          # Streamlit monitoring dashboard
├── requirements.txt
├── data/
│   ├── raw/
│   ├── cleaned/
│   ├── features/
├── models/
├── outputs/
│   ├── alerts.csv
│   └── alerts.json

# Technologies Used
Python
Pandas
NumPy
Scikit-learn
Isolation Forest
Streamlit
Plotly
PyArrow
Machine Learning 
Artificial intelligence

# Machine Learning Approach

The system uses Isolation Forest for anomaly detection
Features Used:
total_bytes
avg_hour
sftp_count
remote_vm_count
unknown_loc_count
Model:
200 estimators
1% contamination
StandardScaler normalization
Threshold = 99th percentile anomaly score

# Detection Logic
Alerts are generated if:
Anomaly Score > Learned Threshold

Rule-Based Condition:
User's total_bytes > 95th percentile
Remote VM + Unknown Location + SFTP activity combinatio

# Detection logic implemented in:
Alerts are saved as:
outputs/alerts.csv
outputs/alerts.json

# Interactive Dashboard

Built using Streamlit + Plotly
Dashboard Features:
Filter by user
Filter by minimum ML score
Rule-based only filter
Alerts over time visualization
Top risky users
Scatter plot (data volume vs anomaly score)
CSV download option

Run Dashboard:
streamlit run dashboard.py

# How to Run the Project

1️⃣ Install Dependencies
pip install -r requirements.txt

2️⃣ Load Raw Dataset
python load_data.py

Converts CSV logs into parquet format.

3️⃣ Preprocess Data
python preprocess.py

Standardizes column names
Parses timestamps
Cleans object columns

4️⃣ Feature Engineering
python features.py

Generates behavioral user-day features.

5️⃣ Train Model
python train_model.py

Creates:
models/iso_model.joblib
models/scaler.joblib
models/threshold.json

6️⃣ Generate Alerts
python detect.py

Creates:
outputs/alerts.csv
outputs/alerts.json

7️⃣ Launch Monitoring Dashboard
streamlit run dashboard.py



''

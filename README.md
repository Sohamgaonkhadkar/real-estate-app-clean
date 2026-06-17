# Gurgaon Real Estate Intelligence Portal (Production Deployment)

**Author:** Soham Mahesh Gaonkhadkar  
**Institution:** Indian Institute of Technology Kharagpur  

**Live Deployment Access:** [http://140.238.240.219:8501](http://140.238.240.219:8501)  
*(Note: Hosted on Oracle Cloud Infrastructure. Uptime is subject to OCI free-tier compute instance availability).*

---

## Application Architecture and Scope
This repository contains the production-grade Streamlit application serving the Gurgaon Real Estate Machine Learning pipeline. The application serializes the mathematical models and similarity matrices developed in the primary research repository, deploying them as three distinct, interactive microservices. 

## Core Microservices

### 1. Predictive Valuation Engine
An algorithmic price prediction interface. Users input specific property metrics (Sector, Built-up Area, BHK, Property Age, and Luxury/Furnishing Scores) to receive a direct, data-driven market valuation.
* **Backend Infrastructure:** Driven by an Optuna-optimized **XGBoost Regressor** (MAE: 0.4475).
* **Feature Engineering Integration:** The model seamlessly processes high-cardinality geographic inputs (100+ Gurgaon sectors) using a serialized Scikit-Learn `ColumnTransformer` embedded with **Bayesian Target Encoding**.

### 2. Context-Aware Recommender System
A similarity-matching engine that outputs the top comparable properties based on a selected target asset.
* **Backend Infrastructure:** Powered by a customized **Weighted Multi-Matrix Ensemble Algorithm**.
* **Algorithmic Logic:** Fuses three separate Cosine Similarity matrices—Amenities (TF-IDF), Structural Metrics (Normalized Euclidean), and Spatial/Locational Advantages—into a master weighted matrix to replicate holistic buyer decision-making.

### 3. Sector-Wise Market Analytics
A macroeconomic data visualization dashboard designed to identify market distributions and pricing variance across the city.
* **Analytics Output:** Provides aggregate insights into sector-wise pricing, explicitly mapping which geographic sectors operate as premium/costly environments versus affordable/cheaper segments.
* **Metrics Tracked:** Price-per-square-foot trends, inventory distribution, and structural variance across independent houses versus residential flats.

## Technical Stack & Infrastructure

* **Deployment Hosting:** Oracle Cloud Infrastructure (OCI) Compute Instance
* **Frontend Framework:** Streamlit
* **Model Serialization:** `pickle` (Exported XGBoost model, preprocessor pipelines, and cosine matrices)
* **Data Processing Backend:** Pandas, NumPy
* **Core ML Engine:** Scikit-Learn, Category Encoders

## Source Code / Local Replication

In the event that the Oracle Cloud compute instance is temporarily spun down due to resource limits, the application architecture can be reviewed or executed locally:

```bash
# Clone the deployment repository
git clone [https://github.com/Sohamgaonkhadkar/real-estate-app-clean.git](https://github.com/Sohamgaonkhadkar/real-estate-app-clean.git)
cd real-estate-app-clean

# Install dependencies
pip install -r requirements.txt

# Initialize the local server
streamlit run app.py

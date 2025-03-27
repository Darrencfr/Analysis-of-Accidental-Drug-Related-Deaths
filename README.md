# Analysis-of-Accidental-Drug-Related-Deaths

📌 Overview
This end-to-end data science project analyzes accidental drug-related deaths through systematic data cleaning, exploratory analysis, and machine learning techniques. The goal was to uncover patterns in overdose cases to inform public health strategies.

Key Components:
1️⃣ Data Cleaning & Preprocessing
Standardized demographic variables (sex, race, ethnicity)
Handled missing values through imputation (mean, mode) and logical rules
Detected and managed outliers using z-scores
Created new features: Drug_Count and Age_Group

2️⃣ Association Rule Mining (Apriori & FP-Growth)
Discovered frequent drug combinations in overdose cases
Identified strong rules (e.g., "Heroin → Fentanyl" with lift > 3.5)
Compared algorithm performance: FP-Growth was 3x faster than Apriori

3️⃣ Predictive Modeling
Classification (Random Forest): Predicted Fentanyl involvement (89% AUC)
Top predictor: Cause_of_Death
Regression (Random Forest): Predicted death location from injury data (R² = 0.68)

4️⃣ Clustering & Anomaly Detection
Hierarchical clustering revealed 6 distinct drug-use patterns
LOF algorithm flagged high-risk counties for targeted interventions

Technical Highlights
✔ Data Wrangling: Pandas, Regex
✔ ML Algorithms: Random Forest, Agglomerative Clustering, LOF, Apriori, FPGrowth 
✔ Visualization: Matplotlib, Seaborn 
✔ Optimization: GridSearchCV for hyperparameter tuning

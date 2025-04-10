# -*- coding: utf-8 -*-
"""AssignmentPart2_Code_2_0369793.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aym3qwJQXMVCSC-yGl3ZB5EaDvCS5UGx

# Import libraries
"""

#relevant imports
import pandas as pd
import numpy as np
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori as apmlx, association_rules as rulesmlx
from mlxtend.frequent_patterns import fpgrowth
import time
import tracemalloc
import psutil

"""# Import Dataset"""

#import datasetv Accidental_Drug_Related_Deaths_Cleaned.xlsx
df = pd.read_excel('Accidental_Drug_Related_Deaths_Cleaned.xlsx')

"""# Pre=Processing"""

#convert "Other_Opioid" and "Other" to binary
df['Other_Opioid']= df['Other_Opioid'].apply(lambda x: 1 if isinstance(x, str) and x.strip() != "None" else 0)
df['Other'] = df['Other'].apply(lambda x: 1 if isinstance(x, str) and x.strip() != "None" else 0)

print(df.head())

#columns to drop
columns_to_drop = [
    "Date", "Date_Type", "Age", "Age_Group", "Sex", "Race", "Ethnicity",
    "Residence_City", "Residence_County", "Residence_State", "Injury_City",
    "Injury_County", "Injury_State", "Injury_Place", "Description_of_Injury",
    "Death_City", "Death_County", "Death_State", "Location", "Location_if_Other",
    "Cause_of_Death", "Manner_of_Death", "Other_Significant_Conditions_",
    "Heroin_death_certificate_(DC)", "Drug_Count","Any_Opioid"
]

#drop columns
df = df.drop(columns=columns_to_drop, errors="ignore")

print(df.head())

#convert to list of lists (each row represents drugs present in a case)
drugs = df.apply(lambda row: [col for col in df.columns if row[col] == 1], axis=1).tolist()

#apply TransactionEncoder for one-hot encoding
te = TransactionEncoder()
te_array = te.fit(drugs).transform(drugs)
dataset_encoded = pd.DataFrame(te_array, columns=te.columns_)

#remove empty or single-item drug
filtered_drugs = [t for t in drugs if len(t) >= 2]

#export dataset
dataset_encoded.to_excel("Asg2_cleaned_dataset.xlsx", index=False)

"""# Apriori Algoritm"""

#start tracking the time
start_time = time.time()

#start ttracking the memory usage
tracemalloc.start()

#finds Frequent Itemsets
#min_support=0.045: Includes only itemsets appearing in at least 4.5% of drug.
frequent_items = apmlx(dataset_encoded, min_support=0.045, use_colnames=True)
print("\n\n\nShow Frequent Items by Support:\n", frequent_items.sort_values(by="support", ascending=False))

#generate association rules
#min_threshold = 0.6: Filters rules where confidence is at least 80%.
rules = rulesmlx(frequent_items, metric="confidence", min_threshold=0.8)

#sorts rules by highest confidence, then highest lift.
rules = rules.sort_values(['confidence', 'lift'], ascending=[False, False])
print("\n\n\nSample Results:")
print(rules.head())

#filter Strong Rules
print("\n\n\nStrong Rules:")
print(rules[["antecedents", "consequents","support", "confidence","lift"]])

#filters rules where lift is at least 3 (moderate association)
#ensures confidence is at least 60%.
strong_results = rules[(rules['lift'] >=3) & (rules['confidence'] >= 0.8)]

#only print the strongest ones.
print("\n\n\nFiltered Results:\n",strong_results[["antecedents", "consequents","support", "confidence","lift"]])

#ending memory usage trracking
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

#ending time tracking
execution_time = time.time() - start_time

#system resource usage
cpu_usage = psutil.cpu_percent(interval=1)
memory_usage = psutil.virtual_memory().percent

#results
print("\n\n\nSystem Results:")
print(f"Execution Time: {execution_time:.4f} seconds")
print(f"Memory Used: {current / 10**6:.4f} MB (Peak: {peak / 10**6:.4f} MB)")
print(f"CPU Usage: {cpu_usage:.2f}%")
print(f"System Memory Usage: {memory_usage:.2f}%")

"""FP Growth"""

#start tracking the time
start_time = time.time()

#start ttracking the memory usage
tracemalloc.start()

#min_support=0.045 - Filters itemsets that appear in at least 4.5% of transactions.
fp_results = fpgrowth(dataset_encoded, min_support= 0.045, use_colnames= True)
print("\n\n\nShow Frequent Items by Support:\n", fp_results.sort_values(by="support", ascending=False))

#association rules with confidence ≥ 0.6
rules_fp = rulesmlx(fp_results, metric="confidence", min_threshold=0.8)

#sort rules by confidence (descending), then by lift (descending)
rules_fp = rules_fp.sort_values(['confidence', 'lift'], ascending=[False, False])
print("\n\n\nSample Results:")
print(rules_fp.head())

#filter Strong Rules
print("\n\n\nStrong Rules:")
print(rules[["antecedents", "consequents","support", "confidence","lift"]])

# filter strong rules: Lift ≥ 5 and Confidence ≥ 0.6 (same as Apriori)
strong_results = rules_fp[(rules_fp['lift'] >= 3) & (rules_fp['confidence'] >= 0.8)]
print("\n\n\nFiltered Results:\n",strong_results[["antecedents", "consequents","support", "confidence","lift"]])

#ending memory usage trracking
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

#ending time tracking
execution_time = time.time() - start_time

#system resource usage
cpu_usage = psutil.cpu_percent(interval=1)
memory_usage = psutil.virtual_memory().percent

#results
print("\n\nSystem Results")
print(f"Execution Time: {execution_time:.4f} seconds")
print(f"Memory Used: {current / 10**6:.4f} MB (Peak: {peak / 10**6:.4f} MB)")
print(f"CPU Usage: {cpu_usage:.2f}%")
print(f"System Memory Usage: {memory_usage:.2f}%")
#Variables ->
# 1. Smoking 
smoking = "no"
# 2. Diabetes
diabetes = "yes"
# 3a. BP Systolic 
bp_s = 155
# 3b. BP Diastolic
bp_d = 86
# 4. Age
age = 45
# 5. HDL Cholesterol
hdl = 1.31
# 6. total cholesterol
tc = 5.3
# 7. gender
gender = "male"


# Converting input to points ->
import numpy as np
import pandas as pd

df_age = pd.read_csv("Age_chart.csv")
df_smoking = pd.read_csv("Smoking.csv")
df_diabetes = pd.read_csv("Diabetes.csv")
df_tc = pd.read_csv("total_cholesterol.csv")
df_hdl = pd.read_csv("HDL_cholesterol.csv")
df_bp = pd.read_csv("BP_chart.csv")


# age
for row in df_age.index:
    if age < df_age["Age_high"][row]:
        break
age_point = df_age[gender.title()][row]


# smoking
for row in df_smoking.index:
    if df_smoking["Smoking"][row] == smoking.title():
        break
smoking_point = df_smoking[gender.lower()][row]


# diabetes
for row in df_diabetes.index:
    if df_diabetes["diabetes"][row] == diabetes.title():
        break
diabetes_point = df_diabetes[gender.lower()][row]


# hdl cholesterol
for row in df_hdl.index:
    if hdl < df_hdl["hdl_high"][row]:
        break
hdl_point = df_hdl[gender.lower()][row]


# tc
for row in df_tc.index:
    if tc < df_tc["Cholesterol_high"][row]:
        break
tc_point = df_tc[gender.title()][row]


# BP
for row in df_tc.index:
    if bp_s < df_bp["Systolic_BP_high"][row]:
        break
for row in range(row, row+7, 1):
    if bp_d < df_bp["Diastolic_BP_high"][row]:
        break
bp_point = df_bp[gender.lower()][row]


# Points to risk value ->
risk_points = age_point + smoking_point + diabetes_point + tc_point + hdl_point + bp_point


df_points_to_risk = pd.read_csv("points_to_score.csv")


#Final display ->
for row in df_points_to_risk.index:
    if risk_points == df_points_to_risk["total_score"][row]:
        break
risk_percentage = df_points_to_risk[gender.lower()+"_risk"][row]
print(risk_percentage)

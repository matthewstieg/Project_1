


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
import json
from pprint import pprint
import csv
import quandl
from config import api_key_housing

states = ["Alabama", "Alaska", "Arizona","Arkansas","California","Colorado","Connecticut","Delaware","District of Columbia","Florida","Georgia",
          "Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts",
          "Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey",
          "New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island",
          "South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin",
          "Wyoming"
]




df = pd.DataFrame(data={"States": states})
df["Median Income"] = ""
df["Home Value '11"] = ""
df["Home Value '17"] = ""
df["Bachelors Degree"] = ""
df["Population"] = ""
df["Divorce"] = ""


df




area_categorytest = "S"
area_codetest = "2"
indicator_codetest = "MVALFAH"
frequencytest = "annual"
numberofrowstest = "11"
# Zillow - Median Value Per Square Foot - All Homes|MVALFA

test_url = f"https://www.quandl.com/api/v3/datasets/ZILLOW/{area_categorytest}{area_codetest}_{indicator_codetest}?&collapse={frequencytest}&rows={numberofrowstest}"

responsetest = requests.get(test_url).json()




statesdf = pd.read_csv("StateList.csv")
merge_table = pd.merge(df, statesdf, on="States", how="right")
organized_df = merge_table[["States","Area Code", "Home Value '11", "Home Value '17"]]

organized_df







for index, row in organized_df.iterrows():
    area_code = row["Area Code"]
    area_category = "S"
    indicator_code = "MVALFAH"
    frequency = "annual"
    numberofrows = "11"
    base_url = f"https://www.quandl.com/api/v3/datasets/ZILLOW/{area_category}{area_code}_{indicator_code}?&collapse={frequency}&rows={numberofrows}&api_key={api_key_housing}"
    response1 = requests.get(base_url)
    response1json = response1.json()
    organized_df.loc[index, "Home Value '11"] = response1json['dataset']['data'][8][1]
    organized_df.loc[index, "Home Value '17"] = response1json['dataset']['data'][2][1]


organized_df






organized_df[["Home Value '11", "Home Value '17"]] = organized_df[["Home Value '11", "Home Value '17"]].apply(pd.to_numeric)

organized_df["Home Value % Change"] = round(((organized_df["Home Value '17"] - organized_df["Home Value '11"]) / organized_df["Home Value '11"])*100,2)
sorted_df = organized_df.sort_values("Home Value % Change", ascending=False)


sorted_df



home11 = sorted_df["Home Value '11"]
home17 = sorted_df["Home Value '17"]
homepct = sorted_df["Home Value % Change"]
states = sorted_df["States"]

fig,ax=plt.subplots(figsize=(15,5))
plt.bar(states, homepct, color='teal', alpha=1, align="center")
plt.tight_layout()
plt.xticks(states, rotation='90')
plt.title("Median Home Value per Square Foot Change Between 2011 and 2017")
plt.ylabel("Percent Change")
plt.grid()
plt.show






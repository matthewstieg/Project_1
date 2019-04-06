import requests
import json
import pandas as pd
from pprint import pprint
from census import Census
from us import states

#Census API Key
from config import api_key
c = Census(api_key, year=2017)
c2= Census(api_key, year=2011)

states = ["Alabama", "Alaska", "Arizona","Arkansas","California","Colorado","Connecticut","Delaware","District of Columbia","Florida","Georgia",
          "Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts",
          "Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey",
          "New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island",
          "South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin",
          "Wyoming"
]

df = pd.DataFrame(data={"States": states})
df["Median Income"] = ""
df["Home Value"] = ""
df["Bachelors Degree"] = ""
df["Population"] = ""
df["Divorce"] = ""

# Pull US Census Data for each State
census_data = c.acs1.get(("NAME", "B01003_001E", "B15003_022E","B15003_023E","B15003_024E","B15003_025E",
                          "B23025_002E","B23025_005E", "B21003_001E", "B15003_017E","B15003_018E","B15003_019E",
                         "B15003_020E","B15003_021E"), {'for': 'state:*'})
census_2017 = pd.DataFrame(census_data)


# B15003_022E = Bachelors Degree
# B15003_023E = Masters
# B15003_024E = Professional
# B15003_025E = Doctor
# B19013_001E = Household income
# B01003_001E = Population
# B01002_001E = Median Age
# B19301_001E = Per Capita Income
# B15003_023E = Masters Degree
# B23025_002E = Labor Force
# B23025_004E = Employed
# B23025_005E = Unemployed
# B25077_001E = Median Home Value
# B08136_003E = Commute Time (in minutes)


census_2017 = census_2017.rename(columns={"B01003_001E": "Population",
                                      "B15003_022E": "Bachelors",
                                      "B15003_023E": "Masters",
                                      "B15003_024E": "Professional",
                                      "B15003_025E": "Doctor",
                                      "B23025_002E": "Labor Force",
                                      "B23025_005E": "Unemployed",
                                      "B21003_001E": "Pop25",
                                      "B15003_017E": "HS",
                                      "B15003_018E": "GED",
                                      "B15003_019E": "Under 1",
                                      "B15003_020E": "Over 1",
                                      "B15003_021E": "Associates",
                                      "NAME": "State", "state": "Code"})

# Add dataframe columns for bachelors and above as well as HS diploma and above (including GED)
census_2017["Bachelor+"] = census_2017["Bachelors"]+census_2017["Masters"]+census_2017["Professional"]+census_2017["Doctor"]
census_2017["HS+"]= census_2017["HS"]+census_2017["GED"]+census_2017["Bachelor+"]+census_2017["Under 1"]+census_2017["Over 1"]+census_2017["Associates"]

census_2017 = census_2017[["State", "Population","Pop25", "HS","GED","HS+","Bachelors", "Bachelor+","Labor Force", "Unemployed"]]

census_2017["Bachelors Rate"] = round((census_2017["Bachelor+"]/census_2017["Pop25"])*100,2)
census_2017["HS Diploma Rate"] = round(((census_2017["HS+"] + census_2017["GED"])/census_2017["Pop25"])*100,2)
census_2017["Unemployment Rate"] = round((census_2017["Unemployed"]/census_2017["Labor Force"])*100,2)

# Final Dataframe
census_2017 = census_2017[["State", "Population","Bachelors Rate", "HS Diploma Rate","Unemployment Rate"]]
# census_2017.to_csv("output.csv")

# Build exact same dataframe for 2011 data
census_data2 = c2.acs1.get(("NAME", "B01003_001E", "B15003_022E","B15003_023E","B15003_024E","B15003_025E",
                          "B23025_002E","B23025_005E", "B21003_001E", "B15003_017E","B15003_018E","B15003_019E",
                         "B15003_020E","B15003_021E"), {'for': 'state:*'})
census_2011 = pd.DataFrame(census_data2)

census_2011 = census_2011.rename(columns={"B01003_001E": "Population",
                                      "B15003_022E": "Bachelors",
                                      "B15003_023E": "Masters",
                                      "B15003_024E": "Professional",
                                      "B15003_025E": "Doctor",
                                      "B23025_002E": "Labor Force",
                                      "B23025_005E": "Unemployed",
                                      "B21003_001E": "Pop25",
                                      "B15003_017E": "HS",
                                      "B15003_018E": "GED",
                                      "B15003_019E": "Under 1",
                                      "B15003_020E": "Over 1",
                                      "B15003_021E": "Associates",
                                      "NAME": "State", "state": "Code"})

census_2011["Bachelor+"] = census_2011["Bachelors"]+census_2011["Masters"]+census_2011["Professional"]+census_2011["Doctor"]
census_2011["HS+"]= census_2011["HS"]+census_2011["GED"]+census_2011["Bachelor+"]+census_2011["Under 1"]+census_2011["Over 1"]+census_2011["Associates"]

census_2011 = census_2011[["State", "Population","Pop25", "HS","GED","HS+","Bachelors", "Bachelor+","Labor Force", "Unemployed"]]

census_2011["Bachelors Rate"] = round((census_2011["Bachelor+"]/census_2011["Pop25"])*100,2)
census_2011["HS Diploma Rate"] = round(((census_2011["HS+"] + census_2011["GED"])/census_2011["Pop25"])*100,2)
census_2011["Unemployment Rate"] = round((census_2011["Unemployed"]/census_2011["Labor Force"])*100,2)

census_2011 = census_2011[["State", "Population","Bachelors Rate", "HS Diploma Rate","Unemployment Rate"]]

# Merge 2 dataframes
census_merged = pd.merge(census_2011, census_2017, how="inner",on="State",suffixes=("_2011", "_2017"))

# Remove Puerto Rico
census_merged = census_merged[census_merged.State != "Puerto Rico"]

# Reorder Columns for Readability
census_merged = census_merged[["State", "Population_2011", "Population_2017", "Bachelors Rate_2011", "Bachelors Rate_2017","Unemployment Rate_2011", "Unemployment Rate_2017"]]

# Calculate percent change between years for each metric
census_merged["Population Change"]=round((((census_merged["Population_2017"]-census_merged["Population_2011"])/census_merged["Population_2011"])*100),2)
census_merged["Education Change"]=round((((census_merged["Bachelors Rate_2017"]-census_merged["Bachelors Rate_2011"])/census_merged["Bachelors Rate_2011"])*100),2)
census_merged["Unemployment Change"]=round((((census_merged["Unemployment Rate_2017"]-census_merged["Unemployment Rate_2011"])/census_merged["Unemployment Rate_2011"])*100),2)

# Reorder Columns for Readability
census_merged=census_merged[["State","Population Change", "Education Change", "Unemployment Change"]]
census_merged

# rank order each metric
census_merged["Population Score"]= census_merged["Population Change"].rank()
census_merged["Education Score"]= census_merged["Education Change"].rank()
census_merged["Unemployment Score"]=census_merged["Unemployment Change"].rank(ascending=False)

# Reorder Columns for Readability
census_merged=census_merged[["State","Population Change", "Population Score", "Education Change","Education Score", "Unemployment Change", "Unemployment Score"]]
census_merged["Composite Score"]=census_merged["Population Score"]+census_merged["Education Score"]+census_merged["Unemployment Score"]
census_merged
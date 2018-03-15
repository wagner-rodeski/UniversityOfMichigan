# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 11:42:10 2018

@author: wagner_rodeski
"""
#  Definitions:
#  A quarter is a specific three month period, Q1 is January through March, Q2 is April through June, 
#  Q3 is July through September, Q4 is October through December.
#  A recession is defined as starting with two consecutive quarters of GDP decline, and ending with 
#  two consecutive quarters of GDP growth.
#  A recession bottom is the quarter within a recession which had the lowest GDP.
#  A university town is a city which has a high percentage of university students compared to the
#  total population of the city.
#  Hypothesis: University towns have their mean housing prices less effected by recessions. 
#  Run a t-test to compare the ratio of the mean price of houses in university towns the quarter 
#  before the recession starts compared to the recession bottom. 
#  (price_ratio=quarter_before_recession/recession_bottom)

#  The following data files are available for this assignment:

#  From the Zillow research data site there is housing data for the United States. In particular the 
#  datafile for all homes at a city level, City_Zhvi_AllHomes.csv, has median home sale prices at a fine 
#  grained level.
#  From the Wikipedia page on college towns is a list of university towns in the United States which has 
#  been copy and pasted into the file university_towns.txt.
#  From Bureau of Economic Analysis, US Department of Commerce, the GDP over time of the United States 
#  in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file 
#  gdplev.xls. For this assignment, only look at GDP data from the first quarter of 2000 onward.

# In[]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

a = pd.read_csv('City_Zhvi_AllHomes.csv')
b = pd.read_table('university_towns.txt',names = ['teste'])
c = pd.read_excel('gdplev.xls', usecols = [4, 6], skiprows=7, names = ['Quarter', 'GDP'])

states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 
'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 
'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 
'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 
'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 
'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 
'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 
'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 
'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 
'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 
'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 
'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
# In[]:
#  def get_list_of_university_towns():
#    '''Returns a DataFrame of towns and the states they are in from the 
#    university_towns.txt list. The format of the DataFrame should be:
#    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
#    columns=["State", "RegionName"]  )
#    
#    The following cleaning needs to be done:
#
#    1. For "State", removing characters from "[" to the end.
#    2. For "RegionName", when applicable, removing every character from " (" to the end.
#    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
# In[]:
b.head(20)

d = pd.DataFrame(b['teste'].str.split('(').str.get(0), columns=['teste'])
d.rename(columns={'teste':'RegionName'}, inplace = True)
d['RegionName'][11].find('[edit]')
d['RegionName'] = d['RegionName'].str.strip(' ')
d['State'] = ''
for i in d.index:
    if d['RegionName'][i].find('[edit]') != -1:
        k = d['RegionName'][i].split('[')[0]
        d['State'][i] = k
    d['State'][i] = k
     
d = d.drop(d[d['RegionName'].str.contains('edit')].index)
d = d[['State', 'RegionName']]
d.head(20)

#  e = pd.DataFrame([states.values()]).T
#  e['State'] = pd.DataFrame([states.keys()]).T
#  e.rename(columns={0:'State_ext'}, inplace = True)
#  e.head(20)
#  pd.merge(d, e, how='left', left_on='State_ext', right_on='State_ext')

# In[]:
#  def get_recession_start():
#      '''Returns the year and quarter of the recession start time as a 
#      string value in a format such as 2005q3'''
#      
#  A recession is defined as starting with two consecutive quarters of GDP decline, and ending with 
#  two consecutive quarters of GDP growth.
#  A recession bottom is the quarter within a recession which had the lowest GDP.

c.head(20)
c['year'] = c['Quarter'].str.split('q').str.get(0)    
c = c.loc[c['year'] >= '2000']
c.reset_index(inplace = True)

ini_rec = ''
for i in c.index:
    if c['GDP'][i+2] < c['GDP'][i+1]:
        if c['GDP'][i+1] < c['GDP'][i]:
            ini_rec = c['Quarter'][i+1]
            break
        else:
            continue
        break
    else:
        continue
            
ini_rec

# In[]:
#  def get_recession_end():
#      '''Returns the year and quarter of the recession end time as a 
#      string value in a format such as 2005q3'''
#  

for i in (c.index + c.loc[c['Quarter'] == ini_rec].index[0]):
    if c['GDP'][i+2] > c['GDP'][i+1]:
        if c['GDP'][i+1] > c['GDP'][i]:
            end_rec = c['Quarter'][i+2]
            break
        else:
            continue
        break
    else:
        continue

end_rec

# In[]:
#  def get_recession_bottom():
#      '''Returns the year and quarter of the recession bottom time as a 
#      string value in a format such as 2005q3'''

index_start = c.loc[c['Quarter'] == ini_rec].index[0]
index_end = c.loc[c['Quarter'] == end_rec].index[0]
gdp_min = c['GDP'][index_start : index_end].min()

index_start
index_end
gdp_min

bottom_rec = c['Quarter'][c.loc[c['GDP'] == gdp_min].index[0]]
bottom_rec

# In[]:
#  def convert_housing_data_to_quarters():
#      '''Converts the housing data to quarters and returns it as mean 
#      values in a dataframe. This dataframe should be a dataframe with
#      columns for 2000q1 through 2016q3, and should have a multi-index
#      in the shape of ["State","RegionName"].
#      
#      Note: Quarters are defined in the assignment description, they are
#      not arbitrary three month periods.
#      
#      The resulting dataframe should have 67 columns, and 10,730 rows.
#      '''
a.head()

e = a.copy()
k = 1
for i in range(51,249,3):
    e[e.iloc[:,i].name[:4] + 'q' + str(k)] = (e.iloc[:,i] + e.iloc[:,i+1] + e.iloc[:,i+2])/3
    k = k + 1
    if k > 4:
        k = 1
i = 249
e[e.iloc[:,i].name[:4] + 'q' + str(k)] = (e.iloc[:,i] + e.iloc[:,i+1] )/2

e.drop(e.columns[3:251], axis=1, inplace = True)
e.drop(e.columns[0], axis=1, inplace = True)

e = e.set_index(['State','RegionName'])

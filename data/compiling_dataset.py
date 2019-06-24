"""
File name: compiling_dataset.py
Author: Jaala Robinson
Date Created: 4/16/2019
Date Last Modified: 5/10/2019
Python Version: 3.7.3
Description: Compilation of comprehensive state-level abortion dataset
"""

import pandas as pd
import numpy as np
from datetime import datetime
import wget
import json
import urllib
import requests
import zipfile
import re
import io
import gzip
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.io as spio
import os
import savReaderWriter
import dask.dataframe as dd

# ULTIMATE GOAL
#TEST

df = pd.DataFrame({
    'Year': [0],
    'State': [0],
    'Number_of_Clinics': [0], #
    'Percent_R_in_State_Gov': [0],
    'Percent_R_in_Fed_Gov': [0],
    'R_President': [0],
    'Percent_R_in_Pop': [0],
    'Anti_Laws_on_Books': [0],
    'Anti_Legis_Intro': [0],
    'Anti_Legis_Passed': [0],
    'Support_Laws_On_Books': [0],
    'Support_Laws_Intro': [0],
    'Support_Laws_Passed': [0],
    'ACA_Medicaid_Exp': [0],
    'Percent_Black': [0],
    'Percent_Latino': [0],
    'Percent_Asian': [0],
    'Percent_Native': [0],
    'Percent_Evang': [0],
    'Abortion_Rate_Occurence': [0],
    'Abortion_Rate_Residence': [0],
    'Percent_Counties_No_Clinic': [0], #
    'Percent_Women_Without_Clinic': [0] #
})

################################################################################
#####################GUTTMACHER DATA COMPILATION################################
################################################################################

# I first need to import the data from CSV files downloaded from Guttmacher:
# https://data.guttmacher.org/
#
# This data includes various measures pertaining to abortion access from all
# states across an assortment of years. I will import this data, which exists
# in multiple CSV files, process as needed, then join them together to create
# a single Guttmacher dataset with MultiIndex 'State', 'Year'.
#
# This will be the dataframe that is then added to with additional sources

# Importing the data, which is arranged variably within individual CSV files,
# requires some dictionary mapping, as below.

list_csvs = ['abortion_rate_trend', 'abortion_rate_res_trend', 'gutt_data',
            'num_abortion_res', 'num_abortion_trend', 'num_providers_trend',
            'per_counties_no_clinic_trend', 'per_women_wo_clinic_trend']
dict_columns = {
    1: ['datum', 'state_name', 'datum_date'],
    2: ['datum', 'state_name',  'first_year'],
    3: ['measure_name', 'datum', 'state_name', 'first_year']
    }
link_csv_column = {
    'abortion_rate_trend': 1,
    'abortion_rate_res_trend': 2,
    'gutt_data': 3,
    'num_abortion_res': 1,
    'num_abortion_trend': 1,
    'num_providers_trend': 1,
    'per_counties_no_clinic_trend': 1,
    'per_women_wo_clinic_trend': 1
}
names_column = {
    'abortion_rate_trend': 'Abortion_Rate_Occurence',
    'abortion_rate_res_trend': 'Abortion_Rate_Residence',
    'gutt_data': 'Various_Data',
    'num_abortion_res': 'Number_Abortions_Residence',
    'num_abortion_trend': 'Number_Abortions_Occurence',
    'num_providers_trend': 'Number_of_Clinics',
    'per_counties_no_clinic_trend': 'Percent_Counties_No_Clinic',
    'per_women_wo_clinic_trend': 'Percent_Women_Without_Clinic'
}
list_df = []

################################################################################
# import_data(x)
# This function imports Guttmacher csv files and then retains the necessary
# columns for further cleaning and analysis
# Inputs: x is a list containing csv filenames
# Returns: A list, list_df, of imported dataframes with columns renamed for
# consistency
def import_data(x):
    for i in x:
        i_import = pd.read_csv('/home/jaala/win-Python/Projects/Abortion/data/{}.csv'.format(i))
        link = link_csv_column[i]
        if link == 1:
            to_df = i_import[dict_columns[link]]
            df_i = to_df.rename(columns={
            'datum_date': 'Year',
            'state_name': 'State',
            'datum': names_column[i]})
        elif link == 2:
            to_df = i_import[dict_columns[link]]
            df_i = to_df.rename(columns={
            'first_year': 'Year',
            'state_name': 'State',
            'datum': names_column[i]})
        else:
            to_df = i_import[dict_columns[link]]
            df_i = to_df.rename(columns= {
            'measure_name': 'Measure_Name',
            'first_year': 'Year',
            'state_name': 'State',
            'datum': names_column[i]})
        list_df.append(df_i)
    return list_df

import_data(list_csvs)

# Breaking the list into individual dfs is useful for assessing and completing
# individualized data cleaning based on dataset needs
art = list_df[0]
arrs = list_df[1]
gd = list_df[2]
nar = list_df[3]
nat = list_df[4]
npt = list_df[5]
pcnct = list_df[6]
pwwct = list_df[7]

# Dataframe, arrs, has duplicate rows present in raw data. Dropping.
arrs.drop_duplicates(inplace=True)

# These lists will be useful for further processing within for-loops
list_wo_gd = [art, arrs, nar, nat, npt, pcnct, pwwct]
list_w_gd = [art, arrs, gd, nar, nat, npt, pcnct, pwwct]

# The Year column is formatted differently between datasets (and sometimes
# within datasets). I need to standardize all these columns to an interval
# before I can do the big merge of all datasets.
#
# I write a function that determines whether the current column is string, float
# or interval. If interval, I leave it be. If float, I convert to interval.
# If string, I call a second function that performs a regex search for the year
# and extracts that. Then I iterate through the list of datasets

################################################################################
# extract_string(i)
# This function uses regex to find an extract the year of the date string
# Input: i is the string value of the dataframe cell to be evaluated
# Returns: A string containing only the year in 4 digits
def extract_string(i):
    m = re.search(pattern='[0-9]{4}', string=i)
    return m.group()

################################################################################
# format_to_year(x)
# This function checks to see if the Year value is formatted as an interval. If
# is not, then it adjusted the format accordingly depending on its current
# format.
#
# Additionally, NaNs are converted to 0s as NaNs will interfere with later
# processing. This will be converted back later in process.
# Input: x is the dataset containing column 'Year' to be evaluated
# Returns: Same list with reformatted dfs
def format_to_year(x):
    x.Year.fillna(value=0, inplace=True)
    if isinstance(x.loc[0,'Year'], float):
        x = x.astype({"Year": int})
    elif isinstance(x.loc[0, 'Year'], str):
        x.Year = x.Year.apply(extract_string)
        x.Year = pd.to_numeric(x.Year)

for y in list_w_gd:
    format_to_year(y)

# The dataset, gd, is a combination of many measures. The dataframe has a column
# for measure name, a column for value, then state and year columns. I need to
# unstack the measure name and value columns to create a dataframe that has a
# column per measure containing the associated value. This requires some data
# reshaping.

# This crucial column is formatted as string, so I'm converting it to numeric
gd.Various_Data = pd.to_numeric(gd.Various_Data, errors='coerce')

# I will be reshaping the data with .unstack. First, I need to set a
# 3-level index so that I can unstack the final level, the conglomerated column
# This will disperse the data into individual dict_columns
gd_index = gd.set_index(['State', 'Year', 'Measure_Name'], append=True)
unstack_gd = gd_index.unstack('Measure_Name').reset_index()

#I then set and sort the State/Year index for further processing
unstack_gd_new = unstack_gd.set_index(['State', 'Year'])
gd_sorted = unstack_gd_new.sort_index(level=[0 , 1])

# The columns are awkwardly named. For simplicity, I'm assigning the current
# column names to a list, then referencing this with a dict for simpler
# column names before renaming the columns with .map
array_of_meas = list(gd_sorted.columns.values)
measure_to_var = {
    array_of_meas[0]: 'delete_this',
    array_of_meas[1]: 'Percent_Change_Abortion_Rate_Occurence',
    array_of_meas[2]: 'Percent_Change_Providers',
    array_of_meas[3]: 'Percent_Change_Clinics',
    array_of_meas[4]: 'Percent_US_Abortions_Occurence',
    array_of_meas[5]: 'Percent_Counties_No_Provider',
    array_of_meas[6]: 'Percent_Counties_No_Clinic',
    array_of_meas[7]: 'Percent_Women_Medicaid',
    array_of_meas[8]: 'Percent_Women_Private_Insurance',
    array_of_meas[9]: 'Percent_Women_Without_Clinic',
    array_of_meas[10]: 'Percent_Women_Without_Provider',
    array_of_meas[11]: 'Percent_Women_Uninsured',
    array_of_meas[12]: 'Abortion_Rate_Occurence',
    array_of_meas[13]: 'Abortion_Rate_Residence',
    array_of_meas[14]: 'Change_in_Providers',
    array_of_meas[15]: 'Change_in_Clinics',
    array_of_meas[16]: 'Number_Providers',
    array_of_meas[17]: 'Number_Abortions_Occurence',
    array_of_meas[18]: 'Number_Abortions_Residence',
    array_of_meas[19]: 'Number_of_Clinics',
    array_of_meas[20]: 'Number_Fed_Funded_Abortions',
    array_of_meas[21]: 'Number_State_Funded_Abortions',
    array_of_meas[22]: 'Pop_Est_All_Women',
    array_of_meas[23]: 'Fed_Exp_for_Abortions_1000s',
    array_of_meas[24]: 'State_Exp_for_Abortions_1000s',
    array_of_meas[25]: 'Total_Public_Funded_Abortions',
    array_of_meas[26]: 'Total_Number_Women',
    array_of_meas[27]: 'Total_Exp_For_Abortions_1000s'
}
gd_sorted.columns = gd_sorted.columns.map(measure_to_var)

# From a previous .reset_index
gd_sorted.drop('delete_this', axis=1, inplace=True)

# Having State/Year indexed makes the groupby more difficult, so I'm
# flattening the dataset
#
# There is probably a better way of handling the indexing issues with this, but
# this is my first major Python project, and so I am not still learning how to
# implement the dataframes most efficiently
gd_sorted.reset_index(inplace=True)

# Now I am doing a groupby to agg down. The .unstack creates redundant rows
# within groups and I want to collapse it all and keep only the non-missing
# value. .sum will suffice for this as a value plus NaN is the value.
gd_grouped = gd_sorted.groupby(['State', 'Year']).sum()

# I am adding the cleaned gd df to the list of dataframes for final processing
# and merging. First, I need to replace the 0s with NaNs. Then, I sequentially
# join the datasets together, merging on State, Year. This creates a m:m merge
# that holds all the relevant Guttmacher data.
for i, df in enumerate(list_wo_gd):
    list_wo_gd[i] = list_wo_gd[i].set_index(['State', 'Year'])
    list_wo_gd[i] = list_wo_gd[i].sort_index(level=[0,1])

list_wo_gd.append(gd_grouped)

for i, df in enumerate(list_wo_gd):
    list_wo_gd[i].replace(0, value=np.nan, inplace=True)

gutt_df = list_wo_gd[0].join(list_wo_gd[1], on=['State', 'Year'], how='outer')
gutt_df = gutt_df.join(list_wo_gd[2], on=['State', 'Year'], how='outer')
gutt_df = gutt_df.join(list_wo_gd[3], on=['State', 'Year'], how='outer')
gutt_df = gutt_df.join(list_wo_gd[4], on=['State', 'Year'], how='outer')
gutt_df = gutt_df.join(list_wo_gd[5], on=['State', 'Year'], how='outer')
gutt_df = gutt_df.join(list_wo_gd[6], on=['State', 'Year'], how='outer')
gutt_df = gutt_df.join(list_wo_gd[7],
    on=['State', 'Year'], how='outer', rsuffix='_bulk')

# Due to the multiple CSV files imported, there are some duplicate columns.
# However, the missing data is variant between these columns. To max info,
# I'm assigning missing values in the primary (non-bulk) columns to the bulk
# values, if present. Then I will delete the extraneous columns
nonunique = ['Percent_Counties_No_Clinic', 'Abortion_Rate_Occurence',
    'Abortion_Rate_Residence', 'Abortion_Rate_Residence',
    'Number_Abortions_Occurence', 'Number_Abortions_Residence',
    'Number_of_Clinics', 'Percent_Women_Without_Clinic']
for i in nonunique:
    gutt_df[i].fillna(gutt_df['{}_bulk'.format(i)], inplace=True)

gutt_df.drop(['Percent_Counties_No_Clinic_bulk', 'Abortion_Rate_Occurence_bulk',
    'Abortion_Rate_Residence_bulk', 'Abortion_Rate_Residence_bulk',
    'Number_Abortions_Occurence_bulk', 'Number_Abortions_Residence_bulk',
    'Number_of_Clinics_bulk', 'Percent_Women_Without_Clinic_bulk'],
    axis=1, inplace=True)

df_no_index = gutt_df.reset_index()

df_no_index.to_csv('/home/jaala/win-Python/Projects/Abortion/data/df_no_index.csv', index=False)


################################################################################
#####################END GUTTMACHER DATA COMPILATION############################
################################################################################

################################################################################
#####################DEMOGRAPHIC DATA COMPILATION###############################
################################################################################

# This data is gathered from multiple sources over multiple years. I break this
# down into individual variables, and I try to get as many years as possible.
# This often requires getting data from multiple sources for different years of
# the same variable.
#
# Each variable will be one column and are all measured at the state level:
# Percent population with 4-year degree
# Percent evangelical
# Infant mortality
# Maternal mortality
# Percent white
# Percent population living in urban area

################################################################################
# join_and_sav(x)
# This function takes the given df, prepares it to be joined to the existing
# gutt data, joins them, then saves the modified gutt df to csv
#
# Input: x is df with variables to be added
# Returns: saves df_no_index.csv
def join_and_sav(x):
    x.sort_values(['State', 'Year'], inplace=True)
    x.set_index(['State', 'Year'], inplace=True)
    gutt_df = pd.read_csv('/home/jaala/win-Python/Projects/Abortion/data/df_no_index.csv')
    gutt_df.set_index(['State', 'Year'], inplace=True)
    gutt_df = gutt_df.join(x, on=['State', 'Year'], how='outer')
    df_no_index = gutt_df.reset_index()
    df_no_index.to_csv('/home/jaala/win-Python/Projects/Abortion/data/df_no_index.csv', index=False)


checking = pd.read_csv('/home/jaala/win-Python/Projects/Abortion/data/df_no_index.csv')

checking.Abortion_Rate_Occurence.isna().sum()

checking.columns

grouped = checking.groupby(['State', 'Year'])



grouped['Abortion_Rate_Occurence']
###############################EDUCATION
###############################Source: Population Reference Bureau
###############################(Sourced from Census Bureau and American
###############################Community Survey)

###### Percent of adults 25 and older who have completed a Bachelor's Degree or
###### higher

df_educ = pd.read_csv('/home/jaala/win-Python/Projects/Abortion/data/educ_2000_2017_prb.csv',
   header=3, nrows=153)

df_educ['Year'] = df_educ.TimeFrame.apply(lambda x: x[:4])

df_educ.Year = pd.to_numeric(df_educ.Year)

df_educ.rename(columns={'Name': 'State',
   'Data': 'Perc_w_Bachelors'}, inplace=True)

df_educ.drop(['FIPS', 'Type', 'TimeFrame'], axis=1, inplace=True)

join_and_sav(df_educ) # DO NOT REPEAT THIS

###############################EVANGELICAL
###############################Source:
###############################
###############################

######

sav_file = '/home/jaala/win-Python/Projects/Abortion/data/evang_2007_pew_AL_HA.sav'
spio.readsav(sav_file, python_dict=True)
# I NEED TO MAKE USE OF THE savReader Writer MODULE
# https://pypi.org/project/savReaderWriter/

###############################INFANT MORTALITY
########################Source:
########################1990-2004, 2006-2013, 2018 - United Health Foundation
########################(Sourced from America's Health Rankings)
########################2005, 2014-2018 - National Center for Health Statistics

###### Number of infant deaths per 1,000 live births

imu_dict = {}
directory_str = "/home/jaala/win-Python/Projects/Abortion/data/infant_mortality_uhf/"
for file in os.listdir(directory_str):
    name = os.path.splitext(file)[0]
    imu_dict[name] = pd.read_csv(os.path.join(directory_str, file), \
    header=0, names=['Year', 'Measure', 'State', 'Infant_Mortality'], usecols=[0, 2, 3, 5], \
    dtype={'Year': 'int64', 'Infant_Mortality': 'float64'})

df_im_1990 = imu_dict['infant_mortality_1990_UHF']
df_im_1991 = imu_dict['infant_mortality_1991_UHF']
df_im_1992 = imu_dict['infant_mortality_1992_UHF']
df_im_1993 = imu_dict['infant_mortality_1993_UHF']
df_im_1994 = imu_dict['infant_mortality_1994_UHF']
df_im_1995 = imu_dict['infant_mortality_1995_UHF']
df_im_1996 = imu_dict['infant_mortality_1996_UHF']
df_im_1997 = imu_dict['infant_mortality_1997_UHF']
df_im_1998 = imu_dict['infant_mortality_1998_UHF']
df_im_1999 = imu_dict['infant_mortality_1999_UHF']
df_im_2000 = imu_dict['infant_mortality_2000_UHF']
df_im_2001 = imu_dict['infant_mortality_2001_UHF']
df_im_2002 = imu_dict['infant_mortality_2002_UHF']
df_im_2003 = imu_dict['infant_mortality_2003_UHF']
df_im_2004 = imu_dict['infant_mortality_2004_UHF']
df_im_2006 = imu_dict['infant_mortality_2006_UHF']
df_im_2007 = imu_dict['infant_mortality_2007_UHF']
df_im_2008 = imu_dict['infant_mortality_2008_UHF']
df_im_2009 = imu_dict['infant_mortality_2009_UHF']
df_im_2010 = imu_dict['infant_mortality_2010_UHF']
df_im_2011 = imu_dict['infant_mortality_2011_UHF']
df_im_2012 = imu_dict['infant_mortality_2012_UHF']
df_im_2013 = imu_dict['infant_mortality_2013_UHF']
df_im_2018 = imu_dict['infant_mortality_2018_UHF']

im_uhf_df = [df_im_1990, df_im_1991, df_im_1992, df_im_1993, df_im_1994,
    df_im_1995, df_im_1996, df_im_1997, df_im_1998, df_im_1999, df_im_2000,
    df_im_2001, df_im_2002, df_im_2003, df_im_2004, df_im_2006, df_im_2007,
    df_im_2008, df_im_2009, df_im_2010, df_im_2011, df_im_2012, df_im_2013,
    df_im_2018]

for i in im_uhf_df:
    i.drop(i[i.Measure != 'Infant Mortality'].index, inplace=True)
    i.drop('Measure', axis=1, inplace=True)


infant_mortality_uhf_df = pd.concat(im_uhf_df)

im_nchs_list = []
i = 0
directory_str_nchs = "/home/jaala/win-Python/Projects/Abortion/data/infant_mortality_nchs/"
for file in os.listdir(directory_str_nchs):
    df_i = pd.read_csv(os.path.join(directory_str_nchs, file), \
    names=['State', 'Infant_Mortality'], usecols=[0, 1], \
    dtype={'Infant_Mortality': 'float64'}, header=0)
    im_nchs_list.append(df_i)
    i = i + 1

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}
state_codes_invert = {v: k for k, v in us_state_abbrev.items()}

years_nchs = [2005, 2014, 2015, 2016, 2017]

im_nchs_list[0]

# I'm not getting this nest loop right
for i, j in zip(im_nchs_list, years_nchs):
    i['Year'] = j
    i.replace({'State': state_codes_invert}, inplace=True)

infant_mortality_nchs_df = pd.concat(im_nchs_list)

infant_mortality_df = pd.concat([infant_mortality_nchs_df, infant_mortality_uhf_df])

join_and_sav(infant_mortality_df)

###############################MATERNAL MORTALITY
########################Source:
########################2016, 2018 - United Health Foundation
########################(Sourced from America's Health Rankings)
########################1968-2016 - Center for Disease Control
########################https://wonder.cdc.gov/wonder/help/cmf.html


###### Number of maternal deaths per 100,000 persons in population during period
###### of measurement

# So I'm not happy with these measures as the time period varies, which prohibits
# easy comparison. As such I'm looking into how to make use of raw vital Statistics
# data.
# this might be useful: https://gist.github.com/SohierDane/0f2cf7a8538ca35431dd7575ac38e7ca
# Or https://github.com/Quartz/vital-mortality

maternal_mort_ds = ['maternal_mortality_1968_1978_nchs',
    'maternal_mortality_1979_1998_nchs',
    'maternal_mortality_1999_2016_nchs']
mat_mort_dfs = []
for i in maternal_mort_ds:
    df_i = pd.read_csv('/home/jaala/win-Python/Projects/Abortion/data/{}.txt'.format(i), \
        sep='\t', usecols=[1, 5], names=['State', 'Maternal_Mortality_Rate'], \
        header=0, nrows=51)
    mat_mort_dfs.append(df_i)

years_cdc = [1968, 1979, 1999]

for i, j in zip(mat_mort_dfs, years_cdc):
    i['Year'] = j
    i.Maternal_Mortality_Rate = pd.to_numeric(i.Maternal_Mortality_Rate, errors='coerce')


mat_mort_2010_2014 = pd.read_csv('/home/jaala/win-Python/Projects/Abortion/data/maternal_mortality_2016_uhf.csv', \
    header=0, names=['Year', 'State', 'Maternal_Mortality_Rate'], usecols=[0, 3, 5], \
    dtype={'Year': 'int64', 'Maternal_Mortality_Rate': 'float64'}, skiprows=15880, \
    nrows=52)


mat_mort_2011_2015 = pd.read_csv('/home/jaala/win-Python/Projects/Abortion/data/maternal_mortality_2018_uhf.csv', \
    header=0, names=['Year', 'State', 'Maternal_Mortality_Rate'], usecols=[0, 3, 5], \
    dtype={'Year': 'int64', 'Maternal_Mortality_Rate': 'float64'}, skiprows=13228, \
    nrows=52)

mat_mort_2010_2014['Year'] = 2010
mat_mort_2011_2015['Year'] = 2011

mat_mort_concat = pd.concat(mat_mort_dfs)

mat_recent = pd.concat([mat_mort_2010_2014, mat_mort_2011_2015])

pd.concat([mat_mort_concat, mat_recent])



###############################POPULATION
########################Source:
########################2000-2017 - Population Research Bureau

tot_pop_df = pd.read_csv('/home/jaala/win-Python/Projects/Abortion/data/tot_pop_2000_2017_prb.csv', \
    names=['State', 'Year', 'Total_Population'], usecols=[1, 3, 4], \
    dtype={'Year': 'int64', 'Total_Population': 'int64'}, header=0)

join_and_sav(tot_pop_df)


###############################POVERTY
########################Source:
########################1999-2017 - Population Research Bureau

###### Percent of population living in poverty

poverty_df = pd.read_csv('/home/jaala/win-Python/Projects/Abortion/data/poverty_1999_2017_prb.csv', \
    names=['State', 'Year', 'Per_Poverty'], usecols=[1, 3, 4], \
    header=0)

poverty_df['Year'] = poverty_df.Year.apply(lambda x: x[0:4])
poverty_df['Year'] = pd.to_numeric(poverty_df.Year)

join_and_sav(poverty_df)

###############################RACE
########################Source:
########################2000 - Census

######

# FOR SOME REASON ALL MY YEAR ROWS ARE SHOWING 1950, WHICH CAN'T BE CORRECT.
# AM REDOWNLOADING DATA

ipums_race_df.head()

ipums_rejoined.tail()

ipums_race_df_sample =pd.read_csv('/home/jaala/win-Python/Projects/Abortion/data/ipums_demo_various.csv', \
    names=['Year', 'Region', 'State', 'Per_Urban', 'Mean_Num_Veh', 'Hisp', 'Race', 'Educ', 'Poverty'], \
    usecols=[0, 5, 6, 7, 9, 12, 14, 16, 18], header=0, nrows=500000, \
    dtype={'Race': 'category', 'Hisp': 'int64', 'State': 'category', 'Region': 'category', 'Per_Urban': 'float64'})

race_column = ipums_race_df_sample['Race']

dummies = pd.get_dummies(race_column, prefix='race')

ipums_rejoined = ipums_race_df_sample.join(dummies)
ipums_rejoined['Hisp_1'] = ipums_rejoined['Hisp'].apply(lambda x: 1 if (x > 0 ) and (x != 9) else 0)
ipums_rejoined['Educ_1'] = ipums_rejoined['Educ'].apply(lambda x: 1 if x > 9 else 0)

ipums_grped = ipums_rejoined.groupby(['State', 'Year'])[['Per_Urban', 'Mean_Num_Veh', 'Educ_1', 'Poverty', 'race_1', 'race_2', 'race_3', 'race_4', 'Hisp_1']].mean()

ipums_race_df = dd.read_csv('/home/jaala/win-Python/Projects/Abortion/data/ipums_demo_various.csv', \
    names=['Year', 'State', 'Per_Urban', 'Mean_Num_Veh', 'Hisp', 'Race', 'Educ_1', 'Per_Poverty'], \
    usecols=[0, 6, 7, 9, 12, 14, 16, 18], header=0, blocksize=25e6, \
    dtype={'Race': 'category', 'Hisp': 'category', 'State': 'category', 'Region': 'category', 'Per_Urban': 'float64'})


race_column = ipums_race_df['Race']
dummies = dd.get_dummies(race_column.to_frame().categorize(), prefix='race')
ipums_rejoined = ipums_race_df.join(dummies)
ipums_rejoined['Per_Hisp'] = ipums_rejoined['Hisp'].apply(lambda x: 1 if (x > 0 ) and (x != 9) else 0, meta=('float'))
ipums_rejoined['Perc_w_Bachelors'] = ipums_rejoined['Educ_1'].apply(lambda x: 1 if x > 9 else 0, meta=('float'))
ipums_grped =
ipums_rejoined.groupby(['State', 'Year'])[['Per_Urban', 'Mean_Num_Veh', 'Perc_w_Bachelors', 'Per_Poverty', 'race_1', 'race_2', 'race_3', 'race_4', 'race_5', 'Per_Hisp']].mean()

ipums_df = ipums_grped.compute()


#df_ipums

ipums_grped['race_1'].describe()


################################################################################
#####################LEGISCAN DATA COMPILATION################################
################################################################################

# Legiscan (https://legiscan.com/legiscan) provides detailed information about
# legislative events for each state for multiple years. I want to bring this
# information into Python, parse it to code for anti- or pro- abortion
# legislation introduced, voted out of committee, passed by one branch, etc.
#
# The first step is using the LegiScan API in order to obtain this data.


requests.get(
    'https://api.legiscan.com/?key=60c925507ef9c23462c1a91b581aa1c1&op=getDatasetList&id=1468&state=ALABAMA'). \
    json()


requests.get('https://api.legiscan.com/?key=60c925507ef9c23462c1a91b581aa1c1&op=getDataset&id=1661&access_key=5dAREvxZLLvgPProw2nDmm')

# I am independent research pro and anti abortion organizations (or chapters) within each state and compiling these into a
# separate dataset.

organizations = df.DataFrame({
    'State': ['Alabama'],
    'Name_of_Group': [''],
    'Year_formed': [0],
    'Year_dissolved': [0],
    'Anti_abortion': True
})


# In[100]:


#I'm bringing in data from other sources here

# legiscan 60c925507ef9c23462c1a91b581aa1c1

#datasets_alabama = requests.get(
    'https://api.legiscan.com/?key=60c925507ef9c23462c1a91b581aa1c1&op=getDatasetList&id=1468&state=ALABAMA').
    json()

#datasets_alabama = datasets_alabama['datasetlist']

alabama_session_id = []
alabama_year_start = []
alabama_year_end = []
alabama_dataset_hash = []
alabama_access_key = []

for i in datasets_alabama:
    alabama_session_id.append(i['session_id'])
    alabama_year_start.append(i['year_start'])
    alabama_year_end.append(i['year_end'])
    alabama_dataset_hash.append(i['dataset_hash'])
    alabama_access_key.append(i['access_key'])

alabama_sets = []
def get_alabama_sets():
    """none yet"""
    for i in len(alabama_session_id):
        alabama_i = requests.get/
        ('https://api.legiscan.com/?key=60c925507ef9c23462c1a91b581aa1c1&op=getDataset&id='/
        alabama_session_id[i]'&access_key='alabama_access_key[i]).json()
        alabama_sets.append(alabama_i)



#r = requests.get('https://api.legiscan.com/?key=60c925507ef9c23462c1a91b581aa1c1&op=getDataset&id=1468&access_key=1yJHafJalhE8M7BkAV89JO').json()

#dict_r = r['dataset']
#z = dict_r['zip']
#zipfile.ZipFile.writestr('/zipped.zip', z)



#get https://api.legiscan.com/?key=60c925507ef9c23462c1a91b581aa1c1&op=getDataset&id=1468&access_key=1yJHafJalhE8M7BkAV89JO


# In[99]:


alabama_session_id


# In[5]:


###################################################################################################################
###########################ALABAMA#################################################################################
###################################################################################################################

alabama = pd.DataFrame({
    'Year': [2018],
    'State': ['Alabama'],
    'Percent_R_in_State_Gov': [0.74],
    'Anti_Laws_Intro': []
})


# In[ ]:

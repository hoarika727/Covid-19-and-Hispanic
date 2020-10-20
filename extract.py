import os
from zipfile import ZipFile
from datetime import datetime 
import pandas as pd
import numpy as np
import re

folder = '/Users/kayinho/git/hispanic/'
extension = ".zip"

def unzip_all(dir):
    for item in os.listdir(dir):
        if item.endswith(extension):
            path = folder+item
            with ZipFile(path,'r') as zip_ref:
                zip_ref.extractall('data')

unzip_all(os.path.join(folder,'zipped_data/'))

def modify_unwanted(dir):
    for item in os.listdir(dir):
        if (item.endswith('txt')) or ('metadata' in item):
            path = dir+item
            os.remove(path)
        if (item.startswith('ACS')):
            name = item.split('_')
            newName = dir+name[0]+'.csv'
            os.rename(os.path.join(dir,item), os.path.join(dir,newName))


datafolder = '/Users/kayinho/git/hispanic/data/'
modify_unwanted(datafolder)

chiZCTA = 'data/CityofChicago_Zip_Codes.csv'
zipCodeData = pd.read_csv(os.path.join(folder,chiZCTA), sep=',', header=0)
chiZC = pd.DataFrame(zipCodeData['ZIP'].unique().astype(str), columns=[('Zip Code','Chicago')]).astype('string')

population_all = 'data/ACSDP5Y2018.DP05.csv'
population = 'data/ACSDT5Y2018.B03003.csv'
healthcare = 'data/ACSDT5Y2018.C27001I.csv'
immigrant = 'data/ACSDT5Y2018.B05003I.csv'
language = 'data/ACSDT5Y2018.B16005I.csv'
jobs = 'data/ACSDT5Y2018.C24010I.csv'
transportation = 'data/ACSDT5Y2018.B08105I.csv'
relative = 'data/ACSDT5Y2018.B11002I.csv'
grandparents = 'data/ACSDT5Y2018.B10051I.csv'
occupants = 'data/ACSDT5Y2018.B25014I.csv'
income = 'data/ACSDT5Y2018.B19001I.csv'
foodstamp = 'data/ACSDT5Y2018.B22005I.csv'
poverty = 'data/ACSDT5Y2018.B17020I.csv'


def filter_for_CHI(file):
    df = pd.read_csv(os.path.join(folder,file),sep=',',header=[0,1])
    df[('NAME','Geographic Area Name')] = df[('NAME','Geographic Area Name')].astype('string')
    for i in range(len(df)):
        df[('NAME','Geographic Area Name')][i] = df[('NAME','Geographic Area Name')][i].replace('ZCTA5 ','')
    chi_df = pd.merge(chiZC,df,'left', left_on=[('Zip Code','Chicago')], right_on=[('NAME','Geographic Area Name')], left_index=False)
    chi_df.columns = df.columns.insert(loc = 0, item=('Zip Code','Chicago'))
    chi_df = chi_df.sort_values(by=[('Zip Code','Chicago')])
    return chi_df

population_all_chi_df = filter_for_CHI(os.path.join(folder,population_all))
#population_all_chi_df.to_csv(os.path.join(datafolder,'CHI_DP05.csv'), index = False)
population_all_chi_df
population_chi_df = filter_for_CHI(os.path.join(folder,population))
#population_chi_df.to_csv(os.path.join(datafolder,'CHI_B03003.csv'), index = False)

healthcare_chi_df = filter_for_CHI(os.path.join(folder,healthcare))
#healthcare_chi_df.to_csv(os.path.join(datafolder,'CHI_C27001I.csv'), index = False)

immigrant_chi_df = filter_for_CHI(os.path.join(folder,immigrant))
#immigrant_chi_df.to_csv(os.path.join(datafolder,'CHI_B05003I.csv'), index = False)

language_chi_df = filter_for_CHI(os.path.join(folder,language))
#language_chi_df.to_csv(os.path.join(datafolder,'CHI_B16005I.csv'), index = False)

jobs_chi_df = filter_for_CHI(os.path.join(folder,jobs))
#jobs_chi_df.to_csv(os.path.join(datafolder,'CHI_C24010I.csv'), index = False)

transportation_chi_df = filter_for_CHI(os.path.join(folder,transportation))
#transportation_chi_df.to_csv(os.path.join(datafolder,'CHI_B08105I.csv'), index = False)

relative_chi_df = filter_for_CHI(os.path.join(folder,relative))
#relative_chi_df.to_csv(os.path.join(datafolder,'CHI_B11002I.csv'), index = False)

grandparents_chi_df = filter_for_CHI(os.path.join(folder,grandparents))
#grandparents_chi_df.to_csv(os.path.join(datafolder,'CHI_B10051I.csv'), index = False)

occupants_chi_df = filter_for_CHI(os.path.join(folder,occupants))
#occupants_chi_df.to_csv(os.path.join(datafolder,'CHI_B25014I.csv'), index = False)

income_chi_df = filter_for_CHI(os.path.join(folder,immigrant))
#income_chi_df.to_csv(os.path.join(datafolder,'CHI_B19001I.csv'), index = False)

foodstamp_chi_df = filter_for_CHI(os.path.join(folder,immigrant))
#foodstamp_chi_df.to_csv(os.path.join(datafolder,'CHI_B22005I.csv'), index = False)

poverty_chi_df = filter_for_CHI(os.path.join(folder,immigrant))
#poverty_chi_df.to_csv(os.path.join(datafolder,'CHI_B17020I.csv'), index = False)







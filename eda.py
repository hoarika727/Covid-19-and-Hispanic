import os
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

folder = '/Users/kayinho/git/hispanic/'

population_all = 'data/CHI_DP05.csv'
population = 'data/CHI_B03003.csv'
healthcare = 'data/CHI_C27001I.csv'
immigrant = 'data/CHI_B05003I.csv'
language = 'data/CHI_B16005I.csv'
jobs = 'data/CHI_C24010I.csv'
transportation = 'data/CHI_B08105I.csv'
relative = 'data/CHI_B11002I.csv'
grandparents = 'data/CHI_B10051I.csv'
occupants = 'data/CHI_B25014I.csv'
income = 'data/CHI_B19001I.csv'
foodstamp = 'data/CHI_B22005I.csv'
poverty = 'data/CHI_B17020I.csv'

healthcare_df = pd.read_csv(os.path.join(folder,healthcare),sep=',',header=1)
healthcare_df = healthcare_df.dropna()
col = healthcare_df.columns
healthcare_df[col[2:]] = healthcare_df[col[2:]].apply(np.int64)
dropCol = []
for i in col:
    match = re.search(r"Margin.*",i)
    if match:
        dropCol.append(i)
dropCol.extend(['Chicago'])

healthcare_total = healthcare_df.drop(dropCol, axis=1)

fig = plt.figure(figsize=(40,15))
xtickVals = tuple(healthcare_total['Geographic Area Name'])
x_pos = np.arange(len(xtickVals))
plt.bar(x_pos,healthcare_total['Estimate!!Total'])
plt.xticks(x_pos,xtickVals, fontsize=12,rotation=20)
plt.yticks(fontsize=15)
plt.title('Total number of records in healthcare coverage data set (C27001I)', fontsize=30, pad=10)
plt.show()
#plt.savefig('/graphs/HIC_records_C27001I')

healthcare_y = np.add(np.add(healthcare_total['Estimate!!Total!!Under 19 years!!With health insurance coverage'], \
                    healthcare_total['Estimate!!Total!!19 to 64 years!!With health insurance coverage']),
                    healthcare_total['Estimate!!Total!!65 years and over!!With health insurance coverage'])
healthcare_n = np.add(np.add(healthcare_total['Estimate!!Total!!Under 19 years!!No health insurance coverage'], \
                    healthcare_total['Estimate!!Total!!19 to 64 years!!No health insurance coverage']),
                    healthcare_total['Estimate!!Total!!65 years and over!!No health insurance coverage'])
healthcare_total.insert(3,"Total_w_HIC",healthcare_y)
healthcare_total.insert(4,"Total_wo_HIC",healthcare_n)

healthcare_y_pop_18pc = np.divide(healthcare_total['Estimate!!Total!!Under 19 years!!With health insurance coverage'],healthcare_total['Total_w_HIC'])
healthcare_y_pop_1965pc = np.divide(healthcare_total['Estimate!!Total!!19 to 64 years!!With health insurance coverage'],healthcare_total['Total_w_HIC'])
healthcare_y_pop_66pc = np.divide(healthcare_total['Estimate!!Total!!65 years and over!!With health insurance coverage'],healthcare_total['Total_w_HIC'])

healthcare_y_18pc = np.divide(healthcare_total['Estimate!!Total!!Under 19 years!!With health insurance coverage'],healthcare_total['Estimate!!Total!!Under 19 years'])
healthcare_y_1965pc = np.divide(healthcare_total['Estimate!!Total!!19 to 64 years!!With health insurance coverage'],healthcare_total['Estimate!!Total!!19 to 64 years'])
healthcare_y_66pc = np.divide(healthcare_total['Estimate!!Total!!65 years and over!!With health insurance coverage'],healthcare_total['Estimate!!Total!!65 years and over'])

healthcare_n_pop_18pc = np.divide(healthcare_total['Estimate!!Total!!Under 19 years!!No health insurance coverage'],healthcare_total['Total_wo_HIC'])
healthcare_n_pop_1965pc = np.divide(healthcare_total['Estimate!!Total!!19 to 64 years!!No health insurance coverage'],healthcare_total['Total_wo_HIC'])
healthcare_n_pop_66pc = np.divide(healthcare_total['Estimate!!Total!!65 years and over!!No health insurance coverage'],healthcare_total['Total_wo_HIC'])

healthcare_n_18pc = np.divide(healthcare_total['Estimate!!Total!!Under 19 years!!No health insurance coverage'],healthcare_total['Estimate!!Total!!Under 19 years'])
healthcare_n_1965pc = np.divide(healthcare_total['Estimate!!Total!!19 to 64 years!!No health insurance coverage'],healthcare_total['Estimate!!Total!!19 to 64 years'])
healthcare_n_66pc = np.divide(healthcare_total['Estimate!!Total!!65 years and over!!No health insurance coverage'],healthcare_total['Estimate!!Total!!65 years and over'])

healthcare_total.insert(12,'above_65_wo_HIC%',healthcare_n_66pc)
healthcare_total.insert(12,'above_65_w_HIC%',healthcare_y_66pc)

healthcare_total.insert(9,'19_65_wo_HIC%',healthcare_n_1965pc)
healthcare_total.insert(9,'19_65_w_HIC%',healthcare_y_1965pc)

healthcare_total.insert(6,'under_19_wo_HIC%',healthcare_n_18pc)
healthcare_total.insert(6,'under_19_w_HIC%',healthcare_y_18pc)

healthcare_total.insert(5,'above_65_wo_HIC_pop%',healthcare_n_pop_66pc)
healthcare_total.insert(5,'19_65_wo_HIC_pop%',healthcare_n_pop_1965pc)
healthcare_total.insert(5,'under_19_wo_HIC_pop%',healthcare_n_pop_18pc)

healthcare_total.insert(4,'above_65_w_HIC_pop%',healthcare_y_pop_66pc)
healthcare_total.insert(4,'19_65_w_HIC_pop%',healthcare_y_pop_1965pc)
healthcare_total.insert(4,'under_19_w_HIC_pop%',healthcare_y_pop_18pc)

#mincol = healthcare_total.columns
#mincol

#healthcare_total.to_csv(os.path.join(folder,'data/healthcare_summary.csv'), index = False)

fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(figsize=(20,20),ncols=2,nrows=2)
barWidth = 0.85

ax1.bar(x_pos,healthcare_total['Total_w_HIC'])
ax1.set_xticks(x_pos)
ax1.set_xticklabels(xtickVals, fontsize=6, rotation=90)
ax1.set_title('%Hispanic Population with Healthcare Insurance Coverage per Chicago Zip Code')

gBar_w = [i * 100 for i in healthcare_total['under_19_w_HIC%']]
gBar_wo = [i * 100 for i in healthcare_total['under_19_wo_HIC%']]
ax2.bar(x_pos,gBar_wo, label = 'Under 19 Years without HIC', color='#008000', edgecolor='white', width=barWidth)
ax2.bar(x_pos, gBar_w, label = 'Under 19 Years with HIC', bottom=gBar_wo, color='#b5ffb9', edgecolor='white', width=barWidth)
ax2.set_xticks(x_pos)
ax2.set_xticklabels(xtickVals, fontsize=6, rotation=90)
ax2.set_ylabel("Population percentage (%)")
ax2.legend(loc = 0)
ax2.set_title('Under 19 Years with & without Health Insurace Coverage')

oBar_w = [i * 100 for i in healthcare_total['19_65_w_HIC%']]
oBar_wo = [i * 100 for i in healthcare_total['19_65_wo_HIC%']]
ax3.bar(x_pos, oBar_wo, label = '19-65 Years without HIC', color='#ff8c00', edgecolor='white', width=barWidth)
ax3.bar(x_pos, oBar_w, label = '19-65 Years with HIC', bottom=oBar_wo, color='#f9bc86', edgecolor='white', width=barWidth)
ax3.set_xticks(x_pos)
ax3.set_xticklabels(xtickVals, fontsize=6, rotation=90)
ax3.set_ylabel("Population percentage (%)")
ax3.legend(loc = 0)
ax3.set_title('19 and 65 Years with & without Health Insurace Coverage')

bBar_w = [i * 100 for i in healthcare_total['above_65_w_HIC%']]
bBar_wo = [i * 100 for i in healthcare_total['above_65_wo_HIC%']]
ax4.bar(x_pos, bBar_wo, label = 'Above 65 Years without HIC', color='#00008b', edgecolor='white', width=barWidth)
ax4.bar(x_pos, bBar_w, label = 'Above 65 Years with HIC', bottom=bBar_wo, color='#a3acff', edgecolor='white', width=barWidth)
ax4.set_xticks(x_pos)
ax4.set_xticklabels(xtickVals, fontsize=6, rotation=90)
ax4.set_ylabel("Population percentage (%)")
ax4.legend(loc = 0)
ax4.set_title('Above 65 Years with & without Health Insurace Coverage')

plt.suptitle('Hispanic Population in Chicago with Healthcare Insurance Coverage', fontsize=25)
plt.show()
#plt.savefig('/graphs/HIC_age')

fig, (ax1,ax2) = plt.subplots(figsize=(20,10),nrows=1, ncols=2)
# transform the ratio
greenBars = [i * 100 for i in healthcare_total['under_19_w_HIC_pop%']]
orangeBars = [i * 100 for i in healthcare_total['19_65_w_HIC_pop%']]
blueBars = [i * 100 for i in healthcare_total['above_65_w_HIC_pop%']]

# plot
ax1.bar(x_pos, greenBars, label = 'Under 19 Years with HIC', color='#b5ffb9', edgecolor='white', width=barWidth)
ax1.bar(x_pos, orangeBars, label = '19-65 Years with HIC', bottom=greenBars, color='#f9bc86', edgecolor='white', width=barWidth)
ax1.bar(x_pos, blueBars, label = 'Above 65 Years with HIC', bottom=[i+j for i,j in zip(greenBars, orangeBars)], color='#a3acff', edgecolor='white', width=barWidth)
 
# Custom x axis
ax1.set_xticks(x_pos)
ax1.set_xticklabels(xtickVals, fontsize=7, rotation=90)
#ax1.set_yticks(fontsize=20)
ax1.set_xlabel("zip code")
ax1.set_ylabel("Population percentage (%)")
ax1.legend()
ax1.set_title("%Hispanic Population in age groups with Health Insurance Coverage")

greenBars1 = [i * 100 for i in healthcare_total['under_19_wo_HIC_pop%']]
orangeBars1 = [i * 100 for i in healthcare_total['19_65_wo_HIC_pop%']]
blueBars1 = [i * 100 for i in healthcare_total['above_65_wo_HIC_pop%']]

ax2.bar(x_pos, greenBars1, label = 'Under 19 Years without HIC', color='#b5ffb9', edgecolor='white', width=barWidth)
ax2.bar(x_pos, orangeBars1, label = '19-65 Years without HIC', bottom=greenBars1, color='#f9bc86', edgecolor='white', width=barWidth)
ax2.bar(x_pos, blueBars1, label = 'Above 65 Years without HIC', bottom=[i+j for i,j in zip(greenBars1, orangeBars1)], color='#a3acff', edgecolor='white', width=barWidth)
 
# Custom x axis
ax2.set_xticks(x_pos) #, rotation = 75
ax2.set_xticklabels(xtickVals, fontsize=7, rotation=90)
ax2.set_xlabel("zip code")
ax2.set_ylabel("Population percentage (%)")
ax2.legend()
ax2.set_title("%Hispanic Population in age groups w/out Health Insurance Coverage")
plt.show()
#plt.savefig('/graphs/HIC_with&without')



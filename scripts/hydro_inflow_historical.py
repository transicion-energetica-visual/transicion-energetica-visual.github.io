# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
from matplotlib import cm

cmp = cm.get_cmap('BrBG', 256)

plt.style.use('seaborn-ticks')
plt.rcParams['axes.labelsize'] = 20
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

plt.rcParams['axes.titlesize'] = 16
plt.figure(figsize=(10, 10))
gs1 = gridspec.GridSpec(2, 1)
gs1.update(wspace=0.2, hspace=0.2)
ax1 = plt.subplot(gs1[0,0])
#https://www.ree.es/es/datos/generacion/estructura-generacion 
inflow_df=pd.read_csv('../data/REE/9_Datos_hidraulicos_06_2020.csv', index_col=1,  
                      skiprows=range(0,1), 
                      nrows=2, encoding='latin1', sep=';')
#months names in Spanish
dic_month={1:'ene', 2:'feb', 3:'mar', 4:'abr', 5:'may', 6:'jun',
           7:'jul', 8:'ago', 9:'sep', 10:'oct', 11:'nov', 12:'dic'}

dic_days={1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 
          12:31 }

dic_year={}
years=np.arange(1991,2019)
for year in years:
    dic_year[year]=str(year)[-2:]
months=np.arange(1,13)
     
inflow = pd.DataFrame(
            index=pd.Series(
                data = months,
                name = 'month'),
            columns = pd.Series(
                data = years, 
                name = 'year')
            )
            
for year in years:
    for month in months:
        # the historical datafile is a mess (e.g, value of 1.452  means inflow 
        # is 1452 but value 565 means inflow is 565)
        value=float(inflow_df.loc['Producible hidraulico (GWh)', 
                                  dic_month[month] + '-' + dic_year[year]])
        if value < 10: 
            inflow.loc[month, year]= value*1000 
        else:
            inflow.loc[month, year]= value  
    ax1.plot(inflow[year], color='dodgerblue', alpha=0.5, linewidth=2)
ax1.set_xticks(list(months))
ax1.set_xticklabels([dic_month[month] for month in months], fontsize=18)
ax1.set_ylabel('monthly inflow (GWh)', fontsize=18)    
plt.savefig('../figures/inflow_historical.png', dpi=300, bbox_inches='tight')  


plt.figure(figsize=(10, 5))
gs1 = gridspec.GridSpec(1, 13)
gs1.update(wspace=0.2, hspace=0.2)
ax1 = plt.subplot(gs1[0,0])
norm=mpl.colors.Normalize(0.5, 1.54) #green for values <2%

ax1 = plt.subplot(gs1[0,0:12])
normalized=inflow.sum(axis=0)/np.mean(inflow.sum(axis=0))
#month_s=8
#normalized=[float(i) for i in inflow.loc[month_s]]/np.mean(inflow.loc[month_s])
ax1.pcolor(np.array(normalized).reshape((1,len(years))), cmap=cmp, norm=norm)
ax1.set_yticks([])
ax1.set_xticks(range(0,len(years)))
ax1.set_xticklabels(list(years), fontsize=16, rotation=45)

# legend
ax11 = plt.subplot(gs1[0,12])
cb1=mpl.colorbar.ColorbarBase(ax11, cmap=cmp, norm=norm, 
                              orientation='vertical')
ax11.xaxis.tick_top()
ax11.set_yticks([0.5, 0.75, 1.0, 1.25, 1.5])
ax11.set_yticklabels(['-50%', '-25%', 'average', '+25%', '+50%'], 
                    fontsize=18)
ax1.set_title('inflow (variation with respect to average)', fontsize=18)
plt.savefig('../figures/inflow_variation.png', dpi=300, bbox_inches='tight')  

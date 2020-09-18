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
from matplotlib.colors import ListedColormap

# define new colormap including green for zero values
Greys = cm.get_cmap('Greys', 256)
newcolors = Greys(np.linspace(0, 1, 256))
green = np.array([0/256, 256/256, 0/256, 1])
newcolors[:52, :] = green #green for values <20% 
newcmp = ListedColormap(newcolors)


plt.style.use('seaborn-ticks')
plt.rcParams['axes.labelsize'] = 20
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

plt.rcParams['axes.titlesize'] = 16
plt.figure(figsize=(120, 8))
gs1 = gridspec.GridSpec(30, 21)
gs1.update(wspace=0.2, hspace=0.2)

emi_df=pd.read_csv('../data/emisiones.csv', index_col=0, header=None, 
                   encoding='latin1')
emi_t=pd.Series(index=emi_df.index, data=emi_df[1])
norm=mpl.colors.Normalize(0, 0.32) #green for values <2%
years=[str(year) for year in range(2014,2021)]
for i,year in enumerate(years):
    #https://www.ree.es/es/datos/generacion/estructura-generacion 
    df=pd.read_csv('../data/REE/ESTRUCTURA DE LA GENERACIÓN POR TECNOLOGÍAS_01-01-{}_31-12-{}.csv'.format(year,year),
               skiprows=range(0,4), nrows=13, index_col=0, encoding='latin1')
    df = df.apply(pd.to_numeric, errors='coerce')
    df=df*0.001 #GWh -> MWh
    emi = [  emi_t['Hidraulica']*Hidro 
           + emi_t['Nuclear']*Nuclear
           + emi_t['Carbon']*Carbon
           + emi_t['Ciclocombinado']*Ciclocombinado
           + emi_t['Eolica']*Eolica
           + emi_t['Fotovoltaica']*Fotovoltaica
           + emi_t['Solartermica']*Solartermica
           + emi_t['Cogeneracion']*Cogeneracion
           + emi_t['Termicarenovable']*Termicarenovable
            for Hidro, Nuclear, Carbon, Ciclocombinado, Eolica, Fotovoltaica,
            Solartermica, Cogeneracion, Termicarenovable
            in zip(df.loc['Hidráulica'],
                   df.loc['Nuclear'],
                   df.loc['Carbón'],
                   df.loc['Ciclo combinado'],
                   df.loc['Eólica'],
                   df.loc['Solar fotovoltaica'],
                   df.loc['Solar térmica'],
                   df.loc['Cogeneración'],
                   df.loc['Residuos renovables'])]        
    emi=emi[:365] #drop last day if leap year
    print(max(emi))
    
    if year=='2020':
        ax1 = plt.subplot(gs1[i*3+1:i*3+4,0:1])
        ax1.pcolor(np.array(emi).reshape((1,len(emi))), cmap=newcmp, norm=norm)
        ax1.text(-18, 0.05, year, fontsize=10)
    else:
        ax1 = plt.subplot(gs1[i*3+1:i*3+4,0:2])
        ax1.pcolor(np.array(emi).reshape((1,365)), cmap=newcmp, norm=norm)
        ax1.text(-16, 0.05, year, fontsize=10)
    
    ax1.set_xticks([])
    ax1.set_yticks([])    
    
# legend
ax11 = plt.subplot(gs1[0,0])
cb1=mpl.colorbar.ColorbarBase(ax11, cmap=newcmp, norm=norm, orientation='horizontal')
ax11.xaxis.tick_top()
#ax11.set_xticks([0, 0.05, 0.1, 0.15, 0.2, 0.25])
#ax11.set_xticklabels(['0%', '5%', '10%', '15%', '20%', '25%'], fontsize=14)
ax11.text(0.33, 0.08, 'Emisiones (tCO$_2$/MWh)', fontsize=15)
plt.savefig('../figures/emissions_historical.png', dpi=300, bbox_inches='tight')  
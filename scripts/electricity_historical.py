# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 18:30:45 2020

@author: marta.victoria.perez
"""


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import matplotlib.pylab as pl
import seaborn as sns; sns.set()
sns.set_style('ticks')
plt.style.use('seaborn-ticks')
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 18

#https://www.ree.es/es/datos/generacion/estructura-generacion    
df = pd.read_csv('data/REE/ESTRUCTURA DE LA GENERACIÓN POR TECNOLOGÍAS_01-01-2007_31-12-2019.csv', index_col=0,
                 encoding="latin-1")

df=df/1000 # GWh -> TWh
#df=df/df.sum(axis=0)

plt.figure(figsize=(6, 5))
gs1 = gridspec.GridSpec(1, 1)
ax0 = plt.subplot(gs1[0,0])
ax0.stackplot(np.arange(2007,2020),[df.loc['Carbon'],
                                    df.loc['Fuel + Gas'],
                                    df.loc['Ciclo combinado'],
                                    df.loc['Nuclear'],                                                                     
                                    df.loc['Cogeneracion'],
                                    df.loc['Otras renovables'] +
                                    df.loc['Residuos no renovables'] +
                                    df.loc['Residuos renovables'],
                                    df.loc['Hidraulica'],  
                                    df.loc['Eolica'],
                                    df.loc['Solar termica'],
                                    df.loc['Solar fotovoltaica']], 
                      colors=['black', 'dimgray', 'gray', 'coral',
                               'brown', 'green','yellowgreen', 
                               'dodgerblue','orange', 'gold'], 
                      linewidth=0,
                      labels=['Carbón','Fuel', 'Ciclo combinado', 'Nuclear',
                              'Cogeneración', 
                              'Residuos', #'otras renovables', 'Residuos no renovables', 'Residuos renovables',
                              'Hidráulica', 
                              'Eólica', 'Solar térmica', 'Solar fotovoltaica'], 
                      zorder=-3) 

ax0.set_xlim(2007,2019)
ax0.set_ylabel('Generación eléctrica (TWh)', fontsize=18)
handles, labels = ax0.get_legend_handles_labels()
ax0.legend(reversed(handles), reversed(labels), loc=(1.01,0.02), shadow=True,fancybox=True,prop={'size':18})
plt.savefig('figures/fuentes_generacion_electrica.png', dpi=300, bbox_inches='tight')    
#%%

df=df/df.sum(axis=0) # normalization
plt.figure(figsize=(6, 5))
gs1 = gridspec.GridSpec(1, 1)
ax0 = plt.subplot(gs1[0,0])
ax0.stackplot(np.arange(2007,2020),[df.loc['Carbon'],
                                    df.loc['Fuel + Gas'],
                                    df.loc['Ciclo combinado'],
                                    df.loc['Nuclear'],                                                                     
                                    df.loc['Cogeneracion'],
                                    df.loc['Otras renovables'] +
                                    df.loc['Residuos no renovables'] +
                                    df.loc['Residuos renovables'],
                                    df.loc['Hidraulica'],  
                                    df.loc['Eolica'],
                                    df.loc['Solar termica'],
                                    df.loc['Solar fotovoltaica']], 
                      colors=['black', 'dimgray', 'gray', 'coral',
                               'brown', 'green','yellowgreen', 
                               'dodgerblue','orange', 'gold'], 
                      linewidth=0,
                      labels=['Carbón','Fuel', 'Ciclo combinado', 'Nuclear',
                              'Cogeneración', 
                              'Residuos', #'otras renovables', 'Residuos no renovables', 'Residuos renovables',
                              'Hidráulica', 
                              'Eólica', 'Solar térmica', 'Solar fotovoltaica'], 
                      zorder=-3)   

ax0.set_xlim(2007,2019)
ax0.set_ylim(0,1)
ax0.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax0.set_yticklabels([20, 40, 60, 80, 100])
ax0.set_xticks([2007, 2009, 2011, 2013, 2015, 2017, 2019])
ax0.set_xticklabels([2007, 2009, 2011, 2013, 2015, 2017, 2019])
ax0.set_ylabel('Generación eléctrica (%)', fontsize=18)
handles, labels = ax0.get_legend_handles_labels()
ax0.legend(reversed(handles), reversed(labels), loc=(1.01,0.), shadow=True,fancybox=True,prop={'size':18})
plt.savefig('figures/fuentes_generacion_electrica_100.png', dpi=300, bbox_inches='tight')  






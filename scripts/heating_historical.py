# -*- coding: utf-8 -*-


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

    
base_dir='data/jrc-idees-2015'
plt.figure(figsize=(5, 5))
gs1 = gridspec.GridSpec(1, 1)
ax0 = plt.subplot(gs1[0,0])
ax0.set_xlim(2000,2015)
ax0.set_ylim(0,1)
ax0.set_ylabel('Calefacción (%)', fontsize=18)
ax0.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax0.set_yticklabels([20, 40, 60, 80, 100])

country='ES'

excel_fec = pd.read_excel('{}/JRC-IDEES-2015_Residential_{}.xlsx'.format(base_dir,country), sheet_name='RES_hh_fec', index_col=0, header=0, squeeze=True) # the summary sheet

excel_fec_ter = pd.read_excel('{}/JRC-IDEES-2015_Tertiary_{}.xlsx'.format(base_dir,country), 
                                      sheet_name='SER_hh_fec', index_col=0, header=0, squeeze=True) # the summary sheet

s_fec = excel_fec.iloc[3:13,-16:]
s_fec_ter = excel_fec_ter.iloc[3:13,-16:]

years=np.arange(2000, 2016)
technologies=['gas', 'heat resistors', 'heatpumps', 'geothermal', 
                      'derived heat', 'electricity in circulation', 'solids-liquids']

heat_supply = pd.DataFrame(columns = pd.Series(data=years, name='year'),
                                    index=pd.Series(data=technologies, name='technology'))
                  
heat_supply.loc['geothermal']=(s_fec.loc['Geothermal energy'] + 
                                       s_fec_ter.loc['Geothermal energy'])
        
heat_supply.loc['derived heat']=(s_fec.loc['Derived heat'] +
                                         s_fec_ter.loc['Derived heat'] )

heat_supply.loc['electricity in circulation']=s_fec.loc['Electricity in circulation']
        
heat_supply.loc['other']=heat_supply.loc['geothermal'] + heat_supply.loc['electricity in circulation']

#solids-liquids includs: solids, liquified petroleum gas (LPG), gas/diesel oil. incl. biofuels
heat_supply.loc['solids-liquids']=(s_fec.loc['Solids'] 
                                         + s_fec.loc['Liquified petroleum gas (LPG)'] 
                                         + s_fec.loc['Gas/Diesel oil incl. biofuels (GDO)']+
                                         s_fec_ter.loc['Solids'] 
                                         + s_fec_ter.loc['Liquified petroleum gas (LPG)'] 
                                         + s_fec_ter.loc['Gas/Diesel oil incl. biofuels (GDO)'])

heat_supply.loc['biomass']=(s_fec.loc['Biomass and wastes'] +
                                    s_fec_ter.loc['Biomass and wastes'])
heat_supply.loc['gas']=(s_fec.loc['Gases incl. biogas'] +
                               s_fec_ter.loc['Gas heat pumps']+
                               s_fec_ter.loc['Conventional gas heaters'])

heat_supply.loc['electric boilers']=(s_fec.loc['Conventional electric heating'] +
                                             s_fec_ter.loc['Conventional electric heating'])

heat_supply.loc['heatpumps']=(s_fec.loc['Advanced electric heating'] +
                                      s_fec_ter.loc['Advanced electric heating'])
# normalization
heat_supply=heat_supply/heat_supply.sum(axis=0)

ax1 = plt.subplot(gs1[0,0])        
color_list = pd.read_csv('scripts/color_scheme.csv', sep=',')
color = dict(zip(color_list['tech'].tolist(),
            color_list[' color'].tolist(),))
ax1.set_facecolor(color['geothermal'])
ax1.stackplot(np.arange(2000,2016), [pd.to_numeric(heat_supply.loc['solids-liquids']),
                      pd.to_numeric(heat_supply.loc['gas']),
                      pd.to_numeric(heat_supply.loc['biomass']),
                      pd.to_numeric(heat_supply.loc['electric boilers']),
                      pd.to_numeric(heat_supply.loc['heatpumps']),
                      #pd.to_numeric(heat_supply.loc['derived heat']),
                      pd.to_numeric(heat_supply.loc['other'])], 
                      colors=[color['lignite'], color['gas boiler'], 
                              color['biomass'], color['resistive heater'],
                              color['heat pump'], #color['district heating'],
                              color['geothermal']],
                      linewidth=0,
                      labels=['carbón, petróleo, LPG', 'gas', 'biomasa y residuos',
                           'eléctrico', 'bomba de calor',  
                           'geotérmica y otras'], zorder=-3)      
ax1.tick_params(right=True)        
ax1.set_xlim(2000,2015)
ax1.set_ylim(0,1)
ax1.set_title('Sector residencial y servicios', fontsize=18)
#ax1.set_yticklabels([])
#ax1.set_xticklabels([])

handles, labels = ax1.get_legend_handles_labels()
ax1.legend(reversed(handles), reversed(labels), loc=(1.01,0.15), shadow=True,fancybox=True,prop={'size':18})
plt.savefig('figures/fuentes_sector_residencial_y_servicios.png', dpi=300, bbox_inches='tight')         
 
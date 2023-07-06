'''
Written by Bjørn Gading Solemsli
date: 06.07.2022

Affiliation: iCSI, SMN Catalysis, UiO

'''


from typing import Text
from ipywidgets.widgets.interaction import interactive
from ipywidgets.widgets.widget_float import FloatText
from ipywidgets.widgets.widget_selection import Dropdown
from numpy.core.fromnumeric import size
from numpy.core.function_base import linspace
import pandas as pd
import matplotlib.pyplot as plt
import os
import scipy.signal as spsign

import matplotlib.colors as colors
import numpy as np
import scipy.integrate as sp# trapz, Simps, cumtrapz, romb
import ipywidgets as widgets

from IPython.display import display
from scipy import sparse
from scipy.sparse.linalg import spsolve

class GC_analysis_MTM():

    def __init__(self, *args,**kwargs):
        self.C_factor_DME = 2.34*10**(0)    
        self.C_factor_MeOH = 6.61*10**(-1)





        Main_Direct_GC = r'C:\Users\bjorngso\OneDrive - Universitetet i Oslo\01 Results\Testing\M2M\GC'


        together_GC = list()
        for root, dirs, files in os.walk(Main_Direct_GC, topdown=False):
            for name in files:
                if name[-5:] == '.xlsx':
                    joint = ('{}'.format(name),os.path.join(root,name))
                    together_GC.append(joint)
        
        direct_GC = widgets.Dropdown(options=together_GC,description='GC experiment', disabled=False,layout=widgets.Layout(width='90%'),style = {'description_width': 'initial'})
        w = widgets.interactive(self.reading_GC_files, file_GC= direct_GC)
        display(w)
        

    def reading_GC_files(self,*args,**kwargs):
        fig, (ax1,ax2,ax3) = plt.subplots(1,3,figsize=(14,6))
        Filename_GC = kwargs.get('file_GC', '')
        self.Filename_GC = Filename_GC

        Cu = widgets.FloatText(value=0,description='What is the Copper content? (if N/A give 0)', disabled=False,layout=widgets.Layout(width='90%'),style = {'description_width': 'initial'})
        w1 = widgets.interactive(self.plotting_GC, Cu_content= Cu, fig= widgets.fixed(fig), ax1= widgets.fixed(ax1),ax2= widgets.fixed(ax2),ax3= widgets.fixed(ax3))
        display(w1)

    def plotting_GC(self,*args,**kwargs):
        Cu_content = kwargs.get('Cu_content', 0)
        fig = kwargs.get('fig', False)
        ax1  = kwargs.get('ax1', False)
        ax2  = kwargs.get('ax2', False)
        ax3  = kwargs.get('ax3', False)
        self.Cu_content = Cu_content
        ax3.clear()
        ax2.clear()
        ax3.clear()
        self.data = pd.read_excel(self.Filename_GC,dtype=np.float64)
        CH4 = self.data['Methane'].to_numpy()
        DME_raw = self.data['DME'].to_numpy()
        MeOH_raw = self.data['Metanol'].to_numpy()
        DME = self.data['DME'].to_numpy()/self.C_factor_DME
        MeOH = self.data['Metanol'].to_numpy()/self.C_factor_MeOH

        CH4 = np.insert(CH4, 0, CH4[-1])
        DME = np.insert(DME, 0, DME[-1])
        MeOH = np.insert(MeOH, 0, MeOH[-1])
        DME_raw = np.insert(DME_raw, 0, DME[-1])
        MeOH_raw = np.insert(MeOH_raw, 0, MeOH[-1])

        t = np.array([])

        n = 1

        for i in range(len(CH4)):
            t = np.append(t,n)
            n += 4.416667

        CH4_bkg = np.linspace(CH4[-1],CH4[-1],len(CH4))
        DME_bkg = np.linspace(DME[-1],DME[-1],len(DME))
        MeOH_bkg = np.linspace(MeOH[-1],MeOH[-1],len(MeOH))

        area_CH4 = np.trapz(CH4-CH4_bkg, t, 0.00001)
        area_DME = np.trapz(DME-DME_bkg, t, 0.00001)
        area_MeOH = np.trapz(MeOH-MeOH_bkg, t, 0.00001)
           
        

        fig, (ax1,ax2,ax3) = plt.subplots(1,3,figsize=(14,6))

        ax1.plot(t,CH4,marker='o',label='CH$_{4}$',color= 'tab:blue')
        ax1.plot(t,DME_raw,marker='o',label='DME',color= 'tab:red')
        ax1.plot(t,MeOH_raw,marker='o',label='CH$_{3}$OH', color= 'tab:orange')
        ax1.set_title('GC Signals',fontsize=20)
        ax1.grid(True)
        ax1.set_ylabel('GC counts (a.u.)')
        ax1.set_xlabel('Time (min)')
        ax1.legend()

        ax2.plot(t,DME,marker='o',label='GC data',color= 'tab:red')
        ax2.set_title('DME',fontsize=20)
        ax2.plot(t,DME_bkg, label='Background',color= 'gray')
        ax2.fill_between(t,DME,DME_bkg,color='beige',label='Area= {:.3E}'.format(area_DME)) 
        ax2.grid(True)
        ax2.set_ylabel('ppm')
        ax2.set_xlabel('Time (min)')
        ax2.legend()

        ax3.plot(t,MeOH,marker='o',label='GC data', color= 'tab:orange')
        ax3.set_title('CH$_{3}$OH',fontsize=20)
        ax3.plot(t,MeOH_bkg, label='Background',color= 'gray')
        ax3.fill_between(t,MeOH,MeOH_bkg,color='beige',label='Area= {:.3E}'.format(area_MeOH,))
        ax3.grid(True)
        ax3.set_ylabel('ppm')
        ax3.set_xlabel('Time (min)')
        ax3.legend()
        fig.show()
        dry_weight = 0.086

        #DME
        mol_percent_DME = area_DME*10**(-6)*100
        mL_DME = mol_percent_DME*16.5/100
        mol_DME = (1*(mL_DME*10**(-3)))/(298.15*0.082057)
        Yiled_DME = mol_DME*(10**6)/dry_weight   #(micromol/gram)

        #MEOH
        mol_percent_MEOH = area_MeOH*10**(-6)*100
        mL_MeOH = mol_percent_MEOH*16.5/100
        mol_MeOH = (1*(mL_MeOH*10**(-3)))/(298.15*0.082057)
        Yiled_MeoH = mol_MeOH*(10**6)/dry_weight    #(micromol/gram)

        #TOTAL
        Yield_total = Yiled_MeoH+(2*Yiled_DME)

        if self.Cu_content == 0:
            print('productivity will not be calculated')
            prod = 'N/A'
        else:
            prod = Yield_total/self.Cu_content
            pass
        
        print("""                                                                   
                                                                            __________________________ RESULTS __________________________
                                                                                        ...\{}
                    
                    
                                                                                                    value         unit
                        
                                                                                    DME Yield        {:.4}          micro mol/gram
                                                                                    MeOH Yield       {:.4}          micro mol/gram
        
                                                                                    Total Yield      {:.4}          micro mol/gram
                                                                                    Productivity     {:.6}        mol/mol
        
                                                                            _____________________________________________________________
        """.format(self.Filename_GC[76:],Yiled_DME,Yiled_MeoH,Yield_total,prod))

        pass
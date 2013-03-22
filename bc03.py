# -*- coding: utf-8 *-*
import numpy as np

class Ised:
    '''class Ised construct the mapping between *.ised libaray and
        parameterspace'''
    pars_layouts = ['Tracks', 'SFH&Dust', 'Age&Met']
    pars_ax_dem = {'Tracks': [2, 2], 'SFH&Dust': [2, 6], 'Age&Met': [6, 21]}
    pars_ax_txt = {'Tracks': [['low-res', 'high-res'],
                              ['Padova_1994_chabrier', 'Padova_1994_salpeter']],
        'SFH&Dust': [['Dust_free', 'with_Dust'],
                     ['Instant Burst(SSP)', 'Exp_Tau', 'Single Burst',
                      'Constant', 'Delayed', 'Linear']],
        'Age&Met': [['0.0001', '0.0004', '0.004', '0.008',
                     '0.02', '0.05'],
                    ['H-R', ]]
        }
    pars_bx_dem = {'credit': [2, 4], 'dust&par': [9, 0, 20, 20, 0, 20, 20]}
    pars_bx_txt = {'dust': []}
    
    def __init__(self, par=None):
        self.pars_ax_txt['Age&Met'][1].append(str(range(1, 21)) + '.0')
        for i in ['0.5', '1.0', '1.5']:
            for j in ['0.2', '0.3', '0.4']:
                self.pars_bx_txt['dust'].append('Tau' + i + '_mu' + j)
        for i in ['Exp_Tau', 'Single Burst', 'Delayed', 'Linear']:
            self.pars_bx_txt[i] = ['0.5', '1.0', '1.5', '2.0', '2.5', '3.0',
                                   '3.5', '4.0', '4.5', '5.0', '5.5', '6.0',
                                   '6.5', '7.0', '7.5', '8.0', '8.5', '9.0',
                                   '9.5', '10.0']
        # setup libs
        path = par.bc03_pth
        # get list of library
        self.libs = []
        self.clib = []
    
    def gen_pars(self, ss, key):
        try:
            self.xlim = self.pars_ax_dem[key][1]
            self.ylim = self.pars_ax_dem[key][0]
            self.x_txt = self.pars_ax_txt[key][1]
            self.y_txt = self.pars_ax_txt[key][0]
            self.parspace = 0.5 * np.ones(self.pars_ax_dem[key])
            self.triggers = np.zeros(self.pars_ax_dem[key])
            for i in range(self.pars_ax_dem[key][0]):
                for j in range(self.pars_ax_dem[key][1]):
                    search_str = self.pars_ax_txt[key][1][j] + '_' +\
                        self.pars_ax_txt[key][0][i]
                    self.parspace[i, j] = 0
        
        except KeyError:
            pass
    
    def gen_next(self, par, mx, my, ma):
        pass


class Cfg:
    '''class Cfg stores all config strs and vars'''
    
    # branch controls
    no_compute = True
    no_plot = True
    
    # UI relative
    no_gui = True
    
    # bc03 envs & paths
    bc03_pth = None
    bc03_flt = None
    otpt_pth = None
    lib_spec = None
    lib_ised = None
    lib_mgnt
    
    def __init__(self):
        self.ised = Ised(par=self)

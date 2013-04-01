# -*- coding: utf-8 *-*
import numpy as np
import os
import subprocess


class Ised:
    '''class Ised defines bc03 related variables.'''

    no_compute = True
    # bc03 root paths
    bc03_root = None

    # filters
    flts = ['U', 'B', 'V', 'I', 'R']

    # dict for keyword mapping
    # tracks
    track = {'Padova_1994_chabrier': 0, 'Padova_1994_salpeter': 1}
    track_i = ['Padova_1994_chabrier', 'Padova_1994_salpeter']
    res = {'h': 0, 'l': 1}
    res_i = ['h', 'l']
    # star formation history
    sfh = {'Instant_Burst': 0, 'Exp_Tau': 1, 'Single_Burst': 2,
                      'Constant': 3, 'Delayed': 4, 'Linear': 5}
    sfh_i = ['Instant_Burst', 'Exp_Tau', 'Single_Burst',
                      'Constant', 'Delayed', 'Linear']
    s_tau = [0, ]  # list contain s_tau
    # deal with dust
    d_tau = [0, ]
    d_mu = [0, ]
    # deal with redshift
    red = []
    h0 = 0.7
    o_lambda = 0.3
    # metalicity
    metalicity = {'0.0001': 0, '0.0004': 1, '0.004': 2, '0.008': 3,
                     '0.02': 4, '0.05': 5}
    met = [0, ]
    # age
    age = [0, ]
    # spectra related
    spec = {}

    def __init__(self, par=None):
        '''all stuff related to galaxev'''
        ##  par has a, b, c as string, d as list
        a = 'Padova_1994_chabrier'
        b = 'h'
        c = 'Instant_Burst'
        self.code_txt = a + '__' + b + '__' + c
        self.s_tau = np.arange(0.1, 0.9, 0.2)  # sfh_tau
        self.d_tau = np.arange(0.1, 0.9, 0.4)
        self.d_mu = np.arange(0.1, 0.9, 0.1)
        self.met = [0.0001, 0.0004, 0.004, 0.008,
                     0.02, 0.05]
        self.age = np.arange(1.0, 20.0, 1.0)
        self.spec = {'f_type': 'f_lambda',
            'wl_range': 'yes',
            }
        # set up envs
        self.bc03_root = '/home/ma/Codes/virtualenv_1/galaxev-dev/galaxev/'
        self._set_env()
        # init points in parameter space from epar of pyraf
        # code is those single inputs
        code = [self.track[a], self.res[b], self.sfh[c]]
        # lst is those multi inputs, iterate to expand
        temp = []  # init container
        # last element in temp: 0 - not calculated
        #                       1 - calculated
        for i in self.s_tau:
            for j in self.d_tau:
                for k in self.d_mu:
                    for l in self.met:
                        for m in self.age:
                            temp.append((code[0], code[1], code[2],
                                i, j, k, l, m, 0))
        # generate rec array for accessibility
        self.parspace = np.array(temp,
            dtype=[('track', 'i'), ('res', 'i'), ('sfh', 'i'),
                ('s_tau', 'f'), ('d_tau', 'f'), ('d_mu', 'f'),
                ('met', 'f'), ('age', 'f'), ('exist', 'i')])
        # mark down the existence of lib
        # lib_file is ised/*.ised
        # for age=0, get lib_color/*.1color,
        # for age!=0, get lib_spec/*.spec
        for e in self.parspace:
            # get search string
            filename, exist = self.gen_name(e)  # it is lib_file name
            e[-1] = exist

    def _set_env(self):
        '''setup env and path for bc03 run'''
        r = self.bc03_root
        # paths
        self.bc03_outputs = r + 'outputs/'
        self.bc03_filters = r + 'filters/'
        self.bc03_spectra = r + 'spectra/'
        self.bc03_iseds = r + 'iseds/'
        self.bc03_colors = r + 'colors/'
        # envs
        src = r + 'src/'
        self.bc03_src = src
        self.env = os.environ.copy()
        self.env['bc03'] = src
        self.env['FILTERS'] = src + 'FILTERBIN.RES'
        self.env['A0VSED'] = src + 'A0V_KURUCZ_92.SED'
        self.env['RF_COLORS_ARRAYS'] = src + 'RF_COLORS.filters'

    def gen_name(self, e):
        '''function generates the file_name from an parspace entry'''
        filename = str(e[0]) + '_' +\
            str(e[1]) + '_' +\
            str(e[2]) + '_' +\
            str(e[3]) + '_' + str(e[4]) + '_' + str(e[5]) + '_' +\
            str(e[6]) + '_.ised'
        try:
            with open(self.bc03_iseds + filename):
                exist = 1
        except IOError:
            exist = 0
        return filename, exist

    def gen_csp(self, ind):
        '''generate none-exist ised file'''
        # get up env
        env = self.env

        def gen_libname(e):
            '''from e in parspace generate standard bc03 library name'''
            if e[0] == 0:
                pre = "models/Padova1994/chabrier/bc2003_"
                sur = "_chab_ssp.ised_ASCII.gz"
            elif e[0] == 1:
                pre = "models/Padova1994/salpeter/bc2003_"
                sur = "_salp_ssp.ised_ASCII.gz"
            if e[1] == 0:
                res = "hr_"
            elif e[1] == 1:
                res = "lr_"
            metcode = str(e[-3])
            metdict = {'0.0001': 'm22',
                '0.0004': 'm32',
                '0.004': 'm42',
                '0.008': 'm52',
                '0.02': 'm62',
                '0.05': 'm72'
                }
            met = metdict[metcode]
            libnm = pre + res + met + sur
            return libnm

        # unique-ise the file name
        nm = [''] * len(self.parspace)
        for i in ind:
            nm[i] = 'iseds/' + self.gen_name(self.parspace[i])[0]
        _, uid = np.unique(nm, return_index=True)
        tmp = open(self.bc03_root + "tmp.cspgal", "w")
        for u in uid:
            if (nm[u] != '') & (self.parspace[u][-1] == 0):
                # get out_name
                outname = nm[u]
                print outname
                # get lib_name
                libname_gz = gen_libname(self.parspace[u])
                libname_asc = libname_gz[:-3]
                libname_bin = libname_gz[:-9]
                # check if bc03 library uncompressed and binarized
                p = 0
                try:
                    with open(self.bc03_root + libname_bin):
                        p = 1
                except IOError:
                    print libname_gz
                    try:
                        p = subprocess.call(["gunzip ",
                            self.bc03_root + libname_gz],
                            shell=False)
                    except:
                        pass
                    p = subprocess.call([self.bc03_src + "bin_ised",
                        self.bc03_root + libname_asc],
                        shell=False)
                # write tmp file
                if p == 0:
                    print "error when uncompress and binary-ise the libfile"
                else:
                    # line_1 is lib file name
                    line_1 = libname_bin + '\n'
                    print line_1
                if self.parspace[u][4] > 0:
                    # line_2 is the dust
                    line_2 = 'Y\n' + str(self.parspace[u][4]) + '\n' +\
                        str(self.parspace[u][5]) + '\n'
                else:
                    line_2 = 'N\n'
                # line_3 is sfh
                sfhcode = str(self.parspace[u][2])
                sfhtau = str(self.parspace[u][3])
                if sfhcode == '0':
                    line_3 = sfhcode + '\n'
                elif sfhcode == '1':
                    line_3 = sfhcode + '\n' + sfhtau + '\n' +\
                        'N\n' + '20\n'
                elif sfhcode == '2':
                    line_3 = sfhcode + '\n' + sfhtau + '\n'
                else:
                    line_3 = sfhcode + '\n' + sfhtau + '\n' +\
                        '20\n'  # further develop
                # line_4 is output file name
                line_4 = outname + '\n'
                tmp.write(line_1 + line_2 + line_3 + line_4)
        tmp.close()
        tmp = open(self.bc03_root + "tmp.cspgal", "r")
        sout = subprocess.check_output(self.bc03_src + "csp_galaxev", stdin=tmp,
            env=env, shell=False)
        tmp.close()
        print sout
        self.out_msg = sout

    def get_hrd(self, ind):
        '''get a subset of HR diagram. ind is index in parspace'''
        pass

    def get_spe(self, ind):
        '''get a subset of spectra. ind is index in parspace'''
        # set up env
        env = self.env
        # get input for wave length range
        if self.spec['f_type'] == "f_lambda":
            pre = "-"
        else:
            pre = ""
        if self.spec['wl_range'] == "yes":
            mid = self.spec['w1'] + "," + self.spec['w2']
        else:
            mid = ""
        if self.spec['use_norm'] == "yes":
            sur = "," + self.spec['w0'] + "," + self.spec['f0']
        else:
            sur = ""
        inwr = pre + mid + sur
        #resolve input ised files
        fn = [''] * len(ind)
        age_file = [''] * len(ind)
        data = [0] * len(ind)  # mark 0 for no ised, 1 for no spec
        need_compute = False
        need_extract = False
        #generate param file
        tmp = open(self.bc03_root + "tmp.gpl", "w")
        for i in ind:
            if self.parspace[i][-1] > 0:
                fn[i] = self.bc03_iseds + self.gen_name(self.parspace[i])
                # check if age file exsist
                age_file[i] = self.bc03_spectra + fn[i][:-5] + '_' +\
                     self.parspace[i][-2] +\
                     '_' + self.spec['f_type'] + '.spec'
                try:
                    data[i] = np.loadtxt(age_file[i])
                except IOError:
                    need_extract = True
                    tmp.write(fn[i] + "\n"
                    + inwr + "\n"
                    + self.parspace[i][-2] + "\n"
                    + age_file + "\n")
                    data[i] = 1
            else:
                need_compute = True
                fn[i] = 'n/a'
                data[i] = 0
        tmp.close()
        if need_extract:
            #change working directory to /spectra to achive spectra
            #cwd = os.getcwd()
            #os.chdir(self.bc03_spectra)
            #call spectra extraction: galaxevpl
            tmp = open(self.bc03_root + "tmp.gpl", "r")
            sout = subprocess.check_output(self.bc03_src + "galaxevpl",
                stdin=tmp, env=env, shell=False)
            self.out_msg = sout
            tmp.close()
            #change back
            #os.chdir(cwd)
        # now read the spectra
        for i in range(0, len(data)):
            if data[i] == 1:
                data[i] = np.loadtxt(age_file[i])
        # deal with need compute
        if need_compute:
            if self.no_compute:
                print 'some points are missing, which are not going\
to display unless no_compute is set to False'
            else:
                print 'missing .ised files have been generated,\
recheck the checker to continue...'
                # call gen_csp to generate the ised
                ind_to_gen = []
                for i in range(0, len(data)):
                    if data[i] == 0:
                        ind_to_gen.append(i)
                self.gen_csp(ind_to_gen)


class Cfg:
    '''class Cfg stores all config strs and vars'''

    # UI controls
    no_plot = True
    no_gui = True

    def __init__(self, par=None):
        '''instantialize a Ised calss'''
        self.ised = Ised(par)
# -*- coding: utf-8 *-*


class Cfg:
    '''class Cfg stores all config strs and vars, serves as global var'''

    # branch controls
    gui_view = None
    wl_range = None
    fl_dnsty = None
    fl_scale = None

    # UI relative
    menu_lst = None
    echo_str = None
    pars_axs = None
    # bc03 envs & paths
    bc03_pth = None
    bc03_flt = None
    rslt_pth = None
    lib_spec = None
    lib_ised = None

    def __init__(self):
        pass

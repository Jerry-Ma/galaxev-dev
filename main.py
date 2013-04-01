# -*- coding: utf-8 *-*
import draw
import bc03


def csp(par):
    '''call hr diagram draw'''
    ui = draw.UI(par=par)  # instantize a main window
    ui.master.title("Composation of Stellar Populations")
    ui.pack()
    ui.mainloop()


def gpl(par):
    '''call spec diagram draw'''
    ui = draw.UI(par=par)
    ui.master.title("View of Spectrum")
    ui.pack()
    ui.mainloop()


def flt(par):
    '''show the filters'''
    pass


def nogui_test(par):
    '''for test'''
    ind = range(1, 40)
    par.ised.gen_csp(ind)

cfg = bc03.Cfg()    # cfg.* - basic cfg
                    # cfg.ised.* - bc03 cfg
#import cProfile
#cProfile.run("csp(cfg)")
csp(cfg)
#nogui_test(cfg)

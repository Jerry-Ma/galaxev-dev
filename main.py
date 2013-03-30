# -*- coding: utf-8 *-*
import draw
import bc03


def csp(par):
    ui = draw.UI(par=par)  # instantize a main window
    ui.master.title("Composation of Stellar Populations")
    ui.pack()
    ui.mainloop()


def gpl(par):
    ui = draw.UI(par=par)
    ui.master.title("View of Spectrum")
    ui.pack()
    ui.mainloop()


def flt(par):
    pass


cfg = bc03.Cfg()    # cfg.* - basic cfg
                    # cfg.ised.* - bc03 cfg
print cfg.ised.parspace
#import cProfile
#cProfile.run("csp(cfg)")
csp(cfg)

# -*- coding: utf-8 *-*
import draw
import cfg


def lib_view(par):
    ui = draw.UI(par=par)  # instantize a main window
    ui.master.title("Lib_View")
    ui.pack()
    ui.mainloop()

def pars_view(par):
    ui = draw.UI(par=par)
    ui.master.title("Parspace View")
    ui.pack()
    ui.mainloop()

par = cfg.Cfg()
par.lib_view = False
if par.lib_view == True:
    lib_view(par)
else:
    pars_view(par)

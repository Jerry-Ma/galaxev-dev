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


par = bc03.Cfg()
csp(par)

# -*- coding: utf-8 *-*
import draw
import bc03


def csp(par):
    ui = draw.UI(par=par)  # instantize a main window
    ui.master.title("Lib_View")
    ui.pack()
    ui.mainloop()

def gpl(par):
    ui = draw.UI(par=par)
    ui.master.title("Parspace View")
    ui.pack()
    ui.mainloop()

def flt(par)

par = bc03.Cfg()
csp(par)

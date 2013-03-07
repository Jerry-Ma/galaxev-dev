# -*- coding: utf-8 *-*
import Tkinter
import ttk
from matplotlib.backends.backend_tkagg\
    import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib
#from matplotlib.widgets import RectangleSelector
#import numpy as np


class UI(ttk.Frame):
    '''Drawing the main window'''
    def __init__(self, master=None, par=None):
        ttk.Frame.__init__(self, master)
        mn = DMenu(master=master, par=par)  # Dynamic Menu Bar
        mn.pack()
        cv = DCanvas(master=master, par=par)  # Dynamic Canvas
        cv.pack()
        # Layers here are no more than a matplotlib figure object!
        self.add_layer(mn, cv, par, 'root')

        buttona = ttk.Button(self, command=
            lambda: self.add_layer(mn, cv, par, 'sub1'))
        buttonb = ttk.Button(self, command=
            lambda: self.add_layer(mn, cv, par, 'sub2'))
        buttona.pack()
        buttonb.pack()

    def add_layer(self, menu=None, canvas=None, par=None, s=None):
        # Root Button on Menu Bar, pars
        par.menu_lst.append(s)
        bt = ttk.Button(menu, text=s, command=lambda:
            self.del_layer(menu, par, par.menu_lst.index(bt['text'])))
        menu.ttl.append(bt)
        menu.ttl[-1].pack(side='left')
        # Root Layers on Canvas
        canvas.draw_parspace(par, s)

    def del_layer(self, master=None, par=None, i=None):
        while i < len(par.menu_lst) - 1:
            print par.menu_lst
            del par.menu_lst[-1]
            master.ttl[-1].destroy()
            del master.ttl[-1]


class DMenu(ttk.Frame):
    '''Drawing the dynamic menubar, as well as filter chooser'''

    def __init__(self, master=None, par=None):
        ttk.Frame.__init__(self, master)
        self.ttl = []
        flt = ttk.Menubutton(self, text='Click to choose filter(s)')
        flt.pack(side='right')
        flt.menu = Tkinter.Menu(flt)
        for i in ['U', 'B', 'V', 'I', 'R']:
            flt.menu.add_command(label=i, underline=0, command=None)
            flt.menu.add_separator()
        flt['menu'] = flt.menu


class DCanvas(ttk.Frame):
    '''Drawing the dynamic canvas, as weel as the parspace generator'''
    fig = matplotlib.figure.Figure()
    fig_ld = {}

    def __init__(self, master=None, par=None):
        ttk.Frame.__init__(self, master)
        self.pack()
     #   fig.add_subplot(212)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.master)
        self.toolbar.update()

    def draw_parspace(self, par=None, s=None):
        x = par.pars_axs[s][0]
        y = par.pars_axs[s][1]
        print x, y
        #try:
            #self.fig = self.fig_ld[s].frozen()
            #print s
        #except KeyError:
            #self.fig_ld[s] = matplotlib.figure.Figure()
        for i in range(0, x * y):
          #  self.fig_ld[s].add_subplot(x, y, i + 1)
            self.fig.add_subplot(x, y, i + 1)
            print i
        #self.fig = self.fig_ld[s].frozen()
        self.canvas.draw()



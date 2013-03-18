# -*- coding: utf-8 *-*
import Tkinter
import ttk
from matplotlib.backends.backend_tkagg\
    import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib
#from matplotlib.widgets import RectangleSelector
import numpy as np
import functools


class UI(ttk.Frame):
    '''Drawing the main window'''
    def __init__(self, master=None, par=None):
        ttk.Frame.__init__(self, master)
        mn = DMenu(master=master, par=par)  # Dynamic Menu Bar
        mn.pack()
        cv = DCanvas(master=master, par=par)  # Dynamic Canvas
        cv.pack()
        # Layers here are no more than a matplotlib figure object!
        self.add_layer(None, mn, cv, par)
        cv.canvas.mpl_connect('button_release_event', functools.partial
            (self.add_layer, menu=mn, canvas=cv, par=par))

        #buttona = ttk.Button(self, command=
            #lambda: self.add_layer(mn, cv, par, 'SFH&Dust'))
        #buttonb = ttk.Button(self, command=
            #lambda: self.add_layer(mn, cv, par, 'Met&Age'))
        #buttona.pack()
        #buttonb.pack()

    def add_layer(self, event=None, menu=None, canvas=None, par=None):
        # Root Button on Menu Bar, pars
        if event is None:
            s = 'Tracks'
            ss = ''
            a = None
        else:
            if event.inaxes != canvas.ax & event.inaxes != canvas.bx:
                return
            mx, my = [int(a) for a in np.rint([event.xdata, event.ydata])]
            if event.inaxes == canvas.ax:
                ma = canvas.ax
            s, ss, a = par.ised.gen_next(par, mx, my, ma)
        par.menu_lst.append(s)
        par.sstr_lst.append(ss)
        bt = ttk.Button(menu, text=s, command=lambda:
            self.del_layer(menu, canvas, par, par.menu_lst.index(bt['text'])))
        menu.ttl.append(bt)
        menu.ttl[-1].pack(side='left')
        canvas.draw_parspace(par=par, a=a)

    def del_layer(self, master=None, canvas=None, par=None, i=None):
        while i < len(par.menu_lst) - 1:
            print par.menu_lst
            del par.menu_lst[-1]
            del par.sstr_lst[-1]
            master.ttl[-1].destroy()
            del master.ttl[-1]
        canvas.draw_parspace(par=par, a=canvas.ax)


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
    '''Drawing the dynamic canvas, as well as the parspace generator'''
    fig = matplotlib.figure.Figure()
    ax = fig.add_subplot(211)
    bx = fig.add_subplot(212)
    pars = {}
    oxy = None

    def __init__(self, master=None, par=None):
        ttk.Frame.__init__(self, master)
        self.pack()
        # init a im object
        parspace = np.array([[0, 1], [1, 0]])
        self.im = self.ax.imshow(parspace, interpolation='nearest',
            aspect='auto')
        self.ax.grid(True)
        # set up canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.master)
        self.toolbar.update()
        self.canvas.mpl_connect('motion_notify_event', self.onhover)

    def draw_parspace(self, par=None, a=None):
        self.oxy = None
        s = par.menu_lst[-1]
        ss = par.sstr_lst[-1]
        par.ised.gen_pars(ss, s)
        self.parspace = par.ised.parspace
        xlim = par.ised.xlim
        ylim = par.ised.ylim
        x_txt = par.ised.x_txt
        y_txt = par.ised.y_txt
        self.im.set_data(self.parspace)
        self.im.set_extent([-0.499, xlim - 0.5, ylim - 0.5, -0.499])
        # set axis label and tick
        xlb = [e.get_text() for e in self.ax.get_xticklabels()]
        ylb = [e.get_text() for e in self.ax.get_yticklabels()]
        xlb = [''] * len(xlb)
        ylb = [''] * len(ylb)
        for k in range(1, len(xlb), 2):
            xlb[k] = x_txt[(k - 1) / 2]
        for k in range(1, len(ylb), 2):
            ylb[k] = y_txt[(k - 1) / 2]
        self.ax.set_xticklabels(xlb)
        self.ax.set_yticklabels(ylb)
        self.canvas.draw()

    def onhover(self, event):
        '''reverse color on mouse hover'''
        if event.inaxes != self.ax:
            return
        x, y = [int(a) for a in np.rint([event.xdata, event.ydata])]
        if x == len(self.parspace[0, :]):
            x = x - 1
        if y == len(self.parspace[:, 0]):
            y = y - 1
        if self.oxy is not None:
            ox, oy = self.oxy
            if ox == x & oy == y:
                pass
            else:
                self.parspace[oy, ox] = 1 - self.parspace[oy, ox]
                self.parspace[y, x] = 1 - self.parspace[y, x]
                self.oxy = [x, y]
        else:
            self.oxy = [x, y]
            self.parspace[y, x] = 1 - self.parspace[y, x]
        self.im.set_data(self.parspace)
        self.canvas.draw()

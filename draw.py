# -*- coding: utf-8 *-*
import Tkinter
import ttk
from matplotlib.backends.backend_tkagg\
    import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib
from matplotlib.widgets import RectangleSelector
import numpy as np


class UI(ttk.Frame):
    '''Drawing the main window'''
    def __init__(self, master=None, par=None):
        ttk.Frame.__init__(self, master)
        mn = DMenu(master=master, par=par)  # Dynamic Menu Bar
        mn.pack()
        cv = DCanvas(master=master, par=par)  # Dynamic Canvas
        cv.pack()
        # Layers here are no more than a matplotlib figure object!
        self.add_layer(mn, cv, par, 'Tracks')

        buttona = ttk.Button(self, command=
            lambda: self.add_layer(mn, cv, par, 'SFH&Dust'))
        buttonb = ttk.Button(self, command=
            lambda: self.add_layer(mn, cv, par, 'Met&Age'))
        buttona.pack()
        buttonb.pack()

    def add_layer(self, menu=None, canvas=None, par=None, s=None):
        # Root Button on Menu Bar, pars
        par.menu_lst.append(s)
        bt = ttk.Button(menu, text=s, command=lambda:
            self.del_layer(menu, canvas, par, par.menu_lst.index(bt['text'])))
        menu.ttl.append(bt)
        menu.ttl[-1].pack(side='left')
        canvas.draw_parspace(par, s)

    def del_layer(self, master=None, canvas=None, par=None, i=None):
        while i < len(par.menu_lst) - 1:
            print par.menu_lst
            del par.menu_lst[-1]
            master.ttl[-1].destroy()
            del master.ttl[-1]
        canvas.draw_parspace(par, par.menu_lst[i])


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

    def __init__(self, master=None, par=None):
        ttk.Frame.__init__(self, master)
        self.pack()
        # init a im object
        parspace = np.array([[0, 1], [1, 0]])
        self.im = self.ax.imshow(parspace, interpolation='nearest',
            aspect='auto')
        # set up canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.master)
        self.toolbar.update()
        self.RS = RectangleSelector(self.ax,
            self.onselect, drawtype='box')
        self.canvas.mpl_connect('motion_notify_event', self.onhover)

    def draw_parspace(self, par=None, s=None):
        x = par.pars_axs[s][0]
        y = par.pars_axs[s][1]
        print x, y
        try:
            parspace = self.pars[s]
        except KeyError:
            parspace = np.random.random((x, y))
            self.pars[s] = parspace

        self.im.set_data(parspace)
        self.canvas.draw()


    def onselect(self, eclick, erelease):
        '''eclick and erelease are matplotlib events @ press and release'''
        vet = np.array([[eclick.xdata, eclick.ydata],
            [erelease.xdata, erelease.ydata]])
        print vet

    def onhover(self, event):
        if event.inaxes!=self.ax: return
        print 'hover: %s, %s' % (event.xdata, event.ydata)


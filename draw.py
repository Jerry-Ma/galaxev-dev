# -*- coding: utf-8 *-*
import Tkinter
import ttk
from matplotlib.backends.backend_tkagg\
    import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib
import numpy as np
import functools
from matplotlib.widgets import RectangleSelector, LassoSelector
from matplotlib.path import Path
import string
from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms
from matplotlib.ticker import Formatter, FixedLocator


class UI(ttk.Frame):
    '''Drawing the main window'''
    def __init__(self, master=None, par=None):
        ttk.Frame.__init__(self, master)
        mn = DMenu(master=master, par=par)  # Dynamic Menu Bar
        mn.pack()
        cv = DCanvas(master=master)  # Dynamic Canvas
        cv.pack()
        # add checkbuton to the menu
        # container for checkbutton status
        self.cbvar = {}
        self.checked = 0
        # checkbutton: sfh_tau, dust_tau, dust_mu, met, age
        cb_txt = ['s_tau', 'd_tau', 'd_mu', 'met', 'age']
        for txt in cb_txt:
            self.cbvar[txt] = Tkinter.IntVar()
            cb = ttk.Checkbutton(mn, text=txt, variable=self.cbvar[txt],
                command=functools.partial(self.set_layer,
                    mn, cv, txt, par))
            mn.ttl.append(cb)
            mn.ttl[-1].pack(side='left')

        # set_layer generate the plot for parspace according to self.cbvar{}
        self.set_layer(mn, cv, None, par)

    def set_layer(self, mn, cv, i, par):
        # for init state
        if i is None:
            return
        # allow maximum of two checked
        if self.cbvar[i].get() == 1:
            if self.checked == 2:
                for e in self.cbvar.values():
                    e.set(0)
                self.checked = 0
            else:
                self.checked = self.checked + 1
        else:
            self.checked = self.checked - 1
        # get the axises
        ax_txt = []
        for k, v in self.cbvar.items():
            if v.get() == 1:
                ax_txt.append(k)
        ax_num = len(ax_txt)
        # draw parspace
        if ax_num == 2:
            print "2D"
        elif ax_num == 1:
            print "1D"
        else:
            print "0D"
        cv.draw_parspace(par=par, a=ax_txt)


class DMenu(ttk.Frame):
    '''Drawing the dynamic menubar, as well as filter chooser'''
    ttl = []

    def __init__(self, master=None, par=None):
        ttk.Frame.__init__(self, master)
        # add menu button for filters
        ttk.Separator(self, orient='vertical').pack(
            side='right', fill='both', padx=(1, 0))
        flt = ttk.Menubutton(self, text='Click to choose filter(s)')
        flt.pack(side='right')
        ttk.Separator(self, orient='vertical').pack(
            side='right', fill='both', padx=(9, 1))
        # add filters menu
        flt.menu = Tkinter.Menu(flt)
        flts = par.ised.flts
        # menu_buttons
        for i in flts:
            flt.menu.add_command(label=i, underline=0, command=None)
            flt.menu.add_separator()
        flt['menu'] = flt.menu
        # add menu for default values of parameters
        # d_code: track, res, sfh
        d_code = par.ised.code_txt
        ttk.Separator(self, orient='v').pack(side='left',
            fill='both', padx=(0, 1))
        dft = ttk.Menubutton(self, text=d_code)
        dft.pack(side='left')
        ttk.Separator(self, orient='v').pack(side='left',
            fill='both', padx=(1, 9))
        # add defaults
        dft.menu = Tkinter.Menu(dft,
            title='Set Default Values', font=('TkFixedFont'))
        dfts = ['s_tau', 'd_tau', 'd_mu', 'met', 'age']
        # v is the radiobutton state, submenu stores the submenus
        v = {}
        submenu = {}

        def popup(event=None, mn=None):
            '''get a torn-off menu instead of a regular one'''
            h = self.winfo_height()
            mn.post(event.x_root, event.y_root + h)
            mn.invoke(0)
            mn.unpost()

        def title(event):
            '''set menu entry label according to the RadioButton'''
            for i in range(0, len(dfts)):
                dft.menu.entryconfig(i + 1,
                    label=string.rjust(dfts[i], 6) + ' : ' + v[dfts[i]].get())

        # associate submenu to dft.menu
        for i in dfts:
            submenu[i] = Tkinter.Menu(title=i, font=('TkFixedFont'), tearoff=0)
            submenu[i].bind('<Configure>', title)
            v[i] = Tkinter.StringVar()
            pars = getattr(par.ised, i)
            for j in pars:
                submenu[i].add_radiobutton(
                    label=str(j),
                    variable=v[i], value=str(j))
            v[i].set(str(pars[len(pars) / 2 - 1]))
            dft.menu.add_cascade(
                label=string.rjust(i, 5) + ' : ' + v[i].get(),
                menu=submenu[i])
        dft.bind('<Button-1>', functools.partial(popup, mn=dft.menu))


class DCanvas(ttk.Frame):
    '''Drawing the dynamic canvas, as well as the parspace generator'''
    fig = matplotlib.figure.Figure()
    ax = fig.add_subplot(211, aspect='auto')
    bx = fig.add_subplot(212, aspect='auto')

    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.pack()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.master)
        self.toolbar.update()

    def draw_parspace(self, par=None, a=None):
        if len(a) == 0:
            print "null"
            return
        elif len(a) == 1:
            a.append('N/A')
            isnull = True
        else:
            isnull = False
        # sfh_tau, dust_tau, dust_mu, met, age
        # generate the list of ticks
        pars = {}
        for e in a:
            try:
                pars[e] = getattr(par.ised, e)
            except AttributeError:
                pars[e] = [0, ]
        # set x and y
        if len(pars[a[0]]) >= len(pars[a[1]]):
            x = a[0]
            y = a[1]
        else:
            x = a[1]
            y = a[0]

        # parspace stores the points
        self.parspace = par.ised.parspace
        # stack and unique-ise to eliminate overlapped point
        try:
            xy = np.unique(self.parspace[[x, y]])
            print xy
            xx = xy[x]
            yy = xy[y]
        except ValueError:
            print "keyerror"
            xx = np.unique(self.parspace[x])
            yy = np.zeros(len(xx))
        # clean previous dots
        self.ax.cla()

        # a_out is the alpha of dots outside the select region
        a_out = 0.2
        # plot the whole scatter
        self.sc = self.ax.scatter(xx,
            yy, s=200, c=(0, .2, 1, a_out), linewidths=0, marker='p')
        # deal with metalicity, the discrete value
        if x == 'met':
            mscale.register_scale(sMetalicity)
            print "x_met"
            self.ax.set_xscale('metalicity')
            self.ax.set_xlim(-0.1, 0.1)
        if y == 'met':
            mscale.register_scale(sMetalicity)
            self.ax.set_yscale('metalicity')
            self.ax.set_ylim(-0.1, 0.1)
        # deal with null, only keep the 0 tick
        if isnull:
            self.ax.yaxis.set_major_locator(FixedLocator([0, ]))
        # add figure elements: label, title, legend
        self.ax.grid()
        self.ax.set_xlabel(x)
        self.ax.set_ylabel(y)

        # sc is collection, enable selector for that
        self.selc = Selector(self.canvas, self.ax, self.sc, a_out)

        self.canvas.draw_idle()


class Selector(object):
    '''Select indices from a matplotlib collection'''

    def __init__(self, cv, ax, sc, a_out=0.2):
        self.cv = ax.figure.canvas
        self.ax = ax
        self.sc = sc
        self.a_out = a_out
        self.xys = sc.get_offsets()
        self.N = len(self.xys)
        # Ensure that we have separate colors for each object
        self.fc = sc.get_facecolors()
        if len(self.fc) == 0:
            raise ValueError('Collection must have a facecolor')
        elif len(self.fc) == 1:
            self.fc = np.tile(self.fc, self.N).reshape(self.N, -1)
        self.lasso = rLassoSelector(ax,
            onselect=self.on_select, button=3, useblit=True)
        self.rselect = RectangleSelector(ax,
            onselect=self.on_select, button=1, useblit=True)
        self.ind = []

    def on_select(self, c, r=None):
        if r is None:
            path = Path(c)
        else:
            vet = [(c.xdata, r.ydata),
                (c.xdata, c.ydata),
                (r.xdata, c.ydata),
                (r.xdata, r.ydata), ]
            codes = [Path.MOVETO,
                 Path.LINETO,
                 Path.LINETO,
                 Path.LINETO, ]
            path = Path(vet, codes, )
        self.ind = np.nonzero([
            path.contains_point(xy) for xy in self.xys])[0]
        self.fc[:, -1] = self.a_out
        self.fc[self.ind, :] = (1, 0, 0, 1)
        self.sc.set_facecolors(self.fc)

        self.cv.draw_idle()


class rLassoSelector(LassoSelector):
    '''override the class to enable mouse button'''

    def __init__(self, ax, onselect=None, useblit=True,
        lineprops=None, button=1):
        super(rLassoSelector, self).__init__(
            ax, onselect, useblit, lineprops)
        self.validButton = button

    def ignore(self, event):
        wrong_button = hasattr(event, 'button') and\
            event.button != self.validButton
        return not self.active or wrong_button

    def onmove(self, event):
        if self.ignore(event) or event.inaxes != self.ax:
            return
        if self.verts is None:
            return
        if event.inaxes != self.ax:
            return
        if event.button != self.validButton:
            return
        self.verts.append((event.xdata, event.ydata))
        self.line.set_data(zip(*self.verts))
        if self.useblit:
            self.canvas.restore_region(self.background)
            self.ax.draw_artist(self.line)
            self.canvas.blit(self.ax.bbox)
        else:
            self.canvas.draw_idle()


class sMetalicity(mscale.ScaleBase):
    """
    make metalicities show evenly.
    """

    name = 'metalicity'

    def __init__(self, axis, **kwargs):
        mscale.ScaleBase.__init__(self)

    def get_transform(self):
        """
        Override this method to return a new instance that does the
        actual transformation of the data.
        """
        return self.MetalicityTransform()

    def set_default_locators_and_formatters(self, axis):
        """
        Override to set up the locators and formatters to use with the
        scale.  This is only required if the scale requires custom
        locators and formatters.
        """
        class DegreeFormatter(Formatter):
            def __call__(self, x, pos=None):
                # \u00b0 : degree symbol
                return '%s' % (x)

        #deg2rad = np.pi / 180.0
        axis.set_major_locator(FixedLocator([0.0001, 0.0004, 0.004, 0.008,
                     0.02, 0.05]))
        axis.set_major_formatter(DegreeFormatter())
        axis.set_minor_formatter(DegreeFormatter())
        pass

    def limit_range_for_scale(self, vmin, vmax, minpos):
        """
        Override to limit the bounds of the axis to the domain of the
        transform.
        """
        return -0.1, 0.1

    class MetalicityTransform(mtransforms.Transform):
        '''actually do the transformation'''

        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self):
            mtransforms.Transform.__init__(self)

        def transform_non_affine(self, a):
            """
            This transform takes an Nx1 ``numpy`` array and returns a
            transformed copy.
            """
            b = [-0.1, 0.0001, 0.0004, 0.004, 0.008,
                0.02, 0.05, 0.1]
            c = [0, 1, 2, 3, 4, 5, 6, 7]
            return np.interp(a, b, c)

        def inverted(self):
            """
            Override this method so matplotlib knows how to get the
            inverse transform for this transform.
            """
            return sMetalicity.InvertedMetalicityTransform()

    class InvertedMetalicityTransform(mtransforms.Transform):
        '''do the inverse transformation'''

        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self):
            mtransforms.Transform.__init__(self)

        def transform_non_affine(self, a):
            print a
            print "invers"
            b = [-0.1, 0.0001, 0.0004, 0.004, 0.008,
                     0.02, 0.05, 0.1]
            c = [0, 1, 2, 3, 4, 5, 6, 7]
            return np.interp(a, c, b)

        def inverted(self):
            return sMetalicity.MetalicityTransform()
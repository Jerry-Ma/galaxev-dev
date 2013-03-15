# -*- coding: utf-8 *-*
import draw
import cfg


def main(par):
    if par.gui_view:
        ui = draw.UI(par=par)  # instantize a main window
        ui.master.title("main")
        ui.pack()
        ui.mainloop()

par = cfg.Cfg()
par.menu_lst = []
par.gui_view = True
par.echo_str = 'test'
par.pars_axs = {'Tracks': [2, 4], 'SFH&Dust': [2, 3], 'Met&Age': [7, 21]}
main(par)

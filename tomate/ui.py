import pygtk
pygtk.require('2.0')
import gtk
import gobject
import logging

from tomate.plan import PlanView
from tomate.activity import ActivityView
from tomate.history import HistoryView

icontheme = gtk.icon_theme_get_default()

MENU_ICON_SIZE = 32

PAGES = [
        ('Activity',    'ActivityView', 'stock_task'),
        ('Plan',        'PlanView',     'tomboy'),
        ('History',     'HistoryView',  'stock_calendar'),
    ]

class MainWindow(gtk.Window):
    """Activity Window Class"""
    def __init__(self):
        super(MainWindow, self).__init__()
        self.notebook = self._create_notebook()
        self.menu_view = self._create_menuview()
        self.menu_model = self.menu_view.get_model()
        self._setup_pages()

        mainpane = gtk.HPaned()
        mainpane.pack1(self.menu_view, shrink=False)
        mainpane.pack2(self.notebook, shrink=False)
        self.add(mainpane)

        self.set_title('Tomate')
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_border_width(10)
        self.set_geometry_hints(self.menu_view, min_width=120, min_height=350)
        self.set_geometry_hints(self.notebook, min_width=500, min_height=350)

        self.connect('destroy', self._on_close)

    def _create_notebook(self):
        notebook = gtk.Notebook()
        notebook.set_show_tabs(False)
        return notebook

    def _create_menuview(self):
        def _icon_render_func(col, renderer, model, iter, user_data=None):
            icon = model.get_value(iter, 0)
            if icon:
                renderer.set_property('pixbuf', icon)
            else:
                renderer.set_property('stock-id', gtk.STOCK_EDIT)
                renderer.set_property('stock-size', MENU_ICON_SIZE)

        menu_model = gtk.ListStore(gtk.gdk.Pixbuf, str, int)
        menu_view = gtk.TreeView()
        menu_view.set_model(menu_model)
        menu_view.set_headers_visible(False)
        icon_renderer = gtk.CellRendererPixbuf()
        icon_col = gtk.TreeViewColumn('Icon', icon_renderer)
        icon_col.set_cell_data_func(icon_renderer, _icon_render_func)
        text_col = gtk.TreeViewColumn('Text', gtk.CellRendererText(), text=1)
        menu_view.append_column(icon_col)
        menu_view.append_column(text_col)
        menu_view.get_selection().set_mode(gtk.SELECTION_SINGLE)
        return menu_view

    def _setup_pages(self):
        g = globals()
        for idx, (name, viewcls, iconname) in enumerate(PAGES):
            view = g[viewcls](self)
            label = gtk.Label(name)
            try:
                icon = icontheme.load_icon(iconname, MENU_ICON_SIZE, 0)
            except:
                icon = None
                logging.error('icon %s not found in current theme' % iconname)
            self.notebook.append_page(view, label)
            self.menu_model.append((icon, name, idx))
        self.notebook.set_current_page(0)
        self.menu_view.get_selection().connect('changed', self._on_select_change)

    def _on_close(self, widget, data=None):
        gtk.main_quit()

    def _on_select_change(self, widget):
        (model, it) = self.menu_view.get_selection().get_selected()
        self.notebook.set_current_page(model.get_value(it, 2))


main_window = MainWindow()

def start_app():
    main_window.show_all()
    gtk.main()

if __name__ == '__main__':
    start_app()

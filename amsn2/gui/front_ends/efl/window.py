
from constants import *
import ecore
import ecore.evas
import ecore.x
import etk

from amsn2.gui import base
from amsn2.core.views import MenuView, MenuItemView

class aMSNWindow(etk.Window, base.aMSNWindow):
    def __init__(self, amsn_core):     
        self._amsn_core = amsn_core
        self._vbox = etk.VBox()
        etk.Window.__init__(self,title="aMSN",
                               size_request=(MIN_WIDTH,MIN_HEIGHT),
                               child=self._vbox)
        self.on_key_down(self._on_key_down)
        self.fullscreen = False
        self.wmclass_set(WM_NAME, WM_CLASS)
        self.resize(WIDTH, HEIGHT)
        self._has_menu = False
        self._vbox.show()

    @property
    def _evas(self):
        return self.toplevel_evas_get()

    def show(self):
        self.show_all()

    def hide(self):
        self.hide()
        
    def setTitle(self, text):
        self.title_set(text)

    def setMenu(self, menu):
        if menu is None:
            if self._has_menu:
                #Remove the menubar
                menu_bar = self._vbox.child_get_at(etk.VBox.START, 0)
                menu_bar.parent = None
                self._has_menu = False
        else:
            if self._has_menu:
                menu_bar = self._vbox.child_get_at(etk.VBox.START, 0)
                #Clear the menubar:
                for menu_item in menu_bar.items_get:
                    menu_bar.remove(menu_item)
            else:
                menu_bar = etk.MenuBar()
                self._vbox.prepend(menu_bar, etk.VBox.START, etk.VBox.FILL, 0)
                self._has_menu = True
            createEtkMenuFromMenuView(menu.items, menu_bar)
        
    
    def setChild(self, child):
        obj = self.getChild()
        if obj is not None:
            obj.parent = None
        self._vbox.append(child, etk.VBox.START, etk.VBox.EXPAND_FILL, 0)

    def getChild(self):
        if self._has_menu:
            pos = 1
        else:
            pos = 0
        pass
        return self._vbox.child_get_at(etk.VBox.START, pos)

    def toggleMenu(self):
        if self._has_menu:
            menu_bar = self._vbox.child_get_at(etk.VBox.START, 0)
            if menu_bar.is_visible():
                menu_bar.hide()
            else:
                menu_bar.show()

    def _on_key_down(self, obj, event):
        if event.keyname in ("F6", "f"):
            self.fullscreen = not self.fullscreen
        elif event.keyname in ("F5", "b"):
            self.decorated = not self.decorated
        elif (event.keyname == "m" and
              event.modifiers == etk.core.c_etk.EventEnums.MODIFIER_CTRL):
            self.toggleMenu()

def createEtkMenuFromMenuView(items, etkmenu):
    for item in items:
        if item.type is MenuItemView.CASCADE_MENU:
            m = etk.Menu()
            mi = etk.MenuItem(label=item.label)
            createEtkMenuFromMenuView(item.items, m)
            mi.submenu = m
            etkmenu.append(mi)
        elif item.type is MenuItemView.COMMAND:
            if item.icon is None:
                mi = etk.MenuItem(label=item.label)
            else:
                #TODO: icon
                mi = etk.MenuItemImage(label=item.label)
            #TODO: define the prototype of item.command
            #=> for the moment, it's item.command() i.e. no argument
            def cb(obj):
                item.command()
            mi.on_activated(cb)
            etkmenu.append(mi)
        elif item.type is MenuItemView.SEPARATOR:
            mi = etk.MenuItemSeparator()
            etkmenu.append(mi)

        #TODO: CHECKBUTTON, RADIOBUTTON, RADIOBUTTONGROUP

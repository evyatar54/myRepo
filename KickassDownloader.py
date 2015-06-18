#!/usr/bin/env python

import pygtk, time
pygtk.require('2.0')
import gtk
from SearchModules.KickassSearcher import *
from torrents_selector import torrents_selector


class upper_toolbar(gtk.HBox):

    def activated(self, Widget, Entry):
        if Entry.get_text():
            self.queriesHolder.add_query(Entry.get_text())
        Entry.set_text("")

    def showMyself(self):
        self.button.show()
        self.textEntry.show()

    def __init__(self, queriesHolder):
        gtk.HBox.__init__(self)
        self.queriesHolder = queriesHolder
        #
        self.textEntry = gtk.Entry()
        self.textEntry.connect("activate", self.activated, self.textEntry)
        self.pack_start(self.textEntry, True)

        #
        self.button = gtk.Button('Add')
        self.button.connect_object("clicked", self.activated, self, self.textEntry)
        self.pack_start(self.button, False)

        self.showMyself()


###############################################################################################################3

class queryHolder(gtk.HBox):

    def __init__(self, holder, query_name):
        gtk.HBox.__init__(self)
        self.holder = holder
        self.removeButton = gtk.Button("Remove")
        self.removeButton.connect("clicked", self.remove_self)
        self.button = gtk.Button(query_name)
        self.button.connect("event", self.edit_name)
        self.button.set_relief(gtk.RELIEF_NONE)
        self.entry  = gtk.Entry()
        self.entry.connect("activate", self.enter_name, self.entry)
        self.pack_start(self.button,True)
        self.pack_start(self.entry,True)
        self.pack_start(self.removeButton,False)
        self.button.show()
        self.entry.hide()
        self.removeButton.show()
        self.show()

    def get_query_name(self):
        return self.button.get_label()

    def edit_name(self, button, event):
        if event.type == gtk.gdk.BUTTON_PRESS:
            self.holder.focus_item(self)
            self.entry.set_text(self.button.get_label())
            self.entry.set_position(len(self.button.get_label())-1)
            self.entry.grab_focus()
            self.entry.show()
            self.button.hide()

    def lose_focus(self):
        self.button.set_label(self.entry.get_text())
        self.button.show()
        self.entry.hide()

    def enter_name(self, Widget, entry):
        if(entry.get_text()):
            self.button.set_label(entry.get_text())
        self.entry.hide()
        self.button.show()

    def remove_self(self, Widget):
        self.destroy()




############################################################################################################################3    



class QueriesHolder(gtk.VBox):

    def __init__(self):
        gtk.VBox.__init__(self)
        self.focused = None
        self.show()

    def add_query(self,query_name):
        query = queryHolder(self, query_name)
        self.pack_start(query, False)

    def focus_item(self, item):
        if(self.focused):
            self.focused.lose_focus()
        self.focused = item

    def remove_all(self):
        for q in self.get_children():
            self.remove(q)



##############################################################################################################################3



class mainWindow:

    def init_top_toolbar(self, sh):
        self.topToolbar = upper_toolbar(sh)
        self.topToolbar.set_border_width(10)

    def init_qeries_holder(self):
        self.queriesHolder = QueriesHolder()

    def init_vbox(self):
        self.Vstruct = gtk.VBox()
        self.Vstruct.pack_start(self.queriesHolder, True)
        self.queriesHolder.show()
        self.Vstruct.show()

    def init_send_button(self):
        self.send_button = gtk.Button("Send List")
        self.send_button.connect("clicked", self.send_queriess)
        self.window.action_area.pack_start( self.send_button, True, True, 0)
        self.send_button.show()

    def send_queriess(self, Widget):
        self.window.set_sensitive(False)
        queries = []
        for q in self.queriesHolder.get_children():
            queries.append(q.get_query_name())
        self.queriesHolder.remove_all()

        searcher = KickassSearcher()
        results = searcher.search(queries)

        selector = torrents_selector(self.window, results)


    def __init__(self):
        self.window = gtk.Dialog()
        self.window.set_keep_above(False)
        self.window.set_size_request(600,400)
        self.window.set_title("Kickass Downloader")
        self.window .set_border_width(0)

        self.scrolledWindow= gtk.ScrolledWindow()
        self.scrolledWindow.set_border_width(10)
        self.scrolledWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)

        self.window.connect("destroy", gtk.main_quit)


        self.init_qeries_holder()

        self.init_top_toolbar(self.queriesHolder)

        self.window.vbox.pack_start(self.topToolbar,False)
        self.topToolbar.show()


        self.window.vbox.pack_start(self.scrolledWindow, True, True, 0)
        self.scrolledWindow.show()
        self.init_vbox()
        self.init_send_button()
        self.scrolledWindow.add_with_viewport(self.Vstruct)
        self.window.show()

    def main(self):
        gtk.main()


if __name__ == "__main__":
    win = mainWindow()
    win.main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#!/usr/bin/env python

import pygtk, time
pygtk.require('2.0')
import gtk
from SearchModules.KickassSearcher import *
from torrents_selector import torrents_selector

class down_toolbar(gtk.Table):
  
  def __init__(self,songsHolder=None):
    gtk.Table.__init__(self, 1, 6, True)
    self.songsHolder = songsHolder
    self.send_button = gtk.Button("Send Songs")
    self.send_button.connect("clicked", self.send_songs)
    self.attach(self.send_button, 5,6,0,1)
    self.send_button.show()
    #self.show()
    
  def send_songs(self, Widget):
    queries =  []
    for song in self.songsHolder.get_children():
      queries.append(song.get_song_name() )
    torrentList = queries
    search()

class upper_toolbar(gtk.HBox):
  
  def activated(self, Widget, Entry):
    if Entry.get_text():
      self.songsHolder.add_song(Entry.get_text())
    Entry.set_text("")
  
  def showMyself(self):
    self.button.show()
    self.textEntry.show()
  
  def __init__(self, songsHolder):
    gtk.HBox.__init__(self)
    self.songsHolder = songsHolder
    #
    self.textEntry = gtk.Entry()
    self.textEntry.connect("activate", self.activated, self.textEntry)
    self.pack_start(self.textEntry, True)
    
    #
    self.button = gtk.Button('Add')
    self.button.connect_object("clicked", self.activated, self, self.textEntry)
    self.pack_start(self.button, False)
    
    self.showMyself()
    ##

class songHolder(gtk.HBox):
  
  def __init__(self, holder, song_name):
    gtk.HBox.__init__(self)
    self.holder = holder
    self.removeButton = gtk.Button("Remove")
    self.removeButton.connect("clicked", self.remove_self)
    self.button = gtk.Button(song_name)
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
    
  def get_song_name(self):
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
    
class songsHolder(gtk.VBox):
  
  def __init__(self):
    gtk.VBox.__init__(self)
    self.focused = None
    self.show()
  
  def add_song(self,song_name):
    song = songHolder(self, song_name)
    self.pack_start(song, False)
    
  def focus_item(self, item):
    if(self.focused):
      self.focused.lose_focus()
    self.focused = item
    
class mainWindow:
  
  def init_top_toolbar(self, sh):
    self.topToolbar = upper_toolbar(sh)
    self.topToolbar.set_border_width(10)
  
  def init_songs_holder(self):
    self.songsHolder = songsHolder()
  
  def init_down_toolbar(self):
    self.down_toolbar = down_toolbar(songsHolder=self.songsHolder)
    
  def init_vbox(self):
    self.init_down_toolbar()
    self.Vstruct = gtk.VBox()
    self.Vstruct.pack_start(self.songsHolder, True)
    self.songsHolder.show()  
    self.down_toolbar.show()
    self.Vstruct.show()
  
  def init_send_button(self):
    self.send_button = gtk.Button("Send List")
    self.send_button.connect("clicked", self.send_songs)
    self.window.action_area.pack_start( self.send_button, True, True, 0)
    self.send_button.show()
  
  def send_songs(self, Widget):
    queries = []
    for song in self.songsHolder.get_children():
      queries.append(song.get_song_name())
    
    results = search(queries)
    selector = torrents_selector(results)
    
  def remove_all(self):
    for w in self.window.vbox:
      self.window.vbox.remove(w)
    self.window.show()
    
  def __init__(self):
    self.window = gtk.Dialog()
    self.window.set_size_request(600,400)
    self.window.set_title("Kickass Downloader")
    self.window .set_border_width(0)
    
    self.scrolledWindow= gtk.ScrolledWindow()
    self.scrolledWindow.set_border_width(10)
    self.scrolledWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
    
    self.window.connect("destroy", gtk.main_quit)
    
    
    self.init_songs_holder()
    
    self.init_top_toolbar(self.songsHolder)
    
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
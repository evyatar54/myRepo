import pygtk
pygtk.require('2.0')
import gtk

from SearchModules.KickassSearcher import QueryResults
from LinksDownloader import LinksDownloader


class torrent_descriptor(gtk.TreeView):
  
  def init_cols(self):
    colomns_names = ["Selected","name","size","seed","age"]
    
    cell_tog = gtk.CellRendererToggle()
    cell_tex = gtk.CellRendererText()
    cell_tog.set_property( "activatable", True)

    def on_selected_toggled (renderer, path):
      self.liststore[path][0] = not self.liststore[path][0]
      #print self.liststore[path][0]
    
    cell_tog.connect ("toggled", on_selected_toggled)
    
    for i, name in enumerate(colomns_names):
      if i == 0:
	column_name = gtk.TreeViewColumn(name)
	column_name.pack_start( cell_tog, expand=False)
	column_name.set_attributes( cell_tog, active=0)
	#column_name.set_sort_column_id(2)
      else:
	column_name = gtk.TreeViewColumn(name,cell_tex, text=i)
      self.append_column(column_name)

      
  def __init__(self,results=[]):
    self.reses = results
    self.liststore = gtk.ListStore(bool, str, str, str, str)
    for r in results:
      name_len = len(r.name)
      arr = [False, r.name[:min(40,name_len)], r.size, r.seed, r.age]
      #self.links.append(r.download_link)
      self.liststore.append(arr)
    gtk.TreeView.__init__(self, self.liststore)
    self.init_cols()
    self.show_all()
    
  def get_list(self):
    return self.liststore
  
  def get_reses(self):
    return self.reses
    
class horizontal_holder(gtk.VBox):
  
  def __init__(self,qr=QueryResults()):
    gtk.VBox.__init__(self)
    self.set_border_width(15)
    self.scroller = gtk.ScrolledWindow()
    self.scroller .set_border_width(5)
    self.scroller .set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
    self.scroller .set_size_request(400,150)
    self.scroller.show()
    self.results = qr
    self.holder = gtk.VBox()
    self.holder.show()
    
    self.query = gtk.Label(qr.query)
    self.query.show()
    self.pack_start(self.query,False)
    
    self.scroller.add_with_viewport(self.holder)
    self.add_tables(qr.results)
    self.pack_start(self.scroller)
        
    self.show()

  def add_tables(self,results=[]):
    ti = torrent_descriptor(results)
    self.holder.pack_start(ti,True)
      
      
class torrents_selector():

  def init_send_button(self):
    self.torrents_list = []
    self.send_button = gtk.Button("Download Torrents")
    self.send_button.connect("clicked", self.update_list)
    self.window.action_area.pack_start( self.send_button, True, True, 0)
    self.send_button.show()
  
  def update_list(self, Widget):
    torrents = []
    for hh in self.h_holders:
      torrents.extend(self.get_torrents_from_holder(hh))
    self.torrents_list = torrents
    downloader = LinksDownloader()
    downloader.download(torrents)
    self.window.destroy()
    self.parent.set_sensitive(True)
    

  def get_torrents_from_holder(self, hh):
    torrs = []
    children = hh.holder.get_children()
    if children:
      model=children[0]
      ls = model.get_list()
      for i,l in enumerate(ls):
	if l[0]:
	  torrs.append(model.get_reses()[i])
    return torrs
  
    
  def activate_parent(self,w):
      self.parent.set_sensitive(True)
      
  def __init__(self,parent, QRs):
    self.window = gtk.Dialog()
    self.window.set_size_request(800,600)
    self.window.set_title("Kickass Downloader")
    self.window .set_border_width(0)
    self.parent = parent
    self.window.connect("destroy", self.activate_parent)
    
    self.scrolled_window = gtk.ScrolledWindow()
    self.scrolled_window.set_border_width(10)
    self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
    self.vertical_holder = gtk.VBox()
    self.scrolled_window.add_with_viewport(self.vertical_holder)
    self.vertical_holder.show()
    self.scrolled_window.show()
    
    self.window.vbox.pack_start(self.scrolled_window)
    self.h_holders = []
    for qr in QRs:
      #namei = qr.query
      hh = horizontal_holder(qr)
      self.h_holders.append(hh)
      self.vertical_holder.pack_start(hh, True, True, 0)
    
    self.init_send_button()
    self.window.show_all()
      
    
  def main(self):
    gtk.main()  
    

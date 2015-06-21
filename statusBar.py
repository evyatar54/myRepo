import gtk

class ProgressWin(gtk.Dialog):
    
    def __init__(self,n):
        gtk.Dialog.__init__(self)
        self.query_num = n

        self.status = gtk.Label()
        self.status.set_size_request(600,30)
        self.vbox.pack_start(self.status)

        self.pb = gtk.ProgressBar()
        self.pb.set_size_request(600,30)
        self.vbox.pack_start(self.pb)

        self.show_all()
        self.set_keep_above(True)

    def set_status(self,status):
        self.status.set_text(status)

    def on_query_found(self):
        if self.pb.get_fraction() < 1:
            self.pb.set_fraction(self.pb.get_fraction() + 1.0/self.query_num)


import gzip, urllib2, sys
from StringIO import *
import os, subprocess, platform

from statusBar import ProgressWin
import gtk

class LinksDownloader:


    def __init__(self):
        pass

    def retrieve_path_by_os(self, name):
        path = ""
        try:
            # print "platform:-", platform.system().lower(),"-"/home/walrus/Downloads
            if 'windows' in platform.system().lower():
                if not os.path.isdir(os.path.abspath("C:/Users/Walrus/Downloads/torrents")):
                    os.makedirs(os.path.abspath("C:/Users/Walrus/Downloads/torrents"))
                home_temp = os.path.abspath("C:/Users/Walrus/Downloads/torrents")
            elif 'linux' in sys.platform.lower():
                if not os.path.isdir(os.path.abspath(os.environ['HOME'] + "/Downloads/torrents")):
                    os.makedirs(os.path.abspath(os.environ['HOME'] + "/Downloads/torrents"))
                home_temp = os.path.abspath(os.environ['HOME'] + "/Downloads/torrents")
            else:
                print "Unsupported Operating System"
                return ""
        except:
            return ""
        path = os.path.join(home_temp,name)
        print "path: ", path
        return path

    def download(self, links_array):
        files = []
        pw = ProgressWin(len(links_array))
        #for links in links_array:
        for link in links_array:
            #for link in links:
            name = link.name+".torrent"
            url  = link.download_link
            pw.set_status( "Downloading: " + name )

            while gtk.events_pending():
                gtk.main_iteration()


            path = self.retrieve_path_by_os(name)

            if not path:
                print "Error Opening File"
                continue

            files.append(path)
            try:
                output = open(path, 'wb')
                req = urllib2.Request(url)
                opener = urllib2.build_opener()
                response = opener.open(req)
                data = response.read()
                if response.info().get('Content-Encoding', '').lower() == 'gzip':
                    sio = StringIO(data)
                    gzipper = gzip.GzipFile(fileobj=sio)
                    plain = gzipper.read()
                    data = plain
                output.write(data)
            except IOError:
                print "Error downloading file: ", path
            finally:
                output.close()
                pw.on_query_found()
            try:
                if path:
                    if platform.system().lower().startswith('linux'):
                        subprocess.call(["xdg-open", path])

                    elif platform.system().lower().startswith("windows"):
                        os.startfile(path)
                else:
                    print "no path!"
            except:
                print "Error openning file"
        pw.destroy()
        print "done !!!!!!!!!!"
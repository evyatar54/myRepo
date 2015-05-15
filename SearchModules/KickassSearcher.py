from statusBar import ProgressWin
from KickassAPI import *
from requests import ConnectionError
from StubSearcher import Searcher

import gtk
  
import sys, traceback


class QueryResults:
  
  def __init__(self, query="", results=[]):
    self.query = query
    self.results = results
    
   
class KickassSearcher(Searcher):
    def __init__(self):
	Searcher.__init__(self)
	
    def search(self, queries):
	
	pw = ProgressWin(len(queries))
	results = []
	for q in queries:
	    while gtk.events_pending():
		gtk.main_iteration()
	    pw.set_status( "searching: " + q )
	    result = None
	    try:
		result = Search(q)
		resList = result.list()
	    except ValueError:
		print "no matches found for:\n\t", q
		#traceback.print_exc(file=sys.stdout)
		resList = []
	    except ConnectionError:
		print "Connection Error: Check connection or firewall"
		resList = []
	    except:
		print "Unknown Error:"
		#traceback.print_exc(file=sys.stdout)
		resList = []
	    #finally:
	    pw.on_query_found()
	    QR = QueryResults(q, resList)
	    results.append(QR)
	pw.destroy()
	return results
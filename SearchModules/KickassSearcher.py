
from KickassAPI import *

torrentList = []

def getQueries():
  q = torrentList
  #q = raw_input("Enter Qurey: ")
  return q

  
  
class QueryResults:
  
  def __init__(self, query="", results=[]):
    self.query = query
    self.results = results
    
def search(queries):
  #try:
    results = []
    #queries = getQueries()
    v = 1
    for q in queries:
      print "searching:\n", q
      result = None
      try:
	result = Search(q)
	resList = result.list()
      except ValueError:
	print "no matches found for:\n", q
	resList = []
      QR = QueryResults(q, resList)
      results.append(QR)

    return results
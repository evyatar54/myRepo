#!/usr/bin/python

from KickassAPI import *
import gzip, urllib2, sys
from StringIO import *

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

    
import os, subprocess
def retrieve_path_by_os(name):
  path = ""
  try:
    if os.platform == "Win32" or os.platform == "Win64":
      if not os.path.isdir(os.path.abspath("C:\\temp_torrs")):
	os.makedirs(os.path.abspath("C:\\temp_torrs"))
      home_temp = os.path.abspath("C:\\temp_torrs")|
    elif sys.platform.startswith('linux'):    
      if not os.path.isdir(os.path.abspath(os.environ['HOME'] + "/tmp")):
	os.makedirs(os.path.abspath(os.environ['HOME'] + "/tmp"))
      home_temp = os.path.abspath(os.environ['HOME'] + "/tmp")
    else:
      print "Unsupported Operating System"
      return ""
  except:
    return ""
  path = os.path.join(home_temp,name)
  return path
    
def download(links_array):
  files = []
  for links in links_array:
    for link in links:
      name = link.name+".torrent"
      url  = link.download_link
      print "downloading: ", name
      
      path = retrieve_path_by_os(name)
      
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
	if response.info()['content-encoding'] == 'gzip':
	    sio = StringIO(data)
	    gzipper = gzip.GzipFile(fileobj=sio)
	    plain = gzipper.read()
	    data = plain
	output.write(data)
      except IOError:
	print "Error downloading file: ", path
      finally:
	output.close()
      try:
	if path:
	  if sys.platform.startswith('linux'):
	    subprocess.call(["xdg-open", path])
	  else:
	      os.startfile(file)
      except:
	print "Error openning file"
	
  print "done !!!!!!!!!!"
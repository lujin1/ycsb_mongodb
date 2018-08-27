# /bin/python
import os
from pymongo import MongoClient
import ConfigParser

def drop_collection(mongodb_url):
	print ("drop ycsb.usertable")
	client = MongoClient(mongodb_url)
	db = client.ycsb
	collection = db.usertable
	result = collection.drop()
	print (result)
	
def run(mongodb_url, recordcount, threads, work):
	result = os.popen('sh ycsb.sh %s %s' %(mongodb_url, recordcount, threads, work))
	print (result)

def get_model(work):
	with open(work,'r') as f:
		if "insertproportion" in line:
			insertproportion = int(line.split('=')[1])
			return insertproportion

if __name__=="__main__":
	conf = ConfigParser.ConfigParser() 
	conf.read("config.ini")
	mongodb_url = conf.get("mongodb","mongodb_url")
	work = conf.get("ycsb","work")
	recordcount_list = conf.get("ycsb","recordcount_list")
	threads_list = conf.get("ycsb","threads_list")
	insertproportion = get_model(work)
	for recordcount in recordcount_list:
		for threads in threads_list:
			drop_collection(mongodb_url)
			run(mongodb_url, recordcount, threads, work)
	print (os.popen('cat lujin.txt'))

# encoding=utf-8
import time
import commands
from pymongo import MongoClient
import ConfigParser

def drop_collection(mongodb_url):
        print ("drop ycsb.usertable")
        client = MongoClient(mongodb_url)
        db = client.ycsb
        collection = db.usertable
        result = collection.drop()
        print (result)

def run(mongodb_url, recordcount, threads, work, insertproportion, ycsb_dir, prometheus_url):
        result = commands.getoutput('sh ycsb.sh %s %s %s %s %d %s' %(mongodb_url, recordcount, threads, work, insertproportion, ycsb_dir, prometheus_url))
        print (result)

def get_model(work):
        with open(work,'r') as f:
                for line in f.readlines():
                        if "insertproportion" in line:
                                insertproportion = int(line.split('=')[1])
                                return insertproportion

if __name__=="__main__":
        conf = ConfigParser.ConfigParser()
        conf.read("config.ini")
        mongodb_url = conf.get("mongodb","mongodb_url")
        work = conf.get("ycsb","work")
        recordcount_list = conf.get("ycsb","recordcount_list").split(',')
        threads_list = conf.get("ycsb","threads_list").split(',')
        insertproportion = get_model(work)
        ycsb_dir = conf.get("ycsb","ycsb_dir")
        prometheus_url = conf.get("prometheus","prometheus_url")
        for recordcount in recordcount_list:
                for threads in threads_list:
                        drop_collection(mongodb_url)
                        run(mongodb_url, recordcount, threads, work, insertproportion, ycsb_dir, prometheus_url)
                        time.sleep(600)
        print (commands.getoutput('cat lujin.txt'))

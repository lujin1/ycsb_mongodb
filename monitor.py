# encoding=utf-8
__author__ = 'lujin'
import requests
import json
import time
from datetime import datetime,timezone,timedelta
import xlrd

def strf_strf_utc(local_time,time_type):
    timeArray = time.strptime(local_time, "%Y-%m-%d %H:%M:%S")
    # 转换为时间戳:
    timeStamp = int(time.mktime(timeArray))
    # print(timeStamp - 3600)
    if time_type == 'start':
        timeStamp = timeStamp - 3600
    utc_time = datetime.utcfromtimestamp(timeStamp)
    utc_time_TZ = utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    return utc_time,utc_time_TZ

def strf_utc_8(utc_time):
    dt = utc_time.replace(tzinfo=timezone.utc)
    tzutc_8 = timezone(timedelta(hours=8))
    strf_utc_8 = dt.astimezone(tzutc_8)
    strf_utc_8_TZ = strf_utc_8.strftime("%Y-%m-%dT%H:%M:%SZ")
    return strf_utc_8,strf_utc_8_TZ

def prometheus_query_range(prometheus_url,key,start,end):
    expr = 'bosh_job_%s{bosh_deployment="mongodb-single-benchmark",bosh_job_az="z1",bosh_job_id="797c26f9-d273-42d5-8170-0c9cebf8f6d0",bosh_job_index="0",bosh_job_ip="42.159.5.224",bosh_job_name="mongodb",bosh_name="x-bosh",bosh_uuid="09113c6d-46c2-4f7f-9ea8-8b8c7af33976",environment="cf",instance="localhost:9190",job="bosh"}&start=%s&end=%s&step=60s' %(key,start, end)
    request = prometheus_url + '/api/v1/query_range?query=%s' % (expr)
    response = requests.get(request)
    status_code = response.status_code
    if status_code == 200:
        result = json.loads(response.text)
        status = result['status']
        if status == 'success':
            data = result['data']['result'][0]['values']
            data_list = []
            for i in data:
                data_list.append(round(float(i[1])))
            count_0 = data_list.count(0)
            for n in range(count_0):
                data_list.remove(0)
            try:
                max_data = max(data_list)
                min_data = min(data_list)
                sum = 0.0
                for item in data_list:
                    sum += item
                avg_data = round(sum/len(data_list),1)
                return max_data,min_data,avg_data
            except:
                return 0,0,0

if __name__=="__main__":
    date = '''2018/8/29 8:09:16,
2018/8/29 9:14:22,
2018/8/29 10:19:27,
2018/8/29 11:24:43,
2018/8/29 12:29:57,
2018/8/29 13:35:08,
2018/8/28 7:12:15,
2018/8/28 8:23:24,
2018/8/28 9:34:19,
2018/8/29 14:51:38,
2018/8/29 16:08:20,
2018/8/29 17:24:55,
2018/8/28 15:47:50,
2018/8/28 17:58:02,
2018/8/28 20:08:06,
2018/8/29 19:29:56,
2018/8/29 21:34:59,
2018/8/29 23:40:03
'''
    date_list = date.replace('\n','').split(',')
    for item in date_list:
        end_time = item.replace('/','-')
        utc_time_end_time = strf_strf_utc(end_time,'end')[0]
        end = strf_utc_8(utc_time_end_time)[1]
        print(strf_utc_8(utc_time_end_time)[1])
        utc_time_start_time = strf_strf_utc(end_time,'start')[0]
        start = strf_utc_8(utc_time_start_time)[1]
        print(strf_utc_8(utc_time_start_time)[1])
        prometheus_url = "http://wise-prometheus.chinanorth.cloudapp.chinacloudapi.cn"
        keys = ["cpu_user","cpu_sys","cpu_wait","mem_percent"]
        for key in keys:
            max_data, min_data, avg_data = prometheus_query_range(prometheus_url,key,start,end)
            print(key)
            print(max_data, min_data, avg_data )
# data = xlrd.open_workbook('C:\\Users\\lu.jin\\Desktop\\test.xls')
# table = data.sheet_by_name(u'Sheet1')
# print(table.col_values(1))
# end_time_list = table.col_values(1)
# for i in end_time_list:
#     if i != end_time_list[0]:
#         time = xlrd.xldate_as_tuple(i,0)
#         end_time = "%s-%s-%s %s:%s:%s"%(time[0],time[1],time[2],time[3],time[4],0)
#         print (end_time)
#         print(type(end_time))



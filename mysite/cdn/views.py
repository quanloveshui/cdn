from django.shortcuts import render
import pymysql,json
from django.http import HttpResponse
from pyecharts import Line
from django.template import loader
import http.client
import hashlib
from urllib import parse


#gsd响应时间监控页面

tmp = 0

"""def getdata(request):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1qazXDR%', db='cdn', charset='utf8')
    cursor = conn.cursor()
    sql = "SELECT `time`,`total_time` FROM `cdn_tcp`"
    cursor.execute(sql)
    row = cursor.fetchall()
    ones = [[i[0]*1000, i[1]] for i in row]
    data = json.dumps(ones)
    return HttpResponse(data)"""

#获取增量数据
def getdata(request):
    global tmp
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1qazXDR%', db='cdn', charset='utf8')
    cursor = conn.cursor()
    if tmp > 0:
        sql = "select `time`,`total_time` FROM `cdn_tcp`  where time > %s" % (tmp/1000)
    else:
        sql = "SELECT `time`,`total_time` FROM `cdn_tcp`"
    cursor.execute(sql)
    arr = []
    row = cursor.fetchall()
    ones = [[i[0]*1000, i[1]] for i in row]
    for i in ones:
        arr.append(i)
    if len(arr)>0:
        tmp=arr[-1][0]
    data = json.dumps(arr)
    return HttpResponse(data)


def main(request):
    return render(request,'gsd.html')


#cdn 各节点响应状态

def index(request):
    return render(request,'index.html')

def url_parse(url):
    dict_url = {}
    result = parse.urlparse(url)
    host = result.netloc
    path = result.path
    query = result.query
    dict_url["host"] = host
    dict_url["path"] = path
    dict_url["query"] = query
    return dict_url


def check(request):
    result={}
    request.encoding = 'utf-8'
    if 'url' in request.GET:
        url=request.GET['url']
        while True:
            a = url_parse(url)
            host = a["host"]
            path = a["path"]
            query = a["query"]
            conn=http.client.HTTPConnection(host,timeout=5)
            conn.request("GET",path + "?" + query)
            response=conn.getresponse()  
            stat = response.status     
            head=response.getheaders() 
            body = response.read()
            conn.close()
            if stat == 302:
                for i in head:
                    if "Location" in i:
                        url=i[1]
                        result[host]=stat
            else:
                result[host]=stat
                #print(result)
                break
        return render(request,'result.html',{"result":result})
    else:
        message = '你提交了空表单'
        return HttpResponse(message)

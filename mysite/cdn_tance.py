#!/usr/bin/env python
import pycurl
from io import BytesIO
from urllib import parse
import time
import pymysql

#监控gsd响应时间

class cdn(object):
    def __init__(self,url):
        self.buffer = BytesIO()
        self.c = pycurl.Curl()
        self.c.setopt(pycurl.URL,url)
        #self.c.setopt(pycurl.FOLLOWLOCATION, 1) #是否开启重定向
        #self.c.setopt(pycurl.MAXREDIRS, 1) #重定向最大次数
        self.c.setopt(pycurl.WRITEDATA, self.buffer)
        self.c.setopt(pycurl.WRITEHEADER,self.buffer)

        try:
            self.c.perform() #提交内容
        except Exception as e:
            print('connection error:' + str(e))
            self.buffer.close()
            self.c.close()
    

    def getinfo(self,url):
        h1 = self.c.getinfo(pycurl.HTTP_CODE)  # 状态码
        h2 = self.c.getinfo(pycurl.TOTAL_TIME)  # 传输结束总消耗时间
        h3 = self.c.getinfo(pycurl.NAMELOOKUP_TIME)  # DNS解析时间
        h4 = self.c.getinfo(pycurl.CONNECT_TIME)  # 建立连接时间
        h5 = self.c.getinfo(pycurl.PRETRANSFER_TIME)  # 建立连接到准备传输消耗时间
        h6 = self.c.getinfo(pycurl.STARTTRANSFER_TIME)  # 从建立连接到传输开始消耗时间
        h7 = self.c.getinfo(pycurl.REDIRECT_TIME)  # 重定向消耗时间
        h8 = self.c.getinfo(pycurl.SIZE_UPLOAD)  # 上传数据包大小
        h9 = self.c.getinfo(pycurl.SIZE_DOWNLOAD)  # 下载数据包大小
        h10 = self.c.getinfo(pycurl.SPEED_DOWNLOAD)  # 平均下载速度
        h11 = self.c.getinfo(pycurl.SPEED_UPLOAD)  # 平均上传速度
        h12 = self.c.getinfo(pycurl.HEADER_SIZE)  # http头文件大小
        #h13 = self.c.getinfo(pycurl.EFFECTIVE_URL) #重定向url
        #h14 = self.c.getinfo(pycurl.REDIRECT_COUNT) #重定向次数
        info ='''
            http状态码：%s
            传输结束总时间：%.2f ms
            DNS解析时间：%.2f ms
            建立连接时间：%.2f ms
            准备传输时间：%.2f ms
            传输开始时间：%.2f ms
            重定向时间：%.2f ms
            上传数据包大小：%d bytes/s
            下载数据包大小：%d bytes/s
            平均下载速度：%d bytes/s
            平均上传速度：%d bytes/s
            http头文件大小：%d byte
        ''' %(h1,h2*1000,h3*1000,h4*1000,h5*1000,h6*1000,h7*1000,h8,h9,h10,h11,h12)
        #print(info)
        self.buffer.close()
        self.c.close()
        return h2*1000,h3*1000,h4*1000

    def getTime(self):
        return str(int(time.time()) + 8 * 3600)
        

if __name__ == '__main__':
    #url = "http://gslbbtos.itv.cmvideo.cn:8080/000000001001/3000000001000028638/3000000001000028638_1500000_20180704_090000_49.ts?channel-id=FifastbLive&livemode=1&Contentid=3000000001000028638&stbId=toShengfenFIFA&usergroup=g28093100000&owaccmark=3000000001000028638&owchid=FifastbLive&owsid=8312291672011781918&owflow=3&owflow==3"
    url = "http://gslbbtos.itv.cmvideo.cn:80/000000001001/3000000001000028638/3000000001000028638.m3u8?channel-id=FifastbLive&livemode=1&Contentid=3000000001000028638&stbId=toShengfenFIFA&usergroup=g28093100000"
    while True:    
        respon = cdn(url)
        data = respon.getinfo(url)
        t = respon.getTime()
        db = pymysql.connect(host='192.168.149.129', port=3306, user='root', passwd='1qazXDR%', db='cdn', charset='utf8')
        db.autocommit(True)
        c = db.cursor()
        sql = "INSERT INTO `cdn_tcp` (`total_time`,`dns_time`,`conn_time`,`time`) VALUES('%.2f', '%.2f', '%.2f', '%d')" % (data[0], float(data[1]), float(data[2]), int(t))
        ret = c.execute(sql)
        print("OK")
        time.sleep(2)

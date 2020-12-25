import urllib.request
f=open('all.txt','a',encoding='UTF-8')
for day in range(1,31):
    if day < 10:
        day = '0'+str(day)
    url='http://paper.people.com.cn/rmrb/html/2020-09/'+str(day)+'/nbs.D110000renmrb_01.htm'
    html=urllib.request.urlopen(url).read().decode('UTF-8')
    f.write(html)
    print("下载一次完成")
f.close()
print('网页下载完成!')
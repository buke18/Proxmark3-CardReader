#!/usr/bin/python
# -*- coding: UTF-8 -*-
import subprocess, os, binascii
from bankcode import *

def getCardType(cardnumber):
    for len in range(5, 9):
        if bankcode.has_key(cardnumber[0:len]):
            return bankcode[cardnumber[0:len]]
    return ''

def getHistory(historystr,number):
    if len(historystr) >= 24:
        time = "20" + historystr[0:2] + "-" + historystr[2:4] + "-" + historystr[4:6] + " " + historystr[6:8] + ":" + historystr[8:10] + ":" + historystr[10:12]
        money = historystr[12:24]
        place = binascii.a2b_hex(historystr[44:84]).decode('gbk')
        return str(number) + "	" + time + "		" + str(float(money)/100) + "			"  + place
    else:
        return ''

os.system("clear")
# 启动Proxmark3,此处自行设置proxmark3客户端所在的路径以及设备名
pm3 = subprocess.Popen("/home/satan/Program/proxmark3-iceman/client/proxmark3 /dev/ttyACM0", shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
# 选择支付系统PSE-1PAY.SYS.DDF01,并建立连接
pm3.stdin.write('hf 14a raw -c -s -p 0200A404000E315041592E5359532E4444463031\n')
# 借记卡最后一位为1贷记卡为2
pm3.stdin.write('hf 14a raw -c 0300A4040008A000000333010101 -p\n')
# 发送银行卡信息查询命令
pm3.stdin.write('hf 14a raw -c 0200B2010C -p\n')
# 发送卡主信息查询指令
pm3.stdin.write('hf 14a raw -c 0300B2020C -p\n')
# 循环发送消费记录查询命令
for i in range(1, 11):
    head = '02'
    if i % 2 == 0: head = '03'
    if i != 10: i = "0" + str(i)
    pm3.stdin.write('hf 14a raw -c ' + head + '00B2'+ str(i) +'5C00 -p\n')
# 断开银行卡连接
pm3.stdin.write('hf 14a raw -a\n')
out = pm3.communicate()[0]
outarray = out.split("pm3 --> ")
cardnumber = outarray[3].split('\n')[2].replace(' ','')[10:29]
idnumber = outarray[4].split('\n')[2].replace(' ','')
history = list()

# 循环添加交易记录到history列表
for i in range(5,15):
    history.append(outarray[i].split('\n')[2].replace(' ','')[2:100])
print '----------------------------------------------------------------------------------------'
print '                                   银行闪付卡信息显示                                   '
print '----------------------------------------------------------------------------------------'
if len(idnumber) >= 90:
    print u'姓      名：' + binascii.a2b_hex(idnumber[60:-8]).decode('gbk')
    print u'卡主身份证：' + binascii.a2b_hex(idnumber[12:48]).decode('gbk')
print u'银行卡卡号：' + cardnumber
print u'银行卡类型：' + getCardType(cardnumber)
print '----------------------------------------------------------------------------------------'
print u'编号	交易时间			交易金额		交易地点'
for i in range(len(history)):
    print '----------------------------------------------------------------------------------------'
    print getHistory(history[i],i+1)
# 删除proxmark3的运行日志
os.system("rm proxmark3.log")
# 删除proxmark3的历史记录
os.system("rm .history")

#!/usr/bin/python
# -*- coding: UTF-8 -*-
import subprocess, os, binascii

#解析余额函数
def getBalance(tvlStr):
    if len(tvlStr) == 18:
        balance = int(tvlStr[2:10].upper(),16)/100.0
        return str(balance)
    else:
        return ''

def getEffdata(tvlStr):
    if len(tvlStr) >= 70:
        effdata = tvlStr[42:46] + '-' + tvlStr[46:48] + '-' + tvlStr[48:50] + ' ~ ' + tvlStr[50:54] + '-' + tvlStr[54:56] + '-' + tvlStr[56:58]
        return str(effdata)
    else:
        return ""

os.system('clear')
# 打开proxmark3
pm3 = subprocess.Popen("/home/satan/Program/proxmark3-iceman/client/proxmark3 /dev/ttyACM0", shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
# 选择交通卡（上海）
pm3.stdin.write('hf 14a raw -c -s 0200A40000023F01 -p\n')
# 读取余额
pm3.stdin.write('hf 14a raw -c 03805c000204 -p\n')
# 读取卡片信息
pm3.stdin.write('hf 14a raw -c 0200B0950000 -p\n')
# 关闭卡片
pm3.stdin.write('hf 14a raw -a\n')
out = pm3.communicate()[0]
outarray = out.split("pm3 --> ")
balance = getBalance(outarray[2].split('\n')[2].replace(" ",""))
effdata = getEffdata(outarray[3].split('\n')[2].replace(" ",""))
print '----------------------------------------------------------------------------------------'
print '                                     交通卡信息显示                                     '
print '----------------------------------------------------------------------------------------'
print '卡内余额：' + balance
print '有效日期：' + effdata
print '----------------------------------------------------------------------------------------'
os.system('rm .history')
os.system('rm proxmark3.log')

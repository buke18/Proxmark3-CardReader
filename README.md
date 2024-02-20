# Proxmark3-CardReader
通过该程序读取某些cpu型卡片
# Proxmark3-Reader
<b>固件版本：Proxmark3-iceman</b>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<b>固件地址：</b>https://github.com/iceman1001/proxmark3</br>
这是一个通过Proxmark3设备，对不同具有NFC功能的卡片/证件信息操作的项目。由于涉及银行卡，护照等敏感证件的信息读取，在此声明该项目的任何代码不得用于非法用途。
## PBOC
PBOC目录下的主程序为PBOC_Reader.py，该程序可以读取带有银联标志的所有闪付卡的信息和交易记录，目前可读取借记卡。
## TravelCard
TravelCard目录下的主程序为TravelCard_Reader.py，该程序用于读取交通卡的余额以及交易记录，目前只测试了上海的卡，其他城市如有需要可issue提交。

import pywifi
#from comtypes import GUID
import time

wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]
# 起始获得的是列表，列表中存放的是无线网卡对象。
# 可能一台电脑有多个网卡，请注意选择
# 如果网卡选择错了，程序会卡住，不出结果。
iface.scan()
time.sleep(2) #必须加
result=iface.scan_results()

for i in range(len(result)):
        print(result[i].ssid, result[i].bssid)#ssid 是名称 ，bssid 是信号强度


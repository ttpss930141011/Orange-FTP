# -*- coding: utf-8 -*-
# @Time    : 2022/10/27 14:06
# @Original author  : giampaolo
# @Author    : Justin Xiao
# @File    : __init__.py
# @Package url：https://github.com/giampaolo/pyftpdlib.git
# @LICENSE    : MIT License
# @Description    : 
# 本專案ftp函示庫使用ftplib，但為了符合此專案需求，
# 額外引入了pub/sub包，
# 需要把ftplib裡所有的print改為自己接手處理並在UI的FTP message box做顯示，
# 將所有print改用在687行新增了的sendMessage method做出發佈者，並在controller內使用訂閱者接收FTP訊息。
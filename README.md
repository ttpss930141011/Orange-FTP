# Orange FTP
Easy FTP application

## Features

- Autofill information by you setting, save key-in FTP information time.
- Friendly UI can customize the file list you wanna upload.
- Auto Upload mode can let you set CRON job, and ftp.log will record your file upload status.

## Structure
``` txt
├─ views/                               // view相關
│  ├─ components                        // 組件相關
│  │  ├─ __init__.py                    // 說明
│  │  ├─ topLeftRightFileListWidget.py  // 封裝檔案操作與fileListWidget.py的組件
│  │  ├─ fileListWidget.py              //  author: yjg30737
│  ├─ UI.py                             // 主要UI檔案
├─ lib/                     // 使用到的library
│  ├─ __init__.py           // 說明
│  ├─ ftplib.py             // ftplib library
├─ static/                  // 靜態檔案
│  ├─ add.svg               // add button的svg
│  ├─ delete.svg            // delete button的svg
│  ├─ clear.svg             // clear button的svg
│  ├─ favicon.ico           // program icon
│  ├─ error_login.png       // Demo pic
│  ├─ success_login.png     // Demo pic
│  ├─ upload_success.png    // Demo pic
├─ controller/              // Controller 相關
│  ├─ mainController.py     // 主要controller 檔案
├─ dist/                    // 打包相關
│  ├─ file/                 // 打開OrangeFTP.exe後要上傳的檔案目錄
│  ├─ OrangeFTP.exe         // 打包後程式本體
│  ├─ ftp.log               // auto upload 會產生的log檔
│  ├─ config.txt            // config.txt
├─ file/                    // start.py 執行後要上傳的檔案目錄
├─ .gitignore               
├─ config.txt               // config.txt
├─ start.py                 // 程式進入點
├─ start.spec               // pyinstaller build spec
├─ requirement.txt          // package requirement
```

## Instructions
For sigle .exe in dict:
- Create ```config.txt``` in ```dict/```
```sh 
#config.txt
FTP_IP:xx.xxx.xxx.xx
FTP_Path:/xxx/xxx
FTP_Account:YOUR_ACCONUT
FTP_Password:YOUR_PASSWORD
```
- create ```dict/file``` folder and put your wanna upload file in
- Excute ```OrangeFTP.exe```.

For source code in start.py:
- Create ```config.txt```
```sh 
#config.txt
FTP_IP:xx.xxx.xxx.xx
FTP_Path:/xxx/xxx
FTP_Account:YOUR_ACCONUT
FTP_Password:YOUR_PASSWORD
```
- create ```file``` folder and put your wanna upload file in .
- Excute.
```sh 
python start.py
 ```
## Build
```sh
pyinstaller start.spec
```

## Included packages
- [pyQt5](https://www.riverbankcomputing.com/software/pyqt/) 
PyQt is a set of Python bindings for The Qt Company's Qt application framework and runs on all platforms supported by Qt including Windows, macOS, Linux, iOS and Android. 
- [pyqt-top-left-right-file-list-widget](https://github.com/yjg30737/pyqt-top-left-right-file-list-widget)
Simple PyQt widget which contains QListWidget and add, delete QPushButton to add and delete file in the list
- [pyqt-file-list-widget](https://github.com/yjg30737/pyqt-file-list-widget)
PyQt QListWidget for files (Being able to drop the files based on user-defined extensions)
- [pyftpdlib](https://github.com/giampaolo/pyftpdlib/)
Python FTP server library provides a high-level portable interface to easily write very efficient, scalable and asynchronous FTP servers with Python.

## Demo
Success login in FTP :  
![alt text](static/success_login.png)

Error login :  
![alt text](static/error_login.png)

Upload success :  
![alt text](static/upload_success.png)
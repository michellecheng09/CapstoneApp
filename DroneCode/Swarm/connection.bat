@echo off

REM connect to tello black and make it connect to tello-dev wifi

    netsh wlan connect ssid=TELLO-99263F name=TELLO-99263F  
    timeout /t 10
    packetsender -u -a 192.168.10.1 8889 command
    timeout /t 2
    packetsender -u -a 192.168.10.1 8889 "ap tello-dev t3ll0Q1!"
    timeout /t 1

REM connect to tello green and make it connect to tello-dev wifi

    netsh wlan connect ssid=TELLO-FDC738 name=TELLO-FDC738
    timeout /t 10
    packetsender -u -a 192.168.10.1 8889 command
    timeout /t 2
    packetsender -u -a 192.168.10.1 8889 "ap tello-dev t3ll0Q1!"
    timeout /t 1

REM connect to tello red and make it connect to tello-dev wifi

    netsh wlan connect ssid=TELLO-99217A name=TELLO-99217A
    timeout /t 10
    packetsender -u -a 192.168.10.1 8889 command
    timeout /t 2
    packetsender -u -a 192.168.10.1 8889 "ap tello-dev t3ll0Q1!"
    timeout /t 1

netsh wlan connect ssid=tello-dev name=tello-dev
timeout /t 10

ping 10.105.221.20
ping 10.105.221.21
ping 10.105.221.22
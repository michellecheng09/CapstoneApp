# Low Cost Drone Light Show

This project is focused on the creation of a low cost light show that can be easily accessiable. 
The purpose is to have a method to create various formations with Tello EDU drones and have control using a mobile application. 


## IP Addressing 
This tool requires the set of the FireFly network where the drones are connected on. 
Each is assigned a unique IP on the network and controlled through this IP by the Tello Manager. 
Refer to the section below for the assignment of SN,IP to ID.

```python
self.sn2ip = {
            '0TQZK7NED02VMT': '192.168.0.103',
            '0TQZK7JED02TVJ': '192.168.0.101',
            '0TQZK5DED02KHL': '192.168.0.102',
        }
        self.id2sn = {
            0: '0TQZK7NED02VMT',
            1: '0TQZK7JED02TVJ',
            2: '0TQZK5DED02KHL',
        }
        self.ip2id = {
            '192.168.0.103': 0,
            '192.168.0.101': 1,
            '192.168.0.102': 2,
        }

```
## Devleopment Tools  
Hardware: Tello EDU, TP Link Wireless Router 
Sawarm Programming: Python, PacketSender
Application: React Native, Expo, SubnetInfo, Fetch API, Firebase 

## Contributers and Remarks
This is in fulfillment for the final year Capstone Project in the Faculty of Engineering and Applied Science at Ontario Tech University.

Authors include Michelle Cheng, Rodaba Ebadi, Toluwanimi Elebute, Munazza Fahmeen and Nivetha Gnaneswaran.
Special remarks to our advisor Dr.Lixuan Lu, P.Eng and capstone coordinator Dr. V.K.Sood, P.Eng.





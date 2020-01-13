# rpi-security-camera-server

## WARNING
**NOTE: Please use this software at your own risk. This project is designed to be an example of a home security system and does not have the appropriate security protocols in place. By opening your web server up to the public, you are putting yourself at risk for a hacker to access videos of your home.**

## Introduction
This repository contains code to setup a Raspberry Pi as a home security camera using the on-board camera (sold separately).

## What You Need

* Raspberry Pi (any model)
* Raspberry Pi Add-On Camera
* 5V 2A power supply

## Raspberry Pi Setup
The Raspberry Pi serves several functions
1. Record video from the camera to disk
2. Stream real-time video from the camera to a client
3. Act as a web server to allow old videos to be retrieved and viewed

### 1. Install Raspbian
https://www.raspberrypi.org/documentation/raspbian/

### 2. Setup SSH
To remotely connect to the server, you will need to enable SSH.
https://www.raspberrypi.org/documentation/remote-access/ssh/

### 3. Setup Static IP Address
This step is necessary to prevent the DHCP server from reassigning the Pi a different address each time it is rebooted.
```
sudo nano /etc/dhcpcd.conf
```
Add the following lines to setup a static IP (assuming server is connected to router via wireless). Obviously these parameter will need to be made specific to your network.
```
interface wlan0
static ip_address=192.168.0.200/24
static routers=192.168.0.1
static domain_name_servers=192.168.0.1
```

### 4. (Optional) Setup Port Forwarding
If you want to access your web server outside of your private network, you will need to setup port forwarding on your router. If you only want to use the application on your private network, this step is not necessary. **WARNING: Exposing your computer to the public puts your computer and your data at risk to outside attacks.**

## Software Setup
You'll need to install the following software to get the server up and running

### 1. Update System Packages
```
sudo apt-get update
sudo apt-get dist-upgrade
```

### 2. Install Node.js
Node.js is an open-source, cross-platform JavaScript run-time environment. The server side JavaScript code will handle transactions between the server-side image database and the client.
```
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt-get install -y nodejs
```
You can check if the installation was successful by checking the version numbers of the installed components.
```
node -v
npm -v
```

### 3. Setup Python3
The security camera scripting is performed using Python. While Raspbian should come with Python3, you can double check by entering `python3` in the console.

You'll need to install a few packages to capture video from the Raspberry Pi camera. The first is `PiCamera`, which is a Python library for communicating with the camera.
```
sudo apt-get update
sudo apt-get install python3-camera
```

### 4. Install Git
```
sudo apt-get install git
```

### 5. Clone this Repostiroy
```
git clone https://github.com/dgreenheck/rpi-security-camera-server.git

# PICOPICA

A Raspberry pi zero w camera.

The goal of this project is to create a simple camera with a custom vintage lens attachment for experimental long-term timelapse capture.

This project is work in progress.

<img src="/IMAGES/00.jpg">

## Part List

* Raspberry Pi Zero W
* Waveshare 1.44 ST7735S LCD HAT
* OV5647 Camera module (any raspi-compatible will work)
* INDUSTAR 28mm 2.8f lens
* [3D Printed parts](/STL/)

<img src="/IMAGES/01.jpg">

<img src="/IMAGES/02.jpg">

<img src="/IMAGES/03.jpg">

# Setup

### Setup WaveShare screen

edit `sudo nano /etc/modules`

add the following lines:
```
spi-bcm2835
fbtft_device
```

create new file `sudo nano /etc/modprobe.d/fbtft.conf`

add the following lines:
```
# /etc/modprobe.d/fbtft.conf

options fbtft_device name=fb_ili9163 gpios=reset:27,dc:25,cs:8,led:24 speed=40000000 bgr=1 fps=60 custom=1 height=128 width=128 rotate=90
```

enable spi in `raspi-config`.
check that your settings are correct in the secondary framebuffer:
```
fbset -i -fb /dev/fb1
```

### Install Picamera

`sudo apt-get install python-picamera`

### Install Pygame

using pip

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
python -m pip install --upgrade pip
python -m pip install pygame
```

using apt

edit sources `sudo nano /etc/apt/sources.list` and uncomment `deb-src` line and run `apt-get update`

```
apt-get build-dep python-pygame
apt-get install python-pygame
```

### TODO

* ~~Add live camera preview~~
* Add buttons support
* Add configurable camera capture behaviour
* Add gui for setting camera options
* How to save / retrieve photos?
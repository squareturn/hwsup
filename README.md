#Python Hardware Support
##prerequisites
The rotary switch is an I2C device.  It is accessed via *python-smbus*.  The easiest way to enable spi support is via *raspi-config->Advanced Options->I2C*

`apt-get install python-smbus`

The display is a 128 x 32 x 1 graphic display utilizing the NewHaven Displays xxxxxx SPI device.  The graphic display is accessed via *python-spidev*.  The easiest way to enable spi support is via *raspi-config->Advanced Options->SPI*

`apt-get install python-spidev`

The display's backlight uses the raspberry pi's hardware PWM to control brightness level.  The hardware is accessed via the *WiringPi* (which used the *wiringpi* C language code to access the hardware.  Building it has other dependencies; listed below.  A more thoughtful build process is described at: https://github.com/WiringPi/WiringPi-Python

```
apt-get install python-dev python-setuptools swig
# try building without python-pytest.  I don't think it's needed.
# apt-get install python-pytest
git clone --recursive https://github.com/WiringPi/WiringPi-Python.git
cd WiringPi-Python
git submodule update --init
cd WiringPi
./build
cd -
swig2.0 -python wiringpi.i

# LDFLAGS are needed for some versions or WiringPi-Python
LDFLAGS="-lcrypt -lrt" python setup.py install
```


## optional
###ImageMagick
The graphics used by the demo.py script were created using ImageMagick.  Those images can be created anywhere so, for space or performance reasons, you may not to install it on your raspberry pi.

`apt-get install imagemagick`

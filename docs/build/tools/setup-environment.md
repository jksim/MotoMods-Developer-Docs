---
title: "Developer Tools: Setup Your Development Environment"
source_url: http://developer.motorola.com/build/tools/setup-environment
source_capture: 2016 Squarespace portal
---

# Developer Tools: Setup Your Development Environment

## Preparing For Application Development

Follow these instructions to add Moto Mod specific support to your applications:

### Step 1) Download and Install Android Studio

To develop a Moto Z application that interacts with Moto Mods, you must be familiar with Android Studio 2.0 and it must be installed on your development environment. If you don’t already have it, [download Android Studio 2.0 here](https://developer.android.com/studio/index.html).

***Note:** You’ll also need to make sure that Android Studio has the Android SDK API 23 installed.*

### Step 2) Download the Moto Mods SDK Library

Next, you’ll need to download the Moto Mods SDK Library.

*Before downloading, please read through the [Moto Mods Development Kit Terms & Conditions](../../legal/mdk-terms-and-conditions.md):*

### Step 3) Place the Moto Mods SDK Library For Use In Your App

Once **ModLib-01.00.000.zip** is downloaded and unzipped, place the **modlib-01.00.000.jar** file in your Android Studio project **lib/** folder, and the the **version.xml** in your **res/** folder. By including this library in your Android application project, you will be able to include Moto Mod specific functionality in your app.

Run these commands from a terminal to copy **modlib.jar** and **version.xml** files to the appropriate location:

```
cp modlib-01.00.000.jar $APP_TOP/app/libs
cp res/version.xml $APP_TOP/app/src/main/res/values
```

## Embedded Firmware Development {#embedded-firmware-development}

Currently, **developing firmware for Moto Mods requires a Linux environment**. Commands below are for Ubuntu ([14.04](http://releases.ubuntu.com/14.04/) or [16.04](http://releases.ubuntu.com/16.04/)).

### Build Dependencies {#build-dependencies}

All of the tools needed to build Moto Mods firmware are provided in the Ubuntu package management system. To download these to your system use the following commands from a terminal:

```console
$ sudo apt-get install -y git gperf flex bison libncurses5-dev gcc-arm-none-eabi python-pip
$ sudo pip install pyelftools
```

---

### Debugging and Flashing Tools {#debugging-and-flashing-tools}

The Reference MotoMod provides an FTDI4232 to emulate JTAG for the HSB and SWD for the MuC. This gives access to debug and install software (flash) using just a USB C port cable. Support for this connection requires slightly modified version of OpenOCD. You will need to build this from source. Again packages for building these are available in the Ubuntu package management system.

#### OpenOCD {#openocd}

OpenOCD is used for flashing and debugging. You will need to download and build the OpenOCD code as follows:

```console
$ sudo apt-get install -y libusb-1.0-0-dev libftdi-dev libtool autoconf texinfo
$ git clone https://github.com/jksim/openocd
$ cd openocd
$ git submodule init
$ git submodule update
$ ./bootstrap
$ ./configure --prefix=/usr/local
$ make
$ sudo make install
$ cd -
```

OpenOCD talks to the chip through USB, so you need grant your account access to the FTDI.

```console
$ id -u -n
```

Replace `<user name>` below with the results of the previous command.

```console
$ sudo -s
# echo 'SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", MODE="0666", OWNER="<user name>"'  >> /etc/udev/rules.d/20-ftdi.rules
# udevadm control --reload
# exit
```

The new permissions will take effect the next time you plug in your USB cable.

#### GDB {#gdb}

GDB is required for low-level debugging. The MDK provides some utility functions that make working with the debugger easier. If you wish to use these utilities you have to download and build the debugger with Python scripting enabled as follows:

```console
$ sudo apt-get install -y libexpat1-dev zlib1g-dev guile-2.0-dev python2.7-dev
$ wget http://ftp.gnu.org/gnu/gdb/gdb-7.11.tar.gz
$ tar -zxf gdb-7.11.tar.gz
$ cd gdb-7.11
$ ./configure --prefix=/usr/local --program-prefix=arm-none-eabi- --target=arm-none-eabi --with-python --with-guile
$ make
$ sudo make install
```

## Further information

Additional information about each tool referenced can be found at the originators site:

- [Android Studio](https://developer.android.com/studio/index.html)
- [OpenOCD](http://openocd.org/)
- [GDB](https://sourceware.org/gdb/)
- [libUSB](http://libusb.info/)
- [libftdi](https://www.intra2net.com/en/developer/libftdi/)
- [FTDI4232](http://www.ftdichip.com/Products/ICs/FT4232H.htm)

[< Previous Page
**Overview**](index.md)

[Next Page >
**Build from Source**](build-from-source.md)

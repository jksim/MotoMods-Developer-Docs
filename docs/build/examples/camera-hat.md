---
title: "Examples: Camera with HAT Adapter Board"
source_url: http://developer.motorola.com/build/examples/camera-hat
source_capture: 2016 Squarespace portal
---

# Examples: Camera with HAT Adapter Board

## Overview {#overview}

Raspberry Pi Camera module can be used with MDK through the HAT adapter Board. This example shows how the MDK can be configured to use Pi Camera with Camera Applications on Moto Z.

The Raspberry Pi Camera module interfaces with the Host processor via a 2-lane CSI interface through the Moto High Speed Bridge. The camera sensor is configured and controlled via a MuC I2C interface via the CAMERA_EXT protocol.

## Before you begin... {#before-you-begin}

#### Required Hardware {#required-hardware}

This app and example requires a **Moto Z, Raspberry Pi Camera Module**, and a **HAT Adapter Board**. To get started, you'll need to buy the required hardware.

#### Software and Tools {#software-and-tools}

See the [Build > Tools](../tools/index.md) section to set up your development environment and learn about building from source, flashing firmware, and how to debug & log.

#### Download Example Source Code {#download-example-source-code}

- **Open source firmware code** for the Camera example is located at <https://github.com/jksim/nuttx>. Specifically:
  - Build Target: <https://github.com/jksim/nuttx/tree/master/nuttx/configs/hdk/muc/picamera>
  - Source Directory: <https://github.com/jksim/nuttx/tree/master/nuttx/configs/hdk/muc/src>
- **Camera Application**
  - There is no special application necessary to run the Camera Mod with Moto Z. Once the Moto Mod is attached, just launch the camera application of your choice.
  - You may find the quality of the image is much worse than what you normally see with the Moto Z’s camera. It is due to the post-processing pipe on Moto Z is only performing color conversion for the RAW sensor stream comes out of the Pi module. If your Moto Mod aims for photography, you should consider adding own ISP so you can control the image quality captured on your Moto Mod.

#### Community and Support {#community-and-support}

Ask questions, engage with the developer community, and get support for this example in the [Moto Mods group at element14.com](https://www.element14.com/community/groups/moto-mods) . Also check out our [Support](../../support/index.md) page.

## Electrical Details {#electrical}

#### Pin Connection Table {#pin-connection-table}

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td><strong>Pin # (80 pin BTB)</strong></td>
<td><strong>Mod Processor Connection</strong></td>
<td><strong>HAT Adapter Board</strong></td>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>3P3</td>
<td>Supply to Pi Camera Module</td>
</tr>
<tr>
<td>2</td>
<td>MUC_PC1 (I2C3_SDA)</td>
<td>SDA</td>
</tr>
<tr>
<td>4</td>
<td>MUC_PC0 (I2C3_SCL)</td>
<td>SCL</td>
</tr>
<tr>
<td>32</td>
<td>MUC_PA9</td>
<td>PI GPIO1 (LED_EN)</td>
</tr>
<tr>
<td>33</td>
<td>MUC_PC9</td>
<td>PI GPIO0 (RST_N)</td>
</tr>
<tr>
<td>57</td>
<td>APBE_CDSI1_D0_N</td>
<td>CSI_DN0</td>
</tr>
<tr>
<td>59</td>
<td>APBE_CDSI1_D0_P</td>
<td>CSI_DP0</td>
</tr>
<tr>
<td>63</td>
<td>APBE_CDSI1_D1_N</td>
<td>CSI_DN1</td>
</tr>
<tr>
<td>65</td>
<td>APBE_CDSI1_D1_P</td>
<td>CSI_DP1</td>
</tr>
<tr>
<td>69</td>
<td>APBE_CDSI1_CLK_N</td>
<td>CSI_CN</td>
</tr>
<tr>
<td>71</td>
<td>APBE_CDSI1_CLK_P</td>
<td>CSI_CP</td>
</tr>
</tbody>
</table>
</div></div>

## Hardware Setup {#hardware}

To use HAT Adapter Board with camera, first detach the Reference Moto Mod from the Moto Z. Locate [dip switch A1](../mdk-user-guide/reference-moto-mod.md#overview) on the Reference Moto Mod and turn it ON and [dip switch A2](../mdk-user-guide/reference-moto-mod.md#overview) OFF to enable using MHB; the remaining dip switches should be Off. The Raspberry Pi Camera Module needs to be inserted to the camera connector on the [HAT Adapter Board](../mdk-user-guide/hat-adapter-board.md#hat-compliant-header). The HAT Adapter Board can then be [inserted](../mdk-user-guide/hat-adapter-board.md#mechanical) into the Reference Moto Mod. Finally, reattach the Reference Moto Mod to your Moto Z.

## Firmware Development {#firmware}

This example utilizes the firmware on both the MuC and the Motorola High Speed Bridge (APBE). The firmware on the APBE is designed to be configured by the MuC, so no development is required directly on the APBE. The MuC will use the Mods High Speed Bus (MHB) to control the APBE at runtime.

Tasks required:

- Create a new target
- Create manifest
- Configure the MHB bus
- Implement the camera driver

#### New Build Target {#new-build-target}

Create a new build target using hdk/muc/base_powered target as the base.

```console
$ cd $BUILD_TOP/nuttx/nuttx/configs/hdk/muc
$ cp -r base_powered picamera
```

Switch to using the new build target.

```console
$ cd $BUILD_TOP/nuttx/nuttx
$ make distclean
$ cd $BUILD_TOP/nuttx/nuttx/tools
$ ./configure.sh hdk/muc/picamera
```

#### Create Manifest {#create-manifest}

```console
$ cd $BUILD_TOP/nuttx/apps/greybus-utils/manifests
$ cp hdk-battery.mnfs hdk-camera.mnfs
```

Edit the hdk-camera.mnfs to change the product string and add the CAMERA_EXT protocol.

Replace the line ‘string = MDK’ under [string-descriptor 2] to read ‘string = MDK-CAMERA’. Add the following to the end of the hdk-camera.mnfs file:

```ini
; Camera on CPort 4
[cport-descriptor 4]
bundle = 3
protocol = 0xed

; Camera related Bundle 3
[bundle-descriptor 3]
class = 0x0d
```

#### Configure the Mods High Speed Bus Control Interface {#configure-the-mods-high-speed-bus-control-interface}

To enable the CSI functionality needed for the camera requires the MHB control channel which, in turn requires UART. On the MDK, the MuC’s USART1 port is connected to the APBE. Run `make menuconfig` and make the following updates to configure the MuC for communications with the APBE over UART.

```
System Type --->
  ...
  (10) Maximum number of CPorts
  [*] STM32 GPIO Chip support
  [*] STM32 UART device                                     <-----
  *** Architecture Options ***
  [ ] Enable MPU
  [ ] Prioritized interrupt support
  [*] Dump stack on assertions
  [ ] Big Endian Architecture

System Type --->
  STM32 Peripheral Support
    [ ] TIM15
    [ ] TIM16
    [ ] TIM17
    [ ] LPTIM1
    [ ] LPTIM2
    [*] USART1                                              <-----
    [ ] USART2
    [*] USART3
    [ ] UART4

Device Drivers --->
  Serial Driver Support --->
    USART1 Configuration --->
      (128) Receive buffer size                             <-----
      (128) Transmit buffer size                            <-----
      (115200) BAUD rate
      (8) Character size
      (0) Parity setting
      (0) Uses 2 stop bits
      [*] USART1 RTS flow control                           <-----
      [*] USART1 CTS flow control                           <-----
```

Now that we have the connection up between the two chips, we will layer an MHB Camera on top of the UART. Make the following updates using `menuconfig`. Note there are two versions of Raspberry Pi Camera Module available in the market. This example uses the newer 8 mega pixel module (v2).

```
Device Drivers
  [ ] Backlight driver Support  ----
  [ ] Block-to-Character (BCH) Support  ----
  [ ] Input Device Support  ----
  [ ] LCD Driver Support  ----
  [*] Mods High-Speed Bus (MHB) driver Support  --->        <-----
  [ ] MMC/SD Driver Support  ----
  [ ] Memory Technology Device (MTD) Support  ----
  [ ] FIFO and named pipe drivers  ----

Device Drivers > Mods High-Speed Bus (MHB) driver Support   
  --- Mods High-Speed Bus (MHB) driver Support
  [*]   APBE control device                                 <-----
  [*]   MHB UART Transport                                  <-----
  (115200) MHB UART0 BAUD
  (2048)  MHB UART Rx buffer size
  (2048)  MHB UART Tx buffer size
  [*]     MHB UART CTS/RTS flow control
  [*]     MHB UART Wait for Sync                            <-----
  [ ]     MHB UART Send Sync
  [ ]   MHB DSI Display
  [*]   MHB Camera                                          <-----
  [ ]     SONY IMX220 Camera Sensor
  [ ]     SONY IMX230 Camera Sensor
  [ ]     OV5674 Raspberry Pi module
  [*]     IMX219 Raspberry Pi module (v2)
  (3)     Camera I2C Bus ID                                 <-----
  (5)     Camera I2C txn retry attempts
  (10000) Camera I2C delay between retries
  (100)   Delay (ms) before camera powerdown
  [ ]   MHB I2S Audio
  [ ]   MHB USB Tunneling
```

Once MHB is configured, the next step is to configure greybus camera_ext driver described in the [Explore > Firmware > Camera-Ext](../../explore/firmware/camera-controls.md) section. There are a few config items to be enabled along with camera_ext support.

```
Device Drivers --->
  Greybus support --->
    --- Greybus support
    [ ]   ARM Semihosting GB Taping
    [*]   Control Protocol support
    [ ]   GPIO PHY support
    [ ]   I2C PHY support
    [ ]   SPI PHY support
    [ ]   Battery support
    [ ]   Mods I2S support
    [ ]   Audio support
    [ ]   Mods Audio support
    [*]   Display support
    [ ]   Loopback support
    [ ]   Vibrator support
    [ ]   USB Host PHY support
    [ ]   PWM PHY support
    [ ]   UART PHY support
    [ ]   HID support 
    [ ]   SDIO PHY support
    [ ]   Vendor Raw Support
    [*]   Vendor Specific Protocol
            Select a vendor driver (Motorola)  --->
    [ ]   NSH UART support
    [ ]   Greybus Firmware Flashing
    [ ]   Power transfer support
    [ ]   Sensors-Ext Protocol  ----
    [*]   Mods Protocol  --->
    [ ]   Lights support
    [ ]   MODS support for USB  
    [*]   Camera Extension                                  <-----

Device Drivers --->
  I2C Driver Support
    [*]   Support the I2C transfer() method                 <-----

Library Routines
  [*] Standard Math library                                 <-----
  [*] Enable floating point in printf                       <-----
```

And finally point the build at the manifest created earlier.

```
Application Configuration --->
  Greybus utility --->
    --- Greybus utility
    [*]   Enable Greybus log
            Select Greybus log level (warning, errors and info)  --->
            Greybus log format (append log level)  --->
          Select a predefined Manifest (Custom manifest)  --->
    (hdk-camera) manifest name
```

#### Implement camera driver {#implement-camera-driver}

In this example, we refer to the camera drivers already implemented. These are available at the following link.

For Raspberry Pi Module v2 (8 megapixel):
    [camera_ext_mhb_imx219_pi.c](https://github.com/jksim/nuttx/blob/master/nuttx/drivers/camera/camera_ext_mhb_imx219_pi.c) (Format/Resolution setting, camera_ext protocol support)
    [camera_ext_ctrls_imx219_pi.c](https://github.com/jksim/nuttx/blob/master/nuttx/drivers/camera/camera_ext_ctrls_imx219_pi.c) (Camera Control implementations)

For Raspberry Pi Module v1 (5 megapixel):
    [camera_ext_mhb_ov5647_pi.c](https://github.com/jksim/nuttx/blob/master/nuttx/drivers/camera/camera_ext_mhb_ov5647_pi.c) (Format/Resolution setting, camera_ext protocol support)
    [camera_ext_ctrls_ov5647_pi.c](https://github.com/jksim/nuttx/blob/master/nuttx/drivers/camera/camera_ext_ctrls_ov5647_pi.c) (Camera Control Implementation)

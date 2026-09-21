---
title: "Examples: Display Personality Card"
source_url: http://developer.motorola.com/build/examples/display
source_capture: 2016 Squarespace portal
---

# Examples: Display Personality Card

## Overview {#overview}

Display Personality Card provides an example of a Moto Mod with an external display and shows how to interface with and control a display and backlight attached through the Moto High Speed Bridge.

The display module interface with the Host processor via a 1-lane MIPI interface through the Moto Bridge. Backlight Driver IC is accessible via a MuC I2C interface and exposed through the Lights protocol.

## Before you begin... {#before-you-begin}

#### Required Hardware {#required-hardware}

This app and example requires a **Moto Z**, **Reference Moto Mod**, and a **Display Personality Card**. To get started, you'll need to buy the required hardware.

#### Software and Tools {#software-and-tools}

See the [Build > Tools](../tools/index.md) section to set up your development environment and learn about building from source, flashing firmware, and how to debug & log.

#### Download Example Source Code {#download-example-source-code}

- **Open source application code** for the MDK Display App is available at <https://github.com/jksim/mdkdisplay>.
- **Open source firmware code** for this example is located at <https://github.com/jksim/nuttx> - specifically:
  - Build Target: <https://github.com/jksim/nuttx/tree/master/nuttx/configs/hdk/muc/display>
  - Source Directory: <https://github.com/jksim/nuttx/tree/master/nuttx/configs/hdk/muc/src>

#### Download Schematics & More {#download-schematics-more}

We also provide schematics, layouts, BOMs, and CAD files for this example. See the [Downloads](#downloads) section at the end of this page.

#### 'MDK Display' App {#-mdk-display-app}

MDK Display is a simple app that provides an end-to-end example of a Moto Mod that contains a display. This is accomplished via the Display Personality Card attached to your Reference Moto Mod. This app provides controls to turn on/off the Moto Mod display, and a way to test various sample modes such as rear camera selfie, clock, and presentation modes.

The MDK Display App will only work on Moto Z devices.

- [MDK Display app (rebuilt from source; was on Google Play Store)](../../assets/apks/mdkdisplay.apk)
- [MDK Display app (rebuilt from source; was on Lenovo App Store)](../../assets/apks/mdkdisplay.apk)

For more details, see the [Moto Mods Android Application](#application) section further down this page.

#### Community and Support {#community-and-support}

Ask questions, engage with the developer community, and get support for this example in the [Moto Mods group at element14.com](https://www.element14.com/community/groups/moto-mods). Also check out our [Support](../../support/index.md) page.

## Electrical Details {#electrical}

#### Block Diagram

*(Diagram coming soon...)*

#### Pin Connection Table {#pin-connection-table}

*(Table coming soon...)*

#### Schematic & Layout {#schematic-layout}

See the [Downloads](#downloads) section at the end of this page for the schematic, layout and more.

## Hardware Setup {#hardware}

*(Coming soon...)*

## Firmware Development {#firmware}

The Display Card demonstrates the ability to output video on Moto Mods.

#### Firmware

This example utilizes the firmware on both the MuC and the Motorola High-Speed Bridge (APBE). The firmware on the APBE is designed to be configured by the MuC, so no development is required directly on the APBE. The MuC will use the Mods High-Speed Bus (MHB) to control the APBE at runtime.

Tasks required:

- Create new target
- Create manifest
- Configure MHB bus
- Configure backlight control
- Implement display driver for panel.

##### New Build Target {#new-build-target}

Create a new build target for the Battery Personality Card using hdk/muc/base_unpowered target as the base.

```console
$ cd $BUILD_TOP/nuttx/nuttx/configs/hdk/muc
$ cp -r base_unpowered display
```

Switch to using the new build target.

```console
$ cd $BUILD_TOP/nuttx/nuttx
$ make distclean
$ cd $BUILD_TOP/nuttx/nuttx/tools
$ ./configure.sh hdk/muc/display
```

##### Initialize Low Power Timer Driver {#initialize-low-power-timer-driver}

Since the backlight driver needs PWM to control brightness, we will need to support the STM32_LPTIM interface. The following calls are required to initialize the interface for LPTIM1:

```
g_lptim = tm32_lptim_init(1);  /* 1 for LPTIM1 */
STM32_LPTIM_SETMODE(g_lptim1, STM32_LPTIM_MODE_CONTINUOUS);
STM32_LPTIM_SETCHANNEL(g_lptim1, STM32_LPTIM_CH_CH1, 1);
```

In the hdk-display example, this logic is implemented and the function `stm32_lptim1_on()` in the `nuttx/configs/hdk/muc/src/stm32_lptim1.c` file. `stm32_lptim1_on()` is then called from `stm32_boot.c` in the same directory.

##### Configure the Mods High Speed Bus Control Interface {#configure-the-mods-high-speed-bus-control-interface}

To enable the DSI functionality needed for the display requires the MHB control channel which, in turn requires UART. On the MDK, the MuC’s USART1 port is connected to the high speed bridge. Run `make menuconfig` and make the following updates to get the MuC communicating with the high speed bridge over UART.

```
System Type --->
...
(10) Maximum number of CPorts
[*] STM32 GPIO Chip support
[*] STM32 UART device
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
    [*] USART1
    [ ] USART2
    [*] USART3
    [ ] UART4

Device Drivers --->
Serial Driver Support --->
USART1 Configuration --->
(128) Receive buffer size
(128) Transmit buffer size
(115200) BAUD rate
(8) Character size
(0) Parity setting
(0) Uses 2 stop bits
[*] USART1 RTS flow control
[*] USART1 CTS flow control
```

Now that we have the connection up between the two chips, we will layer an MHB Display on top of the UART. Make the following updates using menuconfig:

```
> Device Drivers
  [ ] Backlight driver Support  ----
  [ ] Block-to-Character (BCH) Support  ----
  [ ] Input Device Support  ----
  [ ] LCD Driver Support  ----
  [*] Mods High-Speed Bus (MHB) driver Support  --->
  [ ] MMC/SD Driver Support  ----
  [ ] Memory Technology Device (MTD) Support  ----
  [ ] FIFO and named pipe drivers  ----

> Device Drivers > Mods High-Speed Bus (MHB) driver Support   
  --- Mods High-Speed Bus (MHB) driver Support
  [*]   APBE control device (NEW)
  [*]   MHB UART Transport (NEW)
  (115200) MHB UART0 BAUD (NEW)
  (2048)  MHB UART Rx buffer size (NEW) 
  (2048)  MHB UART Tx buffer size (NEW)
  [*]     MHB UART CTS/RTS flow control (NEW)
  [*]     MHB UART Wait for Sync
  [ ]     MHB UART Send Sync (NEW) 
  [*]   MHB DSI Display
  [ ]   MHB I2S Audio (NEW)
  [ ]   MHB USB Tunneling (NEW)
```

At point we have the two chips able to communicate, and send messages related to the display. We now have the base on which to configure a Greybus display. Start with enabling the display driver for our panel. The panel driver just contains the DSI configuration information for the specific panel as described in the [Explore > Firmware > Display](../../explore/firmware/display.md) section. In this case the driver is already available. Once we have a display, the just need to enable the greybus interface to allow the Moto Z to communicate with our display.

```
Device Drivers
...
[*] Power management (PM) driver interfaces
[ ] Power Management Support  ---- 
[ ] Sensor Device Support  ----
[*] DISPLAY driver Support  --->
[ ]   Analogix 7750 support
[*]   NT 35355, 360p DSI display panel support
[ ]   TDI 5.46 inch, 1080p DSI display panel support
[ ]   SMD 4.70 inch, 720p DSI display panel support
[ ] Osmocom-bb Sercomm Driver Support  ----
[*] Serial Driver Support  ---> 
...

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
[ ]   Camera Extension
```

At this point everything is configured for a working display. Unfortunately it will be very difficult to see the result of all of this work without a backlight. In this case we have a backlight controller connected to the third I2C bus. As discussed earlier, the controller uses PWM to control brightness. We will next configure the I2C bus and enable the LPTIM1 interface.

```
System Type --->
STM32 Peripheral Support
[ ] DMA2
[ ] DAC1
[ ] DAC2
[ ] I2C1
[ ] I2C2
[*] I2C3
[ ] OTG FS
[*] PWR 
[ ] RNG 
[ ] SDIO
[ ] SPI1
[*] SPI2
…
[ ] TIM6
[ ] TIM7
[ ] TIM8
[ ] TIM15
[ ] TIM16
[ ] TIM17
[*] LPTIM1
[ ] LPTIM2
[*] USART1
[ ] USART2
[*] USART3
[ ] UART4
[ ] UART5

Device Drivers --->
[ ] HDMI External Display
[ ] Enable loop device
Buffering  --->
[ ] RAM Disk Support
[ ] CAN Driver Support  ----
[ ] PWM Driver Support  ----
[*] GPIO Device Support  --->
[*] I2C Driver Support  --->
-*- SPI Driver Support  --->
[ ] I2S Driver Support  ----
[*] RTC Driver Support  --->
-*- Watchdog Timer Support  --->
[ ] Timer Support  ----
[ ] Analog Device(ADC/DAC) Support  ----
[ ] Audio Device Support  ----
[ ] Backlight driver Support  ----
[ ] Block-to-Character (BCH) Support  ----

System Type --->
I2C Configuration --->
[ ] Alternate I2C implementation
[*] Use dynamic timeouts
(500) Timeout Microseconds per Byte (NEW)
(500) Timeout for Start/Stop (Milliseconds)
(0) Timeout seconds
[ ] Frequency with Tlow/Thigh = 16/9

Device Drivers --->
I2C Driver Support --->
--- I2C Driver Support
[ ]   I2C Slave
[*]   Support the I2C transfer() method
[*]   Support the I2C writeread() method
[ ]   Polled I2C (no interrupts)
[ ]   Enable I2C trace debug
[ ]   Support up_i2creset
```

With all of these pieces in place, we now can enable the backlight driver.

```
Device Drivers --->
[ ] Timer Support  ----
[ ] Analog Device(ADC/DAC) Support  ----
[ ] Audio Device Support  ----
[*] Backlight driver Support  --->
[ ] Block-to-Character (BCH) Support  ----
[ ] Input Device Support  ----
[ ] LCD Driver Support  ----
[*] Mods High-Speed Bus (MHB) driver Support  --->
[ ] MMC/SD Driver Support  ----
[ ] Memory Technology Device (MTD) Support 

Device Drivers --->
Backlight driver Support --->
-- Backlight driver Support
[ ]   DCS support
[ ]   Intersil ISL98611 support
[*]   Intersil LM27965 support
(3)     LM27965 I2C bus
(0x36)  LM27965 I2C address



Device Drivers --->
Greybus support --->
--- Greybus support
...
[ ]   Power transfer support
[ ]   Sensors-Ext Protocol  ----
[*]   Mods Protocol  --->
[*]   Lights support
[ ]   MODS support for USB
[ ]   Camera Extension
```

And finally point the build at the manifest we created earlier.

```
Application Configuration --->
Greybus utility --->
--- Greybus utility
[*]   Enable Greybus log
Select Greybus log level (warning, errors and info)  --->
Greybus log format (append log level)  --->
Select a predefined Manifest (Custom manifest)  --->
(hdk-display) manifest name
```

#### Hardware Manifest {#hardware-manifest}

##### Create Manifest {#create-manifest}

```console
$ cd $BUILD_TOP/nuttx/apps/greybus-utils/manifests
$ cp hdk.mnfs hdk-display.mnfs
```

Edit the hdk-display.mnfs to change the product string and add the Display and Lights protocols.

Replace the line ‘`string = MDK`’ under `[string-descriptor 2]` to read ‘`string = MDK-DISPLAY`’. Add the following to the end of the hdk-`display.mnfs` file:

```ini
[cport-descriptor 2]
bundle = 2
protocol = 0xee        ; Display-Ext

[cport-descriptor 3]
bundle = 2
protocol = 0x0f        ; Lights

[bundle-descriptor 2]
class = 0x0c           ; Display (bundle)
```

##### Setting the Manifest {#setting-the-manifest}

Set the configuration options to use the newly created manifest.

```console
$ cd $BUILD_TOP/nuttx/nuttx
$ make menuconfig
```
```
Application Configuration  --->
-*- Greybus utility  --->
Select a predefined Manifest (Custom manifest)       
(hdk-temperature) manifest name
```

## Moto Mods Android Application {#application}

#### Display card sample APK {#display-card-sample-apk}

MDK Display is a simple app that provides an end-to-end example of a Moto Mod that contains a display. This is accomplished via the Display Personality Card attached to your Reference Moto Mod. This app provides controls to turn on/off the Moto Mod display, and a way to test various sample modes such as rear camera selfie, clock, and presentation modes.

#### Install APK {#install-apk}

Download and install the Display card sample app - see [MDK Display app (rebuilt from source; was on Google Play Store)](../../assets/apks/mdkdisplay.apk)

#### Source code {#source-code}

The source code of the MDK Display APK is published at <https://github.com/jksim/mdkdisplay>.

To build the sample APK from source code, please download and install Android Studio from Android Developer Site, then import the [mdkdisplay project](https://github.com/jksim/mdkdisplay) into Android Studio. See [Developer Tools: Setup Your Development Environment](../tools/setup-environment.md) for more info.

#### Reference for ModManager interface & query Mod statues: {#reference-for-modmanager-interface-query-mod-statues-}

See [Hello World! documentation](hello-world.md#reference) for implementation of MotoMods interface creation and query.

#### Reference for ModDisplay interface: {#reference-for-moddisplay-interface-}

```java
/** Set mod device display state */
@Override
public boolean setModDisplayState(boolean state) {
   boolean result = false;
   if (modDisplay != null) {
       try {
           if (state) {
               result = modDisplay.setModDisplayState(ModDisplay.STATE_ON);
           } else {
               result = modDisplay.setModDisplayState(ModDisplay.STATE_OFF);
           }
       } catch (IllegalStateException e) {
           e.printStackTrace();
       }
   }
   return result;
}

/** Get mod device display state */
@Override
public boolean getModDisplayState() {
   boolean result = false;
   if (modDisplay != null) {
       try {
           if (modDisplay.getModDisplayState() == ModDisplay.STATE_ON) {
               result = true;
           }
       } catch (IllegalStateException e) {
           e.printStackTrace();
       }
   }
   return result;
}

/** Toggle Mod Display back light */
ModBacklight backlight = personality.getModManager().getClassManager(
       personality.getModDevice(), ModBacklight.class);
if (backlight != null) {
   backlight.setModBacklightBrightness(
           checked ? Constants.BACKLIGHT_ON : Constants.BACKLIGHT_OFF);
}
```

#### Reference for Presentation view: {#reference-for-presentation-view-}

A presentation is a special kind of dialog whose purpose is to present content on a secondary display. Once MDK Display card attached, the screen on MDK is mount as a extend target display. For future details for Android presentation view, please refer to the [Android SDK (Presentation) documentation](https://developer.android.com/reference/android/app/Presentation.html).

```java
DisplayManager displayManager = (DisplayManager) getSystemService(Context.DISPLAY_SERVICE);
Display[] presentationDisplays = displayManager.getDisplays(DisplayManager.DISPLAY_CATEGORY_PRESENTATION);
if (presentationDisplays.length > 0) {
   /**
    * If there is more than one suitable presentation display, then we could consider
    * giving the user a choice.  For this example, we simply choose the first display
    * which is the one the system recommends as the preferred presentation display.
    */
   Display display = presentationDisplays[0];
   try {
       /** Clean up previously presentation view */
       if (presentation != null) {
           presentation.dismiss();
           presentation = null;
       }
       presentation = new PresentationActivity(this, display, image);
       presentation.show();
   } catch (WindowManager.InvalidDisplayException e) {
       e.printStackTrace();
   }
}
```

#### Verify {#verify}

Attach Display card to phone, then install and launch Display card sample apk, check the Mod / Personality card status and information, then turn on Display switcher UI to test display screen on MDK:

*(Screenshot coming soon...)*

## Downloads {#downloads}

This section contains the downloadable files associated with this example.

Before downloading, please read through the [Moto Mods Development Kit Terms & Conditions](../../legal/mdk-terms-and-conditions.md):

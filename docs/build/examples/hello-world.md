---
title: "Examples: Hello World!"
source_url: http://developer.motorola.com/build/examples/hello-world
source_capture: 2016 Squarespace portal
---

# Examples: Hello World!

## Overview {#overview}

The “Hello World” example (sometimes lovingly referred to as “Blinky”) is an end-to-end example that shows basic Moto Mods functionality (by controlling the LED on the Reference Moto Mod). It includes open source firmware and is driven by the MDK Utility app (see the [MDK Utility Example](mdk-utility.md) page for more details, including Flashing & Developer support).

**The purpose of this example is to:**

- Provide a “Hello World” example (aka “Blinky”)
- Demonstrate end-to-end implementation of Moto Mods functionality
- Provide control to LED located in Reference Moto Mod

## Before you begin... {#before-you-begin}

#### Required Hardware {#required-hardware}

This app and example requires a **Moto Z** and **Reference Moto Mod**. To get started, you'll need to buy the required hardware.

#### Software and Tools {#software-and-tools}

See the [Build > Tools](../tools/index.md) section to set up your development environment and learn about building from source, flashing firmware, and how to debug & log.

#### Download Example Source Code {#download-example-source-code}

- **Open source application code** for the MDK Utility App is available at <https://github.com/jksim/mdkutility>.
- **Open source firmware code** for this example is located at <https://github.com/jksim/nuttx> - specifically:
  - Build Target: <https://github.com/jksim/nuttx/tree/master/nuttx/configs/hdk/muc/blinky>
  - Source Directory: <https://github.com/jksim/nuttx/tree/master/nuttx/configs/hdk/muc/src>

#### ‘MDK Utility’ App {#-mdk-utility-app}

MDK Utility is a simple app that provides an end-to-end ‘Hello World’ example that shows how to control the LED on the Reference Moto Mod.

The MDK Utility App will only work on Moto Z devices.

- [MDK Utility app on Google Play Store](https://play.google.com/store/apps/details?id=com.motomodsdev.mdkutility)
- [MDK Utility app on Lenovo App Store](http://www.lenovomm.com/appdetail/com.motomodsdev.mdkutility/0)

For more details, see the [Moto Mods Android Application](#application) section further down this page.

#### Community and Support {#community-and-support}

Ask questions, engage with the developer community, and get support for this example in the [Moto Mods group at element14.com](https://www.element14.com/community/groups/moto-mods). Also check out our [Support](../../support/index.md) page.

## Firmware Development {#firmware}

#### Firmware

Follow these instructions to setup your firmware development environment and download source code if it has not been done already.
The base source code has a target for blinky. The information below details the steps to create the firmware for blinky, if it did not exist before.

#### New Build Target {#new-build-target}

Create a new build target for blinky using hdk/muc/base_powered target as the base.

```console
$ cd $BUILD_TOP/nuttx/nuttx/configs/hdk/muc
$ mkdir blinky
$ cp base_powered/* blinky/
```

Switch to using the new build target.

```console
$ cd $BUILD_TOP/nuttx/nuttx/tools
$ ./configure.sh hdk/muc/blinky
```

The following features in nuttx are to be enabled to support blinky functionality.

1. Greybus RAW protocol
2. Timer 6

##### menuconfig support {#menuconfig-support}

To integrate into menuconfig and the build system, two files must be updated.

**`nuttx/nuttx/configs/hdk/muc/Kconfig`**

```
config MODS_RAW_BLINKY
    bool "Blinky LED Mods Raw support"
    default n
    depends on GREYBUS_RAW
    select DEVICE_CORE
    select STM32_TIM6
    ---help---
        Enable Blinky LED Raw support
```

**`nuttx/nuttx/configs/hdk/muc/src/Makefile`**

```
ifeq ($(CONFIG_MODS_RAW_BLINKY),y)
CSRCS += stm32_modsraw_blinky.c
endif
```

#### Raw Protocol {#raw-protocol}

##### Files {#files}

- `nuttx/drivers/greybus/raw.c` - Raw protocol

##### Configuration Changes {#configuration-changes}

Set the configuration options to enable Raw Protocol.

```console
$ cd $BUILD_TOP/nuttx/nuttx
$ make menuconfig
```
```
Device Drivers  --->  
[*] Greybus support  --->
[*]   Vendor Raw Support
```

#### Timer6 {#timer6}

Set the configuration options to enable timer6.

```console
$ cd $BUILD_TOP/nuttx/nuttx
$ make menuconfig
```
```
System Type  --->
STM32 Peripheral Support  --->
[*] TIM6
```

#### Blinking LED (Blinky) Device Driver {#blinking-led-blinky-device-driver}

The driver implements blinking LED control with ON/OFF data exchange over raw protocol between Moto Z and the reference mod.

In addition the driver also toggles a control GPIO(to control optional external circuitry) based on the same blinky ON/OFF commands.

##### Files

- `nuttx/configs/hdk/muc/src/stm32_modsraw_blinky.c` - raw protocol device driver for blinking LED control.

##### Blinky Raw Protocol {#blinky-raw-protocol}

**Message format:**
*(Table coming soon...)*

**Message Commands:**
data sent from apk to HDK
0 or ‘0’ for OFF command.
Non-zero value for ON command.

##### Driver Details {#driver-details}

**stm32_modsraw_blinky.c**
This driver is based on `nuttx/nuttx/configs/hdk/muc/src/stm32_modsraw.c`

```c
static struct device_raw_type_ops blinky_type_ops = {
    .recv = blinky_recv,
    .register_callback = blinky_register_callback,
    .unregister_callback = blinky_unregister_callback,
};
static struct device_driver_ops blinky_driver_ops = {
    .probe = blinky_probe,
    .type_ops = &blinky_type_ops,
};
struct device_driver mods_raw_blinky_driver = {
    .type = DEVICE_TYPE_RAW_HW,
    .name = "mods_raw_blinky",
    .desc = "Blinky LED Raw Interface",
    .ops = &blinky_driver_ops,
};
```

Setup the GPIO and initialize the pin in the driver.

```c
In stm32_boot.c
{ GPIO_MODS_LED_DRV_3,     (GPIO_OPENDRAIN)             },
In stm32_modsraw_blinky.c 
static int blinky_probe(struct device *dev)
{
    gpio_direction_out(GPIO_MODS_LED_DRV_3, LED_OFF);
    gpio_direction_out(GPIO_MODS_DEMO_ENABLE, 0);
    return 0;
}
```

Implement raw message handling in `blinky_recv()`.
Turn ON LED blinking with any non-zero value.

```c
static int blinky_recv(struct device *dev, uint32_t len, uint8_t data[])
{
    if (len == 0)
        return -EINVAL;
    if (data[1] == 0 || data[1] == '0')
        blinky_timer_stop();
    else
        blinky_timer_start();
    return 0;
}
```

Initialize and setup timer functionality for the timer handler be triggered every 1000 milliseconds

```c
#define BLINKY_ACTIVITY    10
#define BLINKY_TIM          6
#define BLINKY_TIM_FREQ  1000
#define BLINKY_PERIOD    1000
----
static void blinky_timer_start(void)
{
    gpio_set_value(GPIO_MODS_DEMO_ENABLE, 1);
----
        tim_dev = stm32_tim_init(BLINKY_TIM);
        DEBUGASSERT(tim_dev);
        STM32_TIM_SETPERIOD(tim_dev, BLINKY_PERIOD);
        STM32_TIM_SETCLOCK(tim_dev, BLINKY_TIM_FREQ);
        STM32_TIM_SETMODE(tim_dev, STM32_TIM_MODE_PULSE);
        STM32_TIM_SETISR(tim_dev, blinky_timer_handler, 0);
        STM32_TIM_ENABLEINT(tim_dev, 0);
```

In timer handler function, toggle the GPIO level.

```c
static int blinky_timer_handler(int irq, FAR void *context)
{
----
    new_val = gpio_get_value(GPIO_MODS_LED_DRV_3) ^ 1;
    gpio_set_value(GPIO_MODS_LED_DRV_3, new_val);
---
```

Disable the timer and assert the GPIO to stop the LED blinking

```c
static void blinky_timer_stop(void)
{
        gpio_set_value(GPIO_MODS_DEMO_ENABLE, 0);
----
        STM32_TIM_DISABLEINT(tim_dev, 0);
        stm32_tim_deinit(tim_dev);
        tim_dev = NULL;
        gpio_set_value(GPIO_MODS_LED_DRV_3, LED_OFF);
-----
```

##### Driver and Device Initialization {#driver-and-device-initialization}

MDK has LED connected over GPIO pin PE8
Define the GPIO for LED control at `$BUILD_TOP/nuttx/nuttx/configs/hdk/muc/include/mods.h`

```c
#define GPIO_MODS_LED_DRV_3      CALC_GPIO_NUM('E',  8)
```

Control GPIO to enable/signal any external circuitry
Define the control GPIO at `$BUILD_TOP/nuttx/nuttx/configs/hdk/muc/include/mods.h`

```c
#define GPIO_MODS_DEMO_ENABLE    CALC_GPIO_NUM('G', 10)
```

The device driver is initialized in `$BUILD_TOP/nuttx/nuttx/configs/hdk/muc/src/stm32_boot.c`.
Entry in the `devices[]` array.

```c
#ifdef CONFIG_MODS_RAW_BLINKY
    {
        .type = DEVICE_TYPE_RAW_HW,
        .name = "mods_raw_blinky",
        .desc = "Blinky LED Raw Interface",
        .id   = 0,
    },
#endif
```

Part of the `board_initialize()` function.

```c
#ifdef CONFIG_MODS_RAW_BLINKY
  extern struct device_driver mods_raw_blinky_driver;
  device_register_driver(&mods_raw_blinky_driver);
#endif
```

##### Configuration Changes

Set the configuration options to enable the raw protocol device driver for Blinky.

```console
$ cd $BUILD_TOP/nuttx/nuttx
$ make menuconfig
```
```
Board Selection  --->
Select target board (Motorola HDK MuC)  --->
[*] Blinky LED Mods Raw support
```

#### Hardware Manifest {#hardware-manifest}

##### New Manifest {#new-manifest}

Create hardware manifest for the example using apps/greybus-utils/manifests/hdk-powered.mnfs as the base.

```console
$ cd $BUILD_TOP/nuttx/apps/greybus-utils/manifests
$ cp hdk-powered.mnfs hdk-blinky.mnfs
```

Edit the hdk-blinky.mnfs file to change the interface string and add Raw Interfaces and Bundle.

```ini
[string-descriptor 2]
-string = MDK-POWERED
+string = MDK-BLINKY
```
```ini
; RAW interface on CPort 4
[cport-descriptor 4]
bundle = 3
protocol = 0xfe
; RAW Bundle 3
[bundle-descriptor 3]
class = 0xfe
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
(hdk-termapp) manifest name
```

#### Building and Flashing Firmware {#building-and-flashing-firmware}

The new target supports all required functionality now. The firmware can be built and flashed into the Reference Moto Mod. Make sure that the Moto Mod is running in development mode as per [these instructions](index.md) or build and flash the development bootloader yourself as [documented here](../tools/build-from-source.md).

## Moto Mods Android Application {#application}

#### MDK Utility sample APK {#mdk-utility-sample-apk}

The MDK Utility sample APK is an open source project, works as an downloadable Android app, to show the capability to toggle the MDK LED.

#### Install APK {#install-apk}

Download and install the MDK Utility sample APK - see [MDK Utility app on Google Play Store](https://play.google.com/store/apps/details?id=com.motomodsdev.mdkutility)

#### Source code {#source-code}

The source code of the MDK Utility sample APK is published at <https://github.com/jksim/mdkutility>.

To build the sample APK from source code, please [download and install Android Studio from Android Developer Site](http://developer.android.com/sdk/index.html), then import the [mdkutility project](https://github.com/jksim/mdkutility) into Android Studio. See [Developer Tools: Setup Your Development Environment](../tools/setup-environment.md) for more info.

#### Sequence Diagram {#sequence-diagram}

*(Diagram coming soon…)*

#### Reference {#reference}

##### Reference for ModManager interface: {#reference-for-modmanager-interface-}

```java
Intent service = new Intent(ModManager.ACTION_BIND_MANAGER);
service.setComponent(ModManager.MOD_SERVICE_NAME);
bindService(service, mConnection, Context.BIND_AUTO_CREATE);
private ServiceConnection mConnection = new ServiceConnection() {
   public void onServiceConnected(ComponentName className,
                                  IBinder binder) {
       IModManager mMgrSrvc = IModManager.Stub.asInterface(binder);
       modManager = new ModManager(context, mMgrSrvc);
       onModAttached(true);
   }
   public void onServiceDisconnected(ComponentName className) {
       modDevice = null;
       modManager = null;
       onModAttached(false);
   }
};
```

##### Reference for ModService events: {#reference-for-modservice-events-}

```java
/** Register Mod intents receiver */
modReceiver = new MyBroadcastReceiver();
IntentFilter filter = new IntentFilter(ModManager.ACTION_MOD_ATTACH);
filter.addAction(ModManager.ACTION_MOD_DETACH);
/**
* Request the broadcaster who send these intents must hold permission PERMISSION_MOD_INTERNAL,
* to avoid the intent from fake senders. For future details, refer to:
* https://developer.android.com/reference/android/content/Context.html#registerReceiver
*/
context.registerReceiver(modReceiver, filter, ModManager.PERMISSION_MOD_INTERNAL, null);
```

##### Query Mod status: {#query-mod-status-}

```java
List<ModDevice> l = modManager.getModList(true);
if (l == null || l.size() == 0) {
  Log.d(Constants.TAG, "Mod device invalid”);
  return;
}
for (ModDevice d : l) {
   Log.d(Constants.TAG, "Mod device Info: " + d);
}
```

##### Reference for ModManager RAW protocol: {#reference-for-modmanager-raw-protocol-}

```java
List<ModInterfaceDelegation> devices =
       modManager.getModInterfaceDelegationsByProtocol(modDevice,
               ModProtocol.Protocol.RAW);
if (devices != null && !devices.isEmpty()) {
   // TODO: go through the whole devices list for multi connected devices.
   // Here simply operate the first device for this example.
   ModInterfaceDelegation device = devices.get(0);
   /**
    * Be care to strict follow Android policy, you need visibly asking for
    * grant permission.
    */
   if (context.checkSelfPermission(ModManager.PERMISSION_USE_RAW_PROTOCOL)
           != PackageManager.PERMISSION_GRANTED) {
       onRequestRawPermission();
   } else {
       /** The RAW_PROTOCOL permission already granted, open RAW I/O */
       getRawPfd(device);
       return true;
   }
}
```

##### Execute RAW command: {#execute-raw-command-}

```
public static byte[] RAW_CMD_LED_ON = {0x01};
public static byte[] RAW_CMD_LED_OFF = {0x00};
// Turn ON LED
byte[] cmd = RAW_CMD_LED_ON;
outputStream.write(cmd);
// Turn OFF LED
byte[] cmd = RAW_CMD_LED_OFF;
outputStream.write(cmd);
```

##### Verify {#verify}

**1) Attach MDK to phone, then install and launch MDK Utility sample apk:**
*(Screenshot coming soon...)*

**2) Check the Mod / Personality card status and information, then turn on/off LED switcher UI to enable LED to blink:**
*(Screenshot coming soon...)*

**3) The LED light on board should blink.**

---
title: "Examples: Sensor Personality Card"
source_url: http://developer.motorola.com/build/examples/sensor
source_capture: 2016 Squarespace portal
---

# Examples: Sensor Personality Card

## Overview {#overview}

The Sensor Personality Card provides an example of a Moto Mod with a custom sensor that provides data to a custom Android application running on a Moto Z smartphone. The Moto Mod and application communicate over the [Raw Protocol](../../explore/firmware/raw.md) using custom protocol defined for this Personality Card.

This sensor used in the example card is a thermistor ([NTC Thermistor NCP03XV103E05RL](http://www.murata.com/en-us/about/newsroom/news/product/thermistor/2008/1027b)) that can measure ambient temperature. When the thermistor circuitry is enabled by asserting the Moto Mod Micro Controller (MuC) general purpose input/output pin (GPIO), it outputs voltage that varies depending on the temperature. The voltage output is connected to the MuC ADC channel for taking measurements. The measurements are reported to the Moto Z upon requests.

## Before you begin... {#before-you-begin}

#### Required Hardware {#required-hardware}

This app and example requires a **Moto Z**, **Reference Moto Mod**, and a **Sensor Personality Card**. To get started, you'll need to buy the required hardware.

#### Software and Tools {#software-and-tools}

See the [Build > Tools](../tools/index.md) section to set up your development environment and learn about building from source, flashing firmware, and how to debug & log.

#### Download Example Source Code {#download-example-source-code}

- **Open source application code** for the MDK Sensor App is available at <https://github.com/MotorolaMobilityLLC/mdksensor>.
- **Open source firmware code** for this example is located at <https://github.com/MotorolaMobilityLLC/nuttx> - specifically:
  - Build Target: <https://github.com/MotorolaMobilityLLC/nuttx/tree/master/nuttx/configs/hdk/muc/temperature>
  - Source Directory: <https://github.com/MotorolaMobilityLLC/nuttx/tree/master/nuttx/configs/hdk/muc/src>

#### Download Schematics & More {#download-schematics-more}

We also provide schematics, layouts, BOMs, and CAD files for this example. See the [Downloads](#downloads) section at the end of this page.

#### ‘MDK Sensor’ App {#-mdk-sensor-app}

MDK Sensor is a simple app that provides an end-to-end example demonstrating how to obtain readings from the Sensor Personality card attached to your Reference Moto Mod, which it then displays in the app as graph.

The MDK Sensor App will only work on Moto Z devices.

- [MDK Sensor app on Google Play Store](https://play.google.com/store/apps/details?id=com.motomodsdev.mdksensor)
- [MDK Sensor app on Lenovo App Store](http://www.lenovomm.com/appdetail/com.motomodsdev.mdksensor/0)

For more details, see the [Moto Mods Android Application](#application) section further down this page.

#### Community and Support {#community-and-support}

Ask questions, engage with the developer community, and get support for this example in the [Moto Mods group at element14.com](https://www.element14.com/community/groups/moto-mods). Also check out our [Support](../../support/index.md) page.

## Electrical Details {#electrical}

#### Block Diagram

Sensor card connected to Reference Moto Mod.

(Diagram coming soon...)

#### Pin Connection Table {#pin-connection-table}

(Table coming soon...)

#### Schematic & Layout {#schematic-layout}

See the [Downloads](#downloads) section at the end of this page for the schematic, layout and more.

## Hardware Setup {#hardware}

To use the Sensor Personality Card, first detach the Reference Moto Mod from the Moto Z. Locate [dip switch A1](../mdk-user-guide/reference-moto-mod.md#overview) on the Mod and turn it on and [dip switch A2](../mdk-user-guide/reference-moto-mod.md#overview) off to enable using Sensor from the example card, then insert the card into the Mod following [these instructions](../mdk-user-guide/reference-moto-mod.md#example-personality-cards). The Reference Moto Mod can be attached back to the Moto Z after that.

## Firmware Development {#firmware}

Follow [these instructions](../tools/index.md) to setup your firmware development environment and download source code if it has not been done already.

The Moto Mods base firmware has a target for the Sensor Personality Card. The information below details the steps to create firmware for the Sensor Personality Card as if this support did not exist and needed to be added.

#### New Build Target {#new-build-target}

Create a new build target for the Sensor Personality Card using hdk/muc/base_powered target as the base.

```console
$ cd $BUILD_TOP/nuttx/nuttx/configs/hdk/muc
$ mkdir example-temperature
$ cp base_powered/* example-temperature/
```

Switch to using the new build target.

```console
$ cd $BUILD_TOP/nuttx/nuttx/tools
$ ./configure.sh hdk/muc/example-temperature
```

The new target does not support required functionality yet. To read the analog signal from the card and communicate with Moto Z over the Raw protocol, the following features need to be enabled:

- Raw protocol
- ADC support
- Raw Protocol device driver

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

#### ADC Support {#adc-support}

Set the configuration options to enable ADC support.

```console
$ cd $BUILD_TOP/nuttx/nuttx
$ make menuconfig
```
```
System Type  --->
STM32 Peripheral Support  --->
[*] ADC1
```
```
Device Drivers  --->
[*] Analog Device(ADC/DAC) Support  ---> 
--- Analog Device(ADC/DAC) Support
[*]   Analog-to-Digital Conversion
(8)     ADC buffer size
[ ]     TI ADS1255/ADS1256 support
[ ]     TI PGA112/3/6/7 support
[ ]   Digital-to-Analog Conversion
```

#### Raw Protocol Device Driver {#raw-protocol-device-driver}

The driver implements Temperature Personality Card Raw Protocol for a data exchange between the Moto Z and the Reference Moto Mod with the example card and measure thermistor circuit output voltage.

##### Files

- `nuttx/configs/hdk/muc/src/stm32_modsraw_temperature.c` - raw protocol device driver for the Personality Card

##### Temperature Personality Card Raw Protocol {#temperature-personality-card-raw-protocol}

**Message Format**

*(Table coming soon...)*

**Message Commands Sent to and from the Reference Moto Mod**

```c
#define TEMP_RAW_COMMAND_INVALID       0x00
#define TEMP_RAW_COMMAND_INFO          0x01
#define TEMP_RAW_COMMAND_ON            0x02
#define TEMP_RAW_COMMAND_OFF           0x03
#define TEMP_RAW_COMMAND_DATA          0x04
#define TEMP_RAW_COMMAND_CHALLENGE     0x05
#define TEMP_RAW_COMMAND_CHLGE_RESP    0x06
```

Responses from Reference Moto Mod to apk will have the command ids with high bit mask.

```c
#define TEMP_RAW_COMMAND_RESP_MASK    0x80
```

**INFO Command**
The command is sent to to the Reference Moto Mod to request device info.

*(Table coming soon...)*

Response from the Reference Moto Mod.

*(Table coming soon...)*

```c
/* device attributes */
struct temp_raw_attr {
    uint8_t     version;        /* device driver version */
    uint8_t     reserved;       /* reserved */
    uint16_t    max_interval;   /* max report interval device supports */
    uint8_t     name[64];       /* name of the device */
} __packed;
```

**ON Command**
The command is sent to to the Reference Moto Mod to turn on temperature reporting. Payload has the interval in milliseconds apk expects the temperature data.

*(Table coming soon...)*

**OFF Command**
The command is sent to to the Reference Moto Mod to turn off temperature reporting.

*(Table coming soon...)*

**DATA Command**
The message is sent from the Reference Moto Mod to report temperature measurements.

*(Table coming soon...)*

**CHALLENGE Command**
The message is sent from the Reference Moto Mod.

*(Table coming soon...)*

**CHALLENGE_RESPONSE Command**
The message is sent to the Reference Moto Mod.

*(Table coming soon...)*

##### Driver Details {#driver-details}

This driver is based on nuttx/configs/hdk/muc/src/stm32_modsraw.c driver.

```c
static struct device_raw_type_ops temp_raw_type_ops = {
    .recv = temp_raw_recv,
    .register_callback = temp_raw_register_callback,
    .unregister_callback = temp_raw_unregister_callback,
};

static struct device_driver_ops temperature_driver_ops = {
    .probe = temp_raw_probe,
    .remove = temp_raw_remove,
    .type_ops = &temp_raw_type_ops,
};

struct device_driver mods_raw_temperature_driver = {
    .type = DEVICE_TYPE_RAW_HW,
    .name = "mods_raw_temperature",
    .desc = "Temperature sensor Raw Interface",
    .ops = &temperature_driver_ops,
};
```

The pinmap file at nuttx/arch/arm/src/stm32/chip/stm32l4x6xx_pinmap.h contains the following definition:

```c
#define GPIO_ADC1_IN4         (GPIO_ANALOG|GPIO_ADC|GPIO_PORTC|GPIO_PIN3)
```

Initialize and register ADC1 with channel GPIO_ADC1_IN4.

```
/* Configure the pins as analog inputs for the selected channels */
 for (i = 0; i < ARRAY_SIZE(g_pinlist); i++)
  {
          stm32_configgpio(g_pinlist[i]);
  }
-----
      /* Call stm32_adcinitialize() to get an instance of the ADC interface */
      adc = stm32_adcinitialize(1, g_chanlist, ARRAY_SIZE(g_chanlist));

------
      /* Register the ADC driver at "/dev/adc0" */
      ret = adc_register(TEMP_RAW_ADC_DEVPATH, adc);
```

Implement raw message handling in mods_raw_recv.

```c
static int mods_raw_recv(struct device *dev, uint32_t len, uint8_t data[])
```

Challenge the client after processing INFO command. Use the current time in nanoseconds as data to be encrypted with AES 128-bit ECB with PKCS5 padding .

```c
case TEMP_RAW_COMMAND_INFO:
----
           up_rtc_gettime(&ts);
            time_ns = timespec_to_nsec(&ts);

----
            /* Encrypt padded time_ns */
            AES128_ECB_encrypt(&info->tr_aes.input[2],
                                (const uint8_t *)&info->tr_aes.key[2],
                                &info->tr_aes.encrypted_data[2]);

            /* send the challenge */
            temp_raw_build_send_mesg(dev, TEMP_RAW_COMMAND_CHALLENGE,
                                sizeof(info->tr_aes.encrypted_data),
                                (uint8_t *)&info->tr_aes.encrypted_data[2], 0);
```

Process the challenge response and verify the previously sent data had the expected modification.

```c
case TEMP_RAW_COMMAND_CHLGE_RESP:
----
            /* Decrypt the adjusted time data */
            AES128_ECB_decrypt(&smsg->payload[2],
                                (const uint8_t *)&info->tr_aes.key[2],
                                &info->tr_aes.decrypted_data[2]);

            /*
             * compare the sent data with received adjusted data.
             * allow ON operation upon match
             */
            memcpy(&time_ns, &info->tr_aes.input[2], sizeof(time_ns));
            time_ns += TEMP_RAW_AES_CLIENT_ADDS;
            retval = memcmp(&info->tr_aes.decrypted_data[2],
                            &time_ns, sizeof(time_ns));
            if (!retval) {
                info->client_verified = 1;
                /* Initialize ADC */
                adc_devinit();
            } else {
                info->client_verified = 0;
                dbg("Client verification failed: %d\n", retval);
            }
```

Setup low priority work queue to handle ON command (only if the client was verified).

```c
case TEMP_RAW_COMMAND_ON:
----
             if (info->client_verified == 0)
                break;

----
           gpio_set_value(GPIO_MODS_DEMO_ENABLE, 1);
----
           /* cancel any work and reset ourselves */
            if (!work_available(&data_report_work))
                work_cancel(LPWORK, &data_report_work);

            /* schedule work */
            work_queue(LPWORK, &data_report_work,
                        temp_raw_worker, info, 0);
```

Read adc device for temperature data in the worker function and queue next worker due at interval requested.

```c
/**
 * worker function for the scheduled work queue.
 * open ADC device and trigger a sample reading.
 */
static void temp_raw_worker(void *arg)
{
----
read(adc_fd, &sample, sizeof(sample));

----

    temp_raw_build_send_mesg(info->gDevice, TEMP_RAW_COMMAND_DATA,
                sizeof(sample.am_data), (uint8_t *)&sample.am_data, 0);

-----

    /* cancel any work and reset ourselves */
    if (!work_available(&data_report_work))
        work_cancel(LPWORK, &data_report_work);

    /* schedule work */
    work_queue(LPWORK, &data_report_work,
                temp_raw_worker, info, MSEC2TICK(info->interval));
```

Cancel the work queue on OFF command.

```
case TEMP_RAW_COMMAND_OFF:
---- 
           /* cancel any work and reset ourselves */
            if (!work_available(&data_report_work))
                work_cancel(LPWORK, &data_report_work);

           gpio_set_value(GPIO_MODS_DEMO_ENABLE, 0);
```

##### Configuration Changes

Set the configuration options to enable the raw protocol device driver for the Temperature Personality Card.

```console
$ cd $BUILD_TOP/nuttx/nuttx
$ make menuconfig
```
```
Board Selection  --->
Select target board (Motorola HDK MuC)  --->
[*] Temperature Personality Mods Raw support
```

##### Driver and Device Initialization {#driver-and-device-initialization}

The GPIO to enable thermistor circuitry on the Personality Card is defined in nuttx/configs/hdk/muc/include/mods.h

```c
#define GPIO_MODS_DEMO_ENABLE    CALC_GPIO_NUM('G', 10)
```

The device driver is initialized in nuttx/configs/hdk/muc/src/stm32_boot.c.
Entry in the devices[] array.

```c
#ifdef CONFIG_MODS_RAW_TEMPERATURE
    {
        .type = DEVICE_TYPE_RAW_HW,
        .name = "mods_raw_temperature",
        .desc = "Temperature sensor Raw Interface",
        .id   = 0,
    },
#endif
```

Part of the board_initialize() function.

```c
#ifdef CONFIG_MODS_RAW_TEMPERATURE
  extern struct device_driver mods_raw_temperature_driver;
  device_register_driver(&mods_raw_temperature_driver);
#endif
```

#### Hardware Manifest {#hardware-manifest}

##### New Manifest {#new-manifest}

Create hardware manifest for the example using apps/greybus-utils/manifests/hdk-powered.mnfs as the base.

```console
$ cd $BUILD_TOP/nuttx/apps/greybus-utils/manifests
$ cp hdk-powered.mnfs temperature-example.mnfs
```

Edit the temperature-example.mnfs file to change the interface string and add Raw Interfaces and Bundle.

```ini
[string-descriptor 2]
-string = MDK-POWERED
+string = TEMPERATURE-EXAMPLE
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
(temperature-example) manifest name
```

#### Building and Flashing Firmware {#building-and-flashing-firmware}

The new target supports all required functionality now. The firmware can be built and flashed into the Reference Moto Mod. Make sure that the Moto Mod is running in development mode as per [these instructions](index.md) or build and flash the development bootloader yourself as [documented here](../tools/build-from-source.md).

## Moto Mods Android Application {#application}

#### Temperature card sample APK {#temperature-card-sample-apk}

The Moto Temperature card sample APK is an open source project, works as an downloadable Android app, to show the capability of Temperature sensor personality card.

#### Install APK {#install-apk}

Download and install the Temperature card sample app - see MDK Sensor app on Google Play Store

#### Source code {#source-code}

The source code of the MDK Sensor APK is published at <https://github.com/MotorolaMobilityLLC/mdksensor>.

To build the sample APK from source code, please [download and install Android Studio from Android Developer Site](http://developer.android.com/sdk/index.html), then import the [mdksensor project](https://github.com/MotorolaMobilityLLC/mdksensor) into Android Studio. See [Developer Tools: Setup Your Development Environment for more info](../tools/setup-environment.md).

#### Sequence Diagram {#sequence-diagram}

*(Diagram coming soon...)*

##### Reference for ModManager Interface: {#reference-for-modmanager-interface-}

Refer to the [Hello, World example](hello-world.md#application) for details on common Moto Mod Management. That source code is reused throughout the Examples.

#### Write RAW command for Sensor Card: {#write-raw-command-for-sensor-card-}

```java
/**
* Command  is [cmd ID(1 byte)] [size of payload(1 byte)] [payload]
*/
public static final int TEMP_RAW_COMMAND_RESP_MASK = 0x80;
public static final int TEMP_RAW_COMMAND_INVALID = 0x00;
public static final int TEMP_RAW_COMMAND_INFO = 0x01;
public static final int TEMP_RAW_COMMAND_ON = 0x02;
public static final int TEMP_RAW_COMMAND_OFF = 0x03;
public static final int TEMP_RAW_COMMAND_DATA = 0x04;
public static final int TEMP_RAW_COMMAND_CHALLENGE = 0x05;
public static final int TEMP_RAW_COMMAND_CHLGE_RESP = 0x06;

/** Challenge code for MDK Temperature Sensor protocol */
public static final int CHALLENGE_ADDATION = 777;

/**  Samples for RAW command format */
public static final int SENSOR_COMMAND_SIZE = 0x02;
public static byte[] RAW_CMD_INFO = {TEMP_RAW_COMMAND_INFO, 0x00};
public static byte[] RAW_CMD_CHALLENGE = {TEMP_RAW_COMMAND_CHALLENGE,
       0x00, /* should use actually size of encrypted AES */
       0x00, /* should be payload of encrypted AES */};
public static byte[] RAW_CMD_START = {TEMP_RAW_COMMAND_ON, SENSOR_COMMAND_SIZE,
       0x00, /* interval(low) */
       0x20, /* interval(high) */};
public static byte[] RAW_CMD_STOP = {TEMP_RAW_COMMAND_OFF, 0x00}; /* stop cmd not need payload */


int interval = Integer.valueOf(values[spinner.getSelectedItemPosition()]);
byte intervalLow = (byte) (interval & 0x00FF);
byte intervalHigh = (byte) (interval >> 8);
byte[] cmd = { Constants.SENSOR_COMMAND_ON, 
       Constants.SENSOR_COMMAND_SIZE,
       intervalLow, 
       intervalHigh };
outputStream.write(cmd);
```

#### Read RAW data from Sensor Card: {#read-raw-data-from-sensor-card-}

```java
/** Read the RAW I/O input pipe, the data is written by attached mod device */
byte[] buffer = new byte[MAX_BYTES];
FileDescriptor fd = parcelFD.getFileDescriptor();
FileInputStream inputStream = new FileInputStream(fd);
int ret = 0;
synchronized (syncPipes) {
   while (ret >= 0) {
       try {
           /** Poll on the exit pipe and the raw channel */
           int polltype = blockRead();
           if (polltype == POLL_TYPE_READ_DATA) {
               ret = inputStream.read(buffer, 0, MAX_BYTES);
               if (ret > 0) {
                   /**  Got raw data */
                   onRawData(buffer, ret);
               }
           } else if (polltype == POLL_TYPE_EXIT) {
               break;
           }
       } catch (IOException e) {
           Log.e(Constants.TAG, "IOException while reading from raw file" + e);
           onIOException();
       } catch (Exception e) {
           Log.e(Constants.TAG, "Exception while reading from raw file" + e);
           e.printStackTrace();
       }
   }
```

#### Parse RAW data: {#parse-raw-data-}

```java
/**
* Response is [cmd ID(1 byte)] [size of payload(1 byte)] [payload]
*/
public static final int CMD_OFFSET = 0;
public static final int CMD_LENGTH = 1;
public static final int SIZE_OFFSET = CMD_OFFSET + CMD_LENGTH;
public static final int SIZE_LENGTH = 1;
public static final int PAYLOAD_OFFSET = SIZE_OFFSET + SIZE_LENGTH;

public static int CMD_INFO_VERSION_OFFSET = 0;
public static int CMD_INFO_VERSION_SIZE = 1;
public static int CMD_INFO_RESERVED_OFFSET = CMD_INFO_VERSION_OFFSET + CMD_INFO_VERSION_SIZE;
public static int CMD_INFO_RESERVED_SIZE = 1;
public static int CMD_INFO_LATENCYLOW_OFFSET = CMD_INFO_RESERVED_OFFSET + CMD_INFO_RESERVED_SIZE;
public static int CMD_INFO_LATENCYLOW_SIZE = 1;
public static int CMD_INFO_LATENCYHIGH_OFFSET = CMD_INFO_LATENCYLOW_OFFSET + CMD_INFO_LATENCYLOW_SIZE;
public static int CMD_INFO_LATENCYHIGH_SIZE = 1;
public static int CMD_INFO_NAME_OFFSET = CMD_INFO_LATENCYHIGH_OFFSET + CMD_INFO_LATENCYHIGH_SIZE;
public static int CMD_INFO_HEAD_SIZE = CMD_INFO_VERSION_SIZE + CMD_INFO_RESERVED_SIZE
       + CMD_INFO_LATENCYLOW_SIZE + CMD_INFO_LATENCYHIGH_SIZE;

public static int CMD_DATA_LOWDATA_OFFSET = 0;
public static int CMD_DATA_LOWDATA_SIZE = 1;
public static int CMD_DATA_HIGHDATA_OFFSET = CMD_DATA_LOWDATA_OFFSET + CMD_DATA_LOWDATA_SIZE;
public static int CMD_DATA_HIGHDATA_SIZE = 1;
public static int CMD_DATA_RESERVED_SIZE = 2;
public static int CMD_DATA_SIZE = CMD_DATA_LOWDATA_SIZE + CMD_DATA_HIGHDATA_SIZE + CMD_DATA_RESERVED_SIZE;

public static  int CMD_CHALLENGE_SIZE = 16;

public static int CMD_CHLGE_RESP_OFFSET = 0;
public static int CMD_CHLGE_RESP_SIZE = 4;


/** Read the RAW I/O input pipe, the data is written by attached mod device */
private int blockRead() {
   /** Poll on the pipe to see whether signal to exit, or any data on raw fd to read */
   StructPollfd[] pollfds = new StructPollfd[2];

   /** readRawFd will watch whether data is available on the raw channel */
   StructPollfd readRawFd = new StructPollfd();
   pollfds[0] = readRawFd;
   readRawFd.fd = parcelFD.getFileDescriptor();
   readRawFd.events = (short) (OsConstants.POLLIN | OsConstants.POLLHUP);

   /** syncFd will watch whether any exit signal */
   StructPollfd syncFd = new StructPollfd();
   pollfds[1] = syncFd;
   syncFd.fd = syncPipes[0];
   syncFd.events = (short) OsConstants.POLLIN;

   try {
       /** Waits for file descriptors pollfds to become ready to perform I/O */
       int ret = Os.poll(pollfds, -1);
       if (ret > 0) {
           if (syncFd.revents == OsConstants.POLLIN) {
               /** POLLIN on the syncFd as signal to exit */
               byte[] buffer = new byte[1];
               new FileInputStream(syncPipes[0]).read(buffer, 0, 1);
               return POLL_TYPE_EXIT;
           } else if ((readRawFd.revents & OsConstants.POLLHUP) != 0) {
               /** RAW driver existing */
               return POLL_TYPE_EXIT;
           } else if ((readRawFd.revents & OsConstants.POLLIN) != 0) {
               /** Finally data ready to read */
               return POLL_TYPE_READ_DATA;
           } else {
               /** Unexcpected error */
               Log.e(Constants.TAG, "unexpected events in blockRead rawEvents:"
                       + readRawFd.revents + " syncEvents:" + syncFd.revents);
               return POLL_TYPE_EXIT;
           }
       } else {
           /** Error */
           Log.e(Constants.TAG, "Error in blockRead: " + ret);
       }
   } catch (ErrnoException e) {
       Log.e(Constants.TAG, "ErrnoException in blockRead: " + e);
       e.printStackTrace();
   } catch (IOException e) {
       Log.e(Constants.TAG, "IOException in blockRead: " + e);
       e.printStackTrace();
   }
   return POLL_TYPE_EXIT;
}

/** Parse raw data to header and payload */
int cmd = buffer[Constants.CMD_OFFSET] & ~Constants.TEMP_RAW_COMMAND_RESP_MASK & 0xFF;
int payloadLength = buffer[Constants.SIZE_OFFSET];

/** Checking the size of buffer we got to ensure sufficient bytes */
if (payloadLength + Constants.CMD_LENGTH + Constants.SIZE_LENGTH != length) {
   return;
}

/** Parser payload data */
byte[] payload = new byte[payloadLength];
System.arraycopy(buffer, Constants.PAYLOAD_OFFSET, payload, 0, payloadLength);
parseResponse(cmd, payloadLength, payload);
```

#### Verify {#verify}

Attach Temperature card to phone, then install and launch Temperature card sample apk, check the Mod / Personality card status and information, then turn on Temperature switcher UI to read Temperature card data

*(Screenshot coming soon...)*

If Temperature card is ready, the sampling value read from HDK Temperature card for every interval will show up.

## Downloads {#downloads}

This section contains the downloadable files associated with this example.

Before downloading, please read through the [Moto Mods Development Kit Terms & Conditions](https://web.archive.org/web/2017/http://developer.motorola.com/assets/html/moto-mods-dev-kit-terms-and-conditions.html):

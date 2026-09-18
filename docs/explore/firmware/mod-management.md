---
title: "Moto Mods Firmware: Mod Management"
source_url: http://developer.motorola.com/explore/firmware/mod-management
source_capture: 2016 Squarespace portal
---

# Moto Mods Firmware: Mod Management

## Overview {#overview}

In order to enable Moto Mods functionality, the Moto Mod must identify itself, enumerate the functionality being provided to the system and configure the communication path to Moto Z device. Identity of the Moto Mod is conveyed through the device’s VID and PID where the VID is the Vendor ID assigned by Motorola and a PID which is managed by the Moto Mod manufacturer. The enumeration of functionality is communicated by the Moto Mod in the form of a Hardware Manifest.

### VID/PID {#vid-pid}

The Moto Mod must identify itself to the system to ensure certification compliance and receive proper infrastructure support such as over the air firmware updates. This identification is in the form of a Vendor ID and Product ID. The Vendor ID is assigned by Motorola through the [certification process](../../partner/certification-program.md) and the Product ID is managed by the Mod manufacturer. During prototyping and development a special VID of 0x42 is used. You can switch to the development VID simply using the [MDK Utility](../../build/tools/flashing-firmware.md#mdkutility).

The setting of the VID and PID are as follows though `make menuconfig` and navigate to:

```
System Type  --->
  -*- Board ID Supported
  [*] Support Unique Board ID
  [*] Pre-defined Board ID
        Board VID
        Board PID
```

### Hardware Manifest {#hardware-manifest}

One of the first things a Moto Mod needs to do is tell the Moto Z what functionality it supports. To do this, it sends a Hardware Manifest. The manifest file contains a list of all of the protocols that are supported as well as the endpoint address of each protocol. The term for this endpoint is 'CPort.' As part of the certification process, you will submit the final source file (in .mnfs format) for each unique Vendor ID, Product ID combination for signing. You will get back a file that will replace the .inc file generated during the compile process. This signed version will be needed for shipping a certified Moto Mod, but is not required for development.

Every Moto Mod contains at least two CPorts. The first 'Control' is always given CPort 0 in the manifest. The second, 'Mods Control' doesn't show up in the manifest at all. These protocols handle the initial setup of communications as well as sending the previously mentioned manifest. Except in specific instances, developers should not have to worry about these protocols.

Example Hardware Manifest Header:

```ini
[manifest-header]
version-major = 0
version-minor = 1

; Interface vendor string (id can't be 0)
[string-descriptor 1]
string = Motorola Mobility, LLC

; Interface product string (id can't be 0)
[string-descriptor 2]
string = Example Moto Mod

; Control protocol on CPort 0
[cport-descriptor 0]
bundle = 0
protocol = 0x00

; Control protocol Bundle 0
[bundle-descriptor 0]
class = 0x0
```

There are common elements that precede the enumeration of your Mod specific implementation, shown in the example hardware manifest header above. This is comprised of versioning, product description, and the required control CPort configuration. The bundle assignment allows protocols to be grouped together. Failure to enumerate any Protocol within a Bundle will result none of those being available. Protocols defined outside of the failed Bundle will be available.. Each Bundle is assigned a class, the value of the the bundle class does not change the behavior of the bundle, but is typically given the protocol number of the most significant protocol in the bundle. All of the protocols are 8 bit unsigned numbers (from 0 to 255). Control is the first protocol and gets the number 0.

The next section of the hardware manifest is where new Mod specific functionality is added. For example, if one were to add a HID device (protocol id = 0x05) the rest of the file would look like:

```ini
;  HID on CPort 1
[cport-descriptor 1]
bundle = 1
protocol = 0x05

[bundle-descriptor 1]
class = 0x05
```

The manifest file is saved with the extension mnfs; under `apps/greybus-utils/manifests`. During the build it will be compiled into a binary format using the 'manifesto’ tool. When the Moto Mod powers up, it uses the contents of the manifest to initialize the communication channels needed to communicate with the Moto Z.

### IPC Configuration: {#ipc-configuration-}

The Moto Mods IPC uses a set of fixed size frames for communication. The packet size and bus rate are configurable based on the Moto Mod’s specific bandwidth and latency requirements. After attach the Moto Mod tells the Moto Z what speed it can support and what size frames it uses. By default, a 15 MHz speed and 32 byte frames are used. The speed gives a maximum limit from which the Moto Z can select. The actual speed will be less than or equal to this value. Frame sizes define how much content is send during any transmission. Small frame sizes require less memory on the Moto Mod size as well as reducing the latency of sending any one message. Frame sizes must be a power of two and less than or equal to 64KB. Frames of this size maximize the throughput of the system but require significant memory resources. Most messages are small and small frame sizes are more common. Note, frames are combined into larger messages by the system. Using a smaller frame size doesn't limit the size of the messages that can be sent, just determines how many transmissions will be needed to send them.

Bus Speed and Frame size (named “Packet Size” in the code) are the configuration options `Mods Maximum Bus Speed` (`GREYBUS_MODS_MAX_BUS_SPEED`), and `Mods Desired Packet Size` (`GREYBUS_MODS_DESIRED_PKT_SIZE`) respectively.

To change the frame size use make menuconfig and navigate to:

```
Device Drivers  --->
  [*] Greybus support  ---> 
  [*] Mods Protocol  --->
        Mods Maximum Bus Speed
        Mods Desired Packet Size
```

[< Previous Page
**Overview**](index.md)

[Next Page >
**Raw Protocol**](raw.md)

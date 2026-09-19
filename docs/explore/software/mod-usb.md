---
title: "Moto Z Software: Mod USB"
source_url: http://developer.motorola.com/explore/software/mod-usb
source_capture: 2016 Squarespace portal
---

# Moto Z Software: Mod USB

## Introduction {#introduction}

USB 2.0 and USB 3.1 are available to the Moto Mod. On attach, the USB-ext protocol is enumerated and can be discovered by the `ModManager.hasDeclaredProtocol()`. Your firmware must notify the Moto Z when the actual USB device(s) is present on a Moto Mod, as described in the [USB-Ext](../firmware/usb-ext.md) firmware page. After doing so, the USB device(s) present on a Moto Mod will appear to Android as standard USB devices or host. The Moto Mod platform does not expose additional USB related API to access USB devices.

An application will use the Android UsbManager to access and communicate with USB devices. The Moto Mod platform supports USB Devices, with the Moto Z acting as the USB host, over USB 2.0 and USB 3.1; a Moto Mod can also play the role of USB host, treating the Moto Z as an [Android Open Accessory](https://source.android.com/devices/accessories/protocol.html). USB 3.1 is only available over the enterprise port, and only if the interface is not used for the Motorola High-Speed Bridge or raw I2S.

A developer interested in Moto Mod USB should have knowledge of the API defined in the [android.hardware.usb](http://developer.android.com/reference/android/hardware/usb/package-summary.html) package.

*(Not preserved: `modusb-diagram-01.png` was not captured by the Wayback Machine and no copy survives.)*

## USB Moto Mod

The information below applies to the developer of a USB Moto Mod or applications which need to communicate to a Moto Mod over USB.

### Moto Mod PID/VID and USB PID/VID {#moto-mod-pid-vid-and-usb-pid-vid}

A `UsbDevice` is identified by its USB Vendor ID and a USB Product ID; similar to the way a `ModDevice` is identified by its Moto Mod Vendor ID and Moto Mod Product ID. There are no guarantees that your Moto Mod VID (assigned by Moto) will be the same as the USB VID (assigned by the USB-IF) of your USB device.

When working with USB hardware on a Moto Mod, it is important to understand that the VID/PID used by the `ModDevice` API refers to the Moto Mod itself and will be different from the USB VID/PIDs of the USB devices on your Moto Mod. In particular `ModDevice.getProductID()` will return the product ID of the Moto Mod; while `UsbDevice.getProductID()` will return the USB product ID of a single discreet USB device on the Moto Mod.

### Determining if a Moto Mod supports USB {#determining-if-a-moto-mod-supports-usb}

If a Moto Mod enable support for USB-Ext, the USB device on the Moto Mod will be made available immediately when the Moto Mod is attached . Your application can query the ModManager service, via the `hasDeclaredProtocol()` function, to determine whether a ModDevice supports the `USB-Ext` protocol.

```java
if (device.hasDeclaredProtocol(ModProtocol.Protocol.USB) {
    // This Mod declares USB in its manifest
  }
```

While a Moto Mod might declare USB device support in its manifest, and while most Moto mods will enumerate their USB devices immediately, this behavior depends on the Moto Mod architecture and design.

### Moto Mod USB Conflicts {#moto-mod-usb-conflicts}

As the Moto Z includes both a USB-C port, and support for USB over the Moto Mod interface, there are a few conflicts a developer should keep in mind when designing a USB capable Moto Mod.

#### The on device USB-C always takes precedence over a Moto Mod USB {#the-on-device-usb-c-always-takes-precedence-over-a-moto-mod-usb}

When a cable or host adapter is plugged into the USB-C port of the phone while USB is connected/enumerated to the Moto Mod, enumeration will be lost to the Moto Mod. Enumeration to the Mod will be lost regardless of the speed (“High-speed” or ”Super Speed”) supported by the data cable connected to the USB-C port of the phone.

#### The Moto Mod USB-2.0 Interface only supports host mode {#the-moto-mod-usb-2-0-interface-only-supports-host-mode}

The USB2 only supports host-mode.

#### The Moto Mod USB-3.1 Interface operates only at Superspeed. {#the-moto-mod-usb-3-1-interface-operates-only-at-superspeed-}

Upstream(host) or downstream (peripherals) connected to this interface should operate at Superspeed (Gen 1). The Moto Mod USB3.1 interface is not backwards compatible with devices that operate at only USB2.0 speeds.

#### The Motorola High-Speed Bridge, raw I2S and USB-3.1 are mutually exclusive {#the-motorola-high-speed-bridge-raw-i2s-and-usb-3-1-are-mutually-exclusive}

These interfaces cannot be active simultaneously over the Moto Mod interface.

### Handling conflicts with Android {#handling-conflicts-with-android}

If USB-Ext is connected over the moto mod interface, and a new host is attached on the device USB-C port, the host on the moto mod will immediately cede control to the USB-C port host. An **`ACTION_USB_ACCESSORY_DETACHED`** intent will be broadcast by the USBManager to signal the Moto Mod host has detached, while an **`ACTION_USB_ACCESSORY_ATTACHED`** intent will be broadcast to indicate a new host has attached

If a host is connected over the USB-C interface, and a new USB-Ext is attached on the moto mod interface, USB-Ext will not assert itself until the USB-C host is disconnected. When the USB-C host disconnects, a dormant Moto Mod host will connect and the USBManager service should broadcast an **`ACTION_USB_ACCESSORY_ATTACHED`** message as a result.

### Android USB Manager {#android-usb-manager}

As mentioned above, there are no new USB related APIs introduced by the Moto Mod SDK. USB devices are accessible over the Moto Mod interface using Android’s standard USB APIs. We provide a short primer on Android USB management, but the reader should refer to the Android `USBManager`, `USBDevice` and Android Open Accessory protocol API provided by the Android SDK for further details.

### Detecting and communicating with a USB device {#detecting-and-communicating-with-a-usb-device}

#### Intent Filter {#intent-filter}

In addition to the permission required by the moto mod SDK, an application which needs to communicate with a USB device and be notified of USB device attach and detach can specify an `<intent filter>` for the `android.hardware.usb.action.USB_DEVICE_ATTACHED`, the `<meta-data>` for this intent filter should also content information about the `<usb-device>` your application wants to filter on in its res/xml/device_filter.xml, as described in the Android USB manager API.

Your application’s Android manifest should declare the following intent filter:

```java
<intent-filter>
      <action android:name="android.hardware.usb.action.USB_DEVICE_ATTACHED" />
  </intent-filter>

  <meta-data android:name="android.hardware.usb.action.USB_DEVICE_ATTACHED"
        android:resource="@xml/device_filter" />
  </activity>
```

And the res/device_filter.xml file should contain the criteria you want to filter by

```xml
<resources>
    <usb-device vendor-id="296" product-id="5461"/>
</resources>
```

#### USB Permissions {#usb-permissions}

To communicate with a USB device, your application must have permission from your users. If your application does not use an intent filter to discover USB devices as connection, it must check for permission to access a USB device before trying to access it, and it must call the `USBManager requestPermission()` API to specifically request permission to communicate with this USB device. These permissions, when granted to an application, allow it to communicate only to the corresponding Moto Mod USB device over USB APIs.

```
mUsbManager.requestPermission(device, mPermissionIntent);
```

#### Communicating with a USB Device {#communicating-with-a-usb-device}

To communicate with a USB device, you need to set up a [`UsbInterface`](http://developer.android.com/reference/android/hardware/usb/UsbInterface.html) and [`UsbEndpoint`](http://developer.android.com/reference/android/hardware/usb/UsbEndpoint.html) for the device. Once the `UsbEndpoint` is setup, your application can make requests to the device using a [`UsbDeviceConnection`](http://developer.android.com/reference/android/hardware/usb/UsbDeviceConnection.html) on the Endpoint. The `bulkTransfer()` and `controlTransfer()` API let an application send data via the USBDevice Endpoint. Data can be sent to a USB Device on the Moto Mod, either synchronously or asynchronously, using the `requestWait()` API.

#### Terminating communication with a device {#terminating-communication-with-a-device}

When you are done communicating with a device or if receive notification that the device has detached, close the [`UsbInterface`](http://developer.android.com/reference/android/hardware/usb/UsbInterface.html) and [`UsbDeviceConnection`](http://developer.android.com/reference/android/hardware/usb/UsbDeviceConnection.html) by calling [`releaseInterface()`](http://developer.android.com/reference/android/hardware/usb/UsbDeviceConnection.html#releaseInterface(android.hardware.usb.UsbInterface)(android.hardware.usb.UsbInterface)) and [`close()`](http://developer.android.com/reference/android/hardware/usb/UsbDeviceConnection.html#close()()). Your application should listen to the `ACTION_USB_DEVICE_DETACHED` intent for this reason: to determine when a USB device is detached and make sure the interfaces are properly released and closed at that time.

[< Previous Page
**Mod HID**](mod-hid.md)

## Related references

- [Moto Mods SDK for Android API Reference](https://jksim.github.io/motomods_sdk/com/motorola/mod/package-summary.html)
- [Moto Mods SDK for Android API Reference](https://jksim.github.io/motomods_sdk)
- [Index](https://jksim.github.io/motomods_sdk/index.html)
- [ModListener](https://jksim.github.io/motomods_sdk/index.html?com/motorola/mod/ModListener.html)
- [ModBacklight](https://jksim.github.io/motomods_sdk/index.html?com/motorola/mod/ModBacklight.html)
- [ModBattery](https://jksim.github.io/motomods_sdk/index.html?com/motorola/mod/ModBattery.html)
- [ModConnection](https://jksim.github.io/motomods_sdk/index.html?com/motorola/mod/ModConnection.html)
- [ModContract](https://jksim.github.io/motomods_sdk/index.html?com/motorola/mod/ModContract.html)
- [ModDevice](https://jksim.github.io/motomods_sdk/index.html?com/motorola/mod/ModDevice.html)
- [ModDisplay](https://jksim.github.io/motomods_sdk/index.html?com/motorola/mod/ModDisplay.html)
- [ModInterfaceDelegation](https://jksim.github.io/motomods_sdk/index.html?com/motorola/mod/ModInterfaceDelegation.html)
- [ModManager](https://jksim.github.io/motomods_sdk/index.html?com/motorola/mod/ModManager.html)
- [ModProtocol](https://jksim.github.io/motomods_sdk/index.html?com/motorola/mod/ModProtocol.html)

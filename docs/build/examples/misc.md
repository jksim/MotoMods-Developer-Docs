---
title: "Examples: Miscellaneous"
source_url: http://developer.motorola.com/build/examples/misc
source_capture: 2016 Squarespace portal
---

# Examples: Miscellaneous

## Overview {#overview}

Besides the various Personality Cards, Moto has also produced several examples to help get you started.

### raw_stub {#raw_stub}

The raw_stub example provides a starting point for firmware and applications using the Raw interface. All threads and pipes are configured, reducing development effort to filling out stubs for sending and receiving your data. This is used in conjunction with the MDK RawStub application, and makes it easy to transition into your solution.
Project: `configs/hdk/muc/raw_stub`
Firmware:
      `configs/hdk/muc/src/stm32_modsraw_stub.c`
APK: MDKRawStub, in the [mdk_examples repository](https://github.com/jksim/mdk_examples)

### compute {#compute}

This firmware only example enables MyDP (Display-Ext) and USB3.0 (USB-Ext) when using the MDK. With a MyDP dongle (to DP or HDMI) attached to the MDK's USB #3 port, and a USB3.0 device attached to USB #2, you have the beginnings of a dock. Use the MDKDisplay application to turn on/off display output.
Project: `configs/hdk/muc/compute`
Firmware:
      `drivers/hdmi_display.c`
      `drivers/fusb302.c`
APK: MDKDisplay, in the [mdk_display repository](https://github.com/jksim/mdkdisplay)

### hid {#hid}

This firmware only example shows the basic structure for implementing a HID device.
Project: `configs/hdk/muc/hid`
Firmware:
      `configs/hdk/muc/src/stm32_hid_example.c`
APK: None

### usb2 {#usb2}

This firmware only example configures USB2.0 through the dedicated path (not through the Moto HS Bridge). Since the MDK does *not* detect hot plug for USB2.0, the driver simply sets this to "On." When used in conjunction with an OTG cable, external USB devices can be plugged into the ports on the MDK. Or, USB devices can be wired directly in with a Perforated Board or HAT adapter.
Project: `configs/hdk/muc/usb2`
Firmware:
      `configs/hdk/muc/src/stm32_usbext_usb2.c`
APK: None

### termapp {#termapp}

This firmware and application combination is designed for quick and easy prototyping of a UART device. The firmware reads and writes from UART2 in the Moto Mod, and uses the Raw protocol to pass this to the application. ASCII or Binary data can be passed between the two and displayed in the app. Additionally, this application can control input/output for various available GPIOs on the MDK using the same Raw channel.
Project: `configs/hdk/muc/termapp`
Firmware:
      `configs/hdk/muc/src/stm32_modsraw_termapp.c`
APK: MDKTerminal, in the [mdk_examples repository](https://github.com/jksim/mdk_examples)

### flirapp {#flirapp}

This firmware and application combination uses the [FLiR Dev Kit](https://www.sparkfun.com/products/13233)  with the HAT Adapter board. This FLiR pins should be connected to the HAT 40-pin header as follows:
  CS: 23
  MOSI: 20
  MISO: 22
  CLK: 24
  GND: 5
  VIN: 2 (3.3V)
The SDA and SDL pins can be left unconnected.
Project: `configs/hdk/muc/flir`
Firmware:
      `configs/hdk/muc/src/flir_raw.c`
APK: FlirApp, in the [mdk_examples repository](https://github.com/jksim/mdk_examples)

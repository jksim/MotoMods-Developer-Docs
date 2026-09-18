---
title: "Moto Mods Firmware: USB-Ext Protocol"
source_url: http://developer.motorola.com/explore/firmware/usb-ext
source_capture: 2016 Squarespace portal
---

# Moto Mods Firmware: USB-Ext Protocol

## Overview

The Moto Mods platform make both USB 2.0 and USB 3.1 available to the Moto Mod.  The USB-Ext protocol controls which USB connection is used, the mode of operation and if the device is attached.

## Hardware Manifest {#hardware-manifest}

```ini
; USB-ext interface on CPort XX
[cport-descriptor XX]
bundle = YY
protocol = 0xec

; USB-ext Bundle YY
[bundle-descriptor YY]
class = 0x0f
```

**`XX`** is a unique integer (within your hardware manifest) defining which CPort is used for the USB-ext Interface.

**`YY`** is a unique integer (within your hardware manifest) which Bundle the USB-ext CPort is a member of.

## Implementation {#implementation}

### Files {#files}

**`nuttx/include/nuttx/device_usb_ext.h`**
**`nuttx/drivers/fusb302.c`**

### Interface Definition {#interface-definition}

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td></td>
<td>High-Speed Group A</td>
<td>High-Speed Group B</td>
</tr>
</thead>
<tr>
<td><strong>USB 2.0</strong></td>
<td>Yes</td>
<td>Yes</td>
</tr>
<tr>
<td><strong>USB 3.1</strong></td>
<td>No</td>
<td>Yes</td>
</tr>
</table>
</div></div>

USB 2.0 is available as a native physical interface if myDP is not being used at the same time. If myDP is required, you can use either USB 3.1 physical interface or a USB 2.0 HSIC interface provided by the Motorola High-Speed bridge. The USB 3.1 physical interface is not available when a Motorola High-Speed bridge is used in the system.

#### Configure Protocol and Path Using the Configuration Menu {#configure-protocol-and-path-using-the-configuration-menu}

To enable USB, the following modifications in menuconfig are required:

```
Device Drivers 
        [*]Greybus support
            [*]MODS support for USB
```

The behavior of the USB device is communicated to the Moto Z using the a notification of the change in attach state (usb_ext_event) and a few simple methods to get the state. The functions are defined in device_usb_ext.h, and an example implementation is available in the fusb302.c driver.

### Methods {#methods}

#### get_attached {#get_attached}

Returns state of USB connection.

```c
uint8_t get_attached(void)
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2">Parameters</td>
</tr>
</thead>
<tr>
<td><code>void</code></td>
<td>No parameters</td>
</tr>
<thead>
<tr>
<td colspan="2">Return</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>1 if USB device is attached,<br/> 0 otherwise</td>
</tr>
</table>
</div></div>

---

#### get_protocol {#get_protocol}

Returns protocol type of USB connection.

```c
uint8_t get_protocol(void)
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2">Parameters</td>
</tr>
</thead>
<tr>
<td><code>void</code></td>
<td>No parameters</td>
</tr>
<thead>
<tr>
<td colspan="2">Return</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>GB_USB_EXT_PROTOCOL_3_1 if connected to a USB 3.1 device,<br/> GB_USB_EXT_PROTOCOL_2_0 if connected to a USB 2.0 device</td>
</tr>
</table>
</div></div>

---

#### get_path {#get_path}

Returns path of USB connection.

```c
uint8_t get_path(void)
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2">Parameters</td>
</tr>
</thead>
<tr>
<td><code>void</code></td>
<td>No parameters</td>
</tr>
<thead>
<tr>
<td colspan="2">Return</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>GB_USB_EXT_PATH_A if using the Group A pins,<br/>
GB_USB_EXT_PATH_B if using the Group B pins</td>
</tr>
</table>
</div></div>

---

#### get_type {#get_type}

Returns type of USB connection.

```c
uint8_t get_type(void)
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2">Parameters</td>
</tr>
</thead>
<tr>
<td><code>void</code></td>
<td>No parameters</td>
</tr>
<thead>
<tr>
<td colspan="2">Return</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>GB_USB_EXT_REMOTE_DEVICE if the connected device is a USB device (the Moto Z should act as the host),<br/>
GB_USB_EXT_REMOTE_HOST if the device connected is a USB host (the Moto Z should act as the device)</td>
</tr>
</table>
</div></div>

### Callback Methods {#callback-methods}

#### register_callback {#register_callback}

Implement `register_callback` in ops and save the pointer provided (of type ‘`usb_ext_event_callback`’) to be called on attach.

```c
typedef int (*usb_ext_event_callback)(bool attached);
int (*register_callback)(struct device *dev, usb_ext_event_callback callback);
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2">Parameters</td>
</tr>
</thead>
<tr>
<td><code>dev</code></td>
<td>Matches dev passed to the probe function.</td>
</tr>
<tr>
<td><code>callback</code></td>
<td>Function implementing <code>usb_ext_event_callback.</code></td>
</tr>
<thead>
<tr>
<td colspan="2">Return</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

#### unregister_callback {#unregister_callback}

Implement a function to signal the provided pointer is no longer valid.

```c
int (*unregister_callback)(struct device *dev);
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2">Parameters</td>
</tr>
</thead>
<tr>
<td><code>dev</code></td>
<td>Matches dev passed to the probe function.</td>
</tr>
<thead>
<tr>
<td colspan="2">Return</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

Once configured, the only driver only needs to call send the attached state using the registered callback. The USB enumeration will be handled by the Moto Z side.

[< Previous Page
**HID Protocol**](hid.md)

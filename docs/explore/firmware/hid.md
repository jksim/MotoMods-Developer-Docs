---
title: "Moto Mods Firmware: HID Protocol"
source_url: http://developer.motorola.com/explore/firmware/hid
source_capture: 2016 Squarespace portal
---

# Moto Mods Firmware: HID Protocol

## Overview

The HID protocol provides a means for the Moto Mod to send Human Interface Device (HID) events to the Moto Z.  These standard events as outlined in the [USB org HID Protocol](http://www.usb.org/developers/hidpage/) are processed by Android on the Moto Z as native HID.

See [Moto Z Software: Mod HID](../software/mod-hid.md) for details of the Android usage of the HID protocol.

## Hardware Manifest {#hardware-manifest}

```ini
; HID interface on CPort XX
[cport-descriptor XX]
bundle = YY
protocol = 0x05

; HID Bundle YY
[bundle-descriptor YY]
class = 0x05
```

**`XX`** is a unique integer (within your hardware manifest) defining which CPort is used for the HID Interface.

**`YY`** is a unique integer (within your hardware manifest) which Bundle the HID CPort is a member of.

## Implementation {#implementation}

### Files {#files}

**`nuttx/include/nuttx/device_hid.h`**

### Structures {#structures}

#### hid_descriptor {#hid_descriptor}

```c
struct hid_descriptor {
    uint8_t length;
    uint16_t report_desc_length;
    uint16_t hid_version;
    uint16_t product_id;
    uint16_t vendor_id;
    uint8_t country_code;
};
```

### Callback Methods {#callback-methods}

The following types and methods provide a means for the driver implementing the HID device to send events to the Moto Z.

#### hid_event_callback {#hid_event_callback}

The `hid_event_callback` method sends a HID report to the Moto Z.

```c
typedef int hid_event_callback(struct device *dev, uint8_t report_type,
                                  uint8_t *report, uint16_t len);
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
<td><code>report_type</code></td>
<td>HID report_type.</td>
</tr>
<tr>
<td><code>report</code></td>
<td>HID report data  follows the HID specification <a>http://www.usb.org/developers/hidpage</a>.</td>
</tr>
<tr>
<td><code>len</code></td>
<td>Length of the report.</td>
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

#### register_callback {#register_callback}

`register_callback` is called when the greybus interface provides the method to send HID events to the Moto Z. If the driver needs to send HID events (which seems likely) the method should be stored so that it can be invoked for sending events.

```c
int (*register_callback)(struct device *dev, hid_event_callback callback);
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
<td>hid_event_callback</td>
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

Once the `unregister_callback` is called, the callee should assume the method provided in register_callback is now invalid.

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
<tr>
<td><code>callback</code></td>
<td>hid_event_callback</td>
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

### Methods {#methods}

#### power_on {#power_on}

Sent by the Moto Z to the Moto Mod to tell the device to turn on.

```c
int (*power_on)(struct device *dev);
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

---

#### power_off {#power_off}

Sent by the Moto Z to the Moto Mod to tell the device to turn off.

```c
int (*power_off)(struct device *dev);
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

---

#### get_descriptor {#get_descriptor}

`get_descriptor` returns the HID descriptor.

```c
int (*get_descriptor)(struct device *dev, struct hid_descriptor *desc);
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
<td><code>desc</code></td>
<td>Returns the descriptor associated with the the device functionality provided.</td>
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

#### get_report_descriptor {#get_report_descriptor}

`get_report_descriptor` returns the HID report descriptor.

```c
int (*get_report_descriptor)(struct device *dev, uint8_t *desc);
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
<td><code>desc</code></td>
<td>Returns the report descriptor as described by <a>http://www.usb.org/developers/hidpage/</a>.</td>
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

#### get_report_length {#get_report_length}

`get_report_length` returns the length of the report.

```c
int (*get_report_length)(struct device *dev, uint8_t report_type,
                             uint8_t report_id);
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
<td><code>report_type</code></td>
<td>The type of report (Input, Output, or Feature).</td>
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

#### get_maximum_report_length {#get_maximum_report_length}

`get_maximum_report_length` returns the maximum length of a report for the given type.

```c
int (*get_maximum_report_length)(struct device *dev, uint8_t report_type);
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
<td><code>report_type</code></td>
<td>The type of report (Input, Output, or Feature).</td>
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

#### get_report {#get_report}

`get_report` returns the HID report.

```c
int (*get_report)(struct device *dev, uint8_t report_type,
                      uint8_t report_id, uint8_t *data, uint16_t len);
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
<td><code>report_type</code></td>
<td>The type of the report (Input, Output, or Feature).</td>
</tr>
<tr>
<td><code>report_id</code></td>
<td>The specific report id from the descriptor.</td>
</tr>
<tr>
<td><code>data</code></td>
<td>The report data.</td>
</tr>
<tr>
<td><code>len</code></td>
<td>The length of the report data.</td>
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

#### set_report {#set_report}

`set_report` sends the HID report from Moto Z to the Moto Mod. Sends a report as documented at <http://www.usb.org/developers/hidpage/>

```c
int (*set_report)(struct device *dev, uint8_t report_type,
                      uint8_t report_id, uint8_t *data, uint16_t len);
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
<td><code>report_type</code></td>
<td>The type of the report (Input, Output, or Feature).</td>
</tr>
<tr>
<td><code>report_id</code></td>
<td>The specific report id from the descriptor.</td>
</tr>
<tr>
<td><code>data</code></td>
<td>The report data.</td>
</tr>
<tr>
<td><code>len</code></td>
<td>The length of the report data.</td>
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

[< Previous Page
**Audio Protocol**](audio.md)

[Next Page >
**USB-Ext Protocol**](usb-ext.md)

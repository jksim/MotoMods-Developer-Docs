---
title: "Moto Mods Firmware: Battery Protocol"
source_url: http://developer.motorola.com/explore/firmware/battery
source_capture: 2016 Squarespace portal
---

# Moto Mods Firmware: Battery Protocol

## Overview

The Battery protocol allows the Moto Z to inquire about the battery on the Moto Mod.  The data includes battery voltage, temperature and capacity.

To provide and receive power from the Moto Z, the Moto Mod is required to support the [Power Transfer Protocol](power-transfer.md).

## Hardware Manifest {#hardware-manifest}

Hardware Manifest files reside in `apps/greybus-utils/manifests`, one should be created for your unique project.

0x08 is the identifier for the Battery protocol.

Two entries are necessary for Battery, one for the Interface and one for the Bundle.

To support Charge Only mode, the Battery protocol must be in the Bundle with the Power Transfer protocol. If any other protocols are included in the bundle with Power Transfer and Battery, the Moto Mod will not be supported in Charge Only mode.

```ini
; Battery interface on CPort XX
[cport-descriptor XX]
bundle = YY
protocol = 0x08

; Battery related Bundle YY
[bundle-descriptor YY]
class = 0x08
```

**`XX`** shall be a unique integer (within your hardware manifest) defining which CPort is used for Battery.

**`YY`** shall be a unique integer (within your hardware manifest) which Bundle the Battery CPort is a member of.

## Implementation {#implementation}

The Low level Battery device driver is specific to the hardware and reports current battery state upon requests.

### Files {#files}

**`nuttx/include/nuttx/device_battery.h`**

> This file defines the `device_battery_type_ops` structure and provides the glue to the Greybus Battery channel.

**`nuttx/configs/ara/bridge/src/battery_dummy.c`**

> This file provides the starting point for your development. It should be copied into `nuttx/configs/PROJECT/src` for your specific Project and modified.

### Methods {#methods}

A battery device driver must implement methods defined in the `device_battery_type_ops` structure.

#### Reporting battery technology type: get_technology {#reporting-battery-technology-type-get_technology}

The `get_technology` function reports the technology type of the Moto Mod battery from a set of defined types.

```c
int (*get_technology)(struct device *dev, uint32_t *tech)
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="3">Parameters</td>
</tr>
</thead>
<tr>
<td><code>dev</code></td>
<td colspan="2">Pointer to structure of device data</td>
</tr>
<tr>
<td rowspan="2"><code>tech</code></td>
<td colspan="2">The output value is battery technology, based off a set of defined values:</td>
</tr>
<tr>
<td><code>GB_BATTERY_TECH_UNKNOWN<br/>GB_BATTERY_TECH_NiMH<br/>GB_BATTERY_TECH_LION<br/>GB_BATTERY_TECH_LIPO<br/>GB_BATTERY_TECH_LiFe<br/>GB_BATTERY_TECH_NiCd<br/>GB_BATTERY_TECH_LiMn</code></td>
<td><code>0x0000<br/>0x0001<br/>0x0002<br/>0x0003<br/>0x0004<br/>0x0005<br/>0x0006</code></td>
</tr>
<thead>
<tr>
<td colspan="3">Return</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td colspan="2">0 on success, negative errno on error</td>
</tr>
</table>
</div></div>

---

#### Reporting battery charging status: get_status {#reporting-battery-charging-status-get_status}

The `get_status` function reports the current charging status of the Moto Mod battery.

```c
int (*get_status)(struct device *dev, uint16_t *status)
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
<td>Pointer to structure of device data</td>
</tr>
<tr>
<td><code>status</code></td>
<td>The output value is battery status</td>
</tr>
<thead>
<tr>
<td colspan="2">Return</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error</td>
</tr>
</table>
</div></div>

---

#### Reporting battery voltage: get_voltage {#reporting-battery-voltage-get_voltage}

The `get_voltage` function reports an accurate reading of the Moto Mod battery voltage.

```c
int (*get_voltage)(struct device *dev, uint32_t *voltage)
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
<td>Pointer to structure of device data</td>
</tr>
<tr>
<td><code>voltage</code></td>
<td>The output value is battery voltage in microvolts</td>
</tr>
<thead>
<tr>
<td colspan="2">Return</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error</td>
</tr>
</table>
</div></div>

---

#### Reporting battery current: get_current {#reporting-battery-current-get_current}

The `get_current` function reports an accurate reading of the current being currently supplied or drawn from the Moto Mod battery.

```c
int (*get_current)(struct device *dev, int *current)
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
<td>Pointer to structure of device data</td>
</tr>
<tr>
<td><code>current</code></td>
<td>The output value is battery current in microamps</td>
</tr>
<thead>
<tr>
<td colspan="2">Return</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error</td>
</tr>
</table>
</div></div>

---

#### Reporting battery capacity in percentage: get_percent_capacity {#reporting-battery-capacity-in-percentage-get_percent_capacity}

The `get_percent_capacity` function reports Moto Mod battery percent capacity.

```c
int (*get_percent_capacity)(struct device *dev, uint32_t *percent_cap)
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
<td>Pointer to structure of device data</td>
</tr>
<tr>
<td><code>percent_cap</code></td>
<td>The output value is battery level in percent</td>
</tr>
<thead>
<tr>
<td colspan="2">Return</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error</td>
</tr>
</table>
</div></div>

---

#### Reporting battery total capacity: get_total_capacity {#reporting-battery-total-capacity-get_total_capacity}

The `get_total_capacity` function reports total Moto Mod battery capacity.

```c
int (*get_total_capacity)(struct device *dev, uint32_t *total_cap)
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
<td>Pointer to structure of device data</td>
</tr>
<tr>
<td><code>total_cap</code></td>
<td>The output value is battery total design capacity in mAh</td>
</tr>
<thead>
<tr>
<td colspan="2">Return</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error</td>
</tr>
</table>
</div></div>

---

#### Reporting battery temperature: get_temperature {#reporting-battery-temperature-get_temperature}

The `get_temperature` function reports current temperature of the Moto Mod battery.

```c
int (*get_temperature)(struct device *dev, int *temperature)
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
<td>Pointer to structure of device data</td>
</tr>
<tr>
<td><code>temperature</code></td>
<td>The output value is battery temperature in 0.1 Celsius</td>
</tr>
<thead>
<tr>
<td colspan="2">Return</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error</td>
</tr>
</table>
</div></div>

[< Previous Page
**Lights Protocol**](lights.md)

[Next Page >
**Power Transfer Protocol**](power-transfer.md)

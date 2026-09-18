---
title: "Moto Mods Firmware: Lights Protocol"
source_url: http://developer.motorola.com/explore/firmware/lights
source_capture: 2016 Squarespace portal
---

# Moto Mods Firmware: Lights Protocol

## Overview

The Lights protocol is used to control various light output devices.  Currently, the Moto Mods platform only supports a display backlight.  For your application to adjust a Moto Mod’s backlight, see [Moto Z Software: Mod Display](../software/mod-display.md).

## Hardware Manifest {#hardware-manifest}

```ini
; Lights interface on CPort XX
[cport-descriptor XX]
bundle = YY
protocol = 0x0f

; Lights Bundle YY
[bundle-descriptor YY]
class = 0x0f
```

**`XX`** is a unique integer (within your hardware manifest) defining which CPort is used for the Lights Interface.

**`YY`** is a unique integer (within your hardware manifest) which Bundle the Lights CPort is a member of.

## Implementation {#implementation}

### Files {#files}

**`nuttx/include/nuttx/device_lights.h`**

### Structures {#structures}

#### light_config {#light_config}

```c
struct light_config {
        uint8_t             channel_count;
        char                name[NAME_LENGTH];
};
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2"><strong>Parameters</strong></td>
</tr>
</thead>
<tr>
<td><code>channel_count</code></td>
<td>Number of Lights channels.</td>
</tr>
<tr>
<td><code>name</code></td>
<td>Unique name for this configuration.</td>
</tr>
</table>
</div></div>

---

#### channel_config {#channel_config}

```c
struct channel_config {
    uint8_t     max_brightness;
    uint32_t    flags;
    uint32_t    color;
    char        color_name[NAME_LENGTH];
    uint32_t    mode;
    char        mode_name[NAME_LENGTH];
}
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2"><strong>Parameters</strong></td>
</tr>
</thead>
<tr>
<td><code>max_brightness</code></td>
<td> Sets supported max brightness.</td>
</tr>
<tr>
<td><code>flags</code></td>
<td><p>Light channel behavior flag bitmask.<br/>
<code>LIGHTS_CHANNEL_FLAG_MULTICOLOR</code><br/>
<code>LIGHTS_CHANNEL_FLAG_FADER</code><br/>
<code>LIGHTS_CHANNEL_FLAG_BLINK</code></p></td>
</tr>
<tr>
<td><code>color</code></td>
<td> Color code value.</td>
</tr>
<tr>
<td><code>color_name</code></td>
<td>Color name, 31 characters with null character.</td>
</tr>
<tr>
<td><code>mode</code></td>
<td>Only Mode Vendor channel supported at this time.<br/>
<code>LIGHTS_CHANNEL_MODE_VENDOR</code></td>
</tr>
<tr>
<td><code>mode_name</code></td>
<td>Mode name, 31 characters with null character.</td>
</tr>
</table>
</div></div>

***See usage for specific Light channel configurations.**

---

### Methods {#methods}

#### get_lights {#get_lights}

```c
int (*get_lights)(struct device *dev, uint8_t *lights);
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2"><strong>Parameters</strong></td>
</tr>
</thead>
<tr>
<td><code>dev</code></td>
<td>Matches dev passed to the probe function.</td>
</tr>
<tr>
<td><code>lights</code></td>
<td>Returns the number of light configurations.</td>
</tr>
</table>
</div></div>

---

#### get_light_config {#get_light_config}

```c
int (*get_light_config)(struct device *dev, uint8_t id, struct light_config *cfg);
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2"><strong>Parameters</strong></td>
</tr>
</thead>
<tr>
<td><code>dev</code></td>
<td>Matches dev passed to the probe function.</td>
</tr>
<tr>
<td><code>cfg</code></td>
<td>Returns an array of light configurations.</td>
</tr>
</table>
</div></div>

---

#### get_channel_config {#get_channel_config}

```c
int (*get_channel_config)(struct device *dev, uint8_t light_id, uint8_t channel_id, struct channel_config *cfg);
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2"><strong>Parameters</strong></td>
</tr>
</thead>
<tr>
<td><code>dev</code></td>
<td>Matches dev passed to the probe function.</td>
</tr>
<tr>
<td><code>light_id</code></td>
<td>Index for which caller is requesting information.</td>
</tr>
<tr>
<td><code>channel_id</code></td>
<td>Channel Number for which the caller is requesting information.</td>
</tr>
<tr>
<td><code>channel_config</code></td>
<td>The configuration as documented above.</td>
</tr>
</table>
</div></div>

---

#### set_brightness {#set_brightness}

```c
int (*set_brightness)(struct device *dev, uint8_t light_id, uint8_t channel_id, uint8_t brightness);
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2"><strong>Parameters</strong></td>
</tr>
</thead>
<tr>
<td><code>dev</code></td>
<td>Matches dev passed to the probe function.</td>
</tr>
<tr>
<td><code>light_id</code></td>
<td>Index for which caller is requesting information.</td>
</tr>
<tr>
<td><code>channel_id</code></td>
<td>Channel Number for which the caller is requesting information.</td>
</tr>
<tr>
<td><code>brightness</code></td>
<td>Brightness level between 0 and <code>max_brightness</code>.</td>
</tr>
</table>
</div></div>

## Usage

### Backlight {#backlight}

The backlight channel of the Lights protocol uses mode `LIGHTS_CHANNEL_MODE_VENDOR` with a `mode_name` of “`backlight`” as follows:

#### channel_config

```c
struct channel_config {
    uint8_t     max_brightness;
    uint32_t    flags;
    uint32_t    color;
    char        color_name[NAME_LENGTH];
    uint32_t    mode;
    char        mode_name[NAME_LENGTH];
}
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2"><strong>Parameters (specifically for Display Backlight)</strong></td>
</tr>
</thead>
<tr>
<td><code>max_brightness</code></td>
<td>For display backlight should be set to <code>1</code>.</td>
</tr>
<tr>
<td><code>flags</code></td>
<td>No flags (set to <code>0</code>).</td>
</tr>
<tr>
<td><code>color</code></td>
<td>No colors (set to <code>0</code>).</td>
</tr>
<tr>
<td><code>color_name</code></td>
<td>Set to empty string.</td>
</tr>
<tr>
<td><code>mode</code></td>
<td><code>LIGHTS_CHANNEL_MODE_VENDOR</code></td>
</tr>
<tr>
<td><code>mode_name</code></td>
<td>“<code>backlight</code>”</td>
</tr>
</table>
</div></div>

[< Previous Page
**Display Protocol**](display.md)

[Next Page >
**Battery Protocol**](battery.md)

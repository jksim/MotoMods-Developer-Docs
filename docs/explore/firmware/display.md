---
title: "Moto Mods Firmware: Display Protocol"
source_url: http://developer.motorola.com/explore/firmware/display
source_capture: 2016 Squarespace portal
---

# Moto Mods Firmware: Display Protocol

## Overview

The Display protocol provides an abstract interface for controlling one additional real-time display device streaming video data using either MIPI DSI or Mobility DisplayPort (MyDP).

The Display protocol interface concerns itself with the 'control' path of a display device.  The actual video data-stream, or 'data' path, is out-of-band and not included in this interface.

- The interface provides a number of functions:
- Query and choose the configuration
- Register for and receive display events
- Query and set the current display state (e.g. on or off)

For DSI panels connected to the APBE using the Mods High-Speed Bridge (MHB) there is a default implementation, mhb_dsi_display, that implements the device-level interface and requires only a few helper functions to provide panel-specific configuration and commands.  The DSI display interface should be used for low-power mobile display functionality.

For DisplayPort devices, the implementation simply advertises the EDID configuration and sends display notification events.  The DisplayPort interface itself handles the rest.  The DisplayPort display interface should be used for DRM protected content and can support up to 4k30 resolution.

## Files {#files}

### Generic Files {#generic-files}

**`nuttx/include/nuttx/device_display.h`**

> This file defines the `device_display_type_ops` structure and provides a number of wrapper functions to safely call the operations in the structure.

### DSI-specific Files {#dsi-specific-files}

**`./nuttx/include/nuttx/mhb/mhb_dsi_display.h`**

> This file defines the function prototypes of the DSI panel-specific functions that you need to implement for a DSI panel.

**`./nuttx/include/nuttx/mhb/mhb_protocol.h`**

> This file defines the structures used in your implementation of the DSI panel-specific functions.

**`./nuttx/drivers/mhb/mhb_dsi_display.c`**

> This file implements the Display class interface for a generic DSI panel connected to the APBE using the Mods High-Speed Bridge (MHB). It requires a number of panel-specific functions to be implemented and linked in.

### DSI-specific Example Files {#dsi-specific-example-files}

**`./nuttx/drivers/display/smd_470_720p.c`**
**`./nuttx/drivers/display/tdi_546_1080p.c`**

> These files implement the panel-specific functions for a pair of example panels. For your specific panel, add `nuttx/drivers/display/<NEW_PANEL>.c` and update `nuttx/drivers/display/Kconfig` and `nuttx/drivers/display/Make.defs`.

**`./nuttx/configs/hdk/muc/src/stm32_boot.c`**

> This file provides an example Display class registration including the necessary device resources. This file provides the starting point for your development. It should be copied into `nuttx/configs/<NEW_PROJECT>/src` for your specific Project and modified.

### DisplayPort-specific Example Files {#displayport-specific-example-files}

**`./nuttx/drivers/hdmi_display.c`**

> This file is a 'skeleton' implementation of a DisplayPort driver that can be used to start your own DisplayPort device implementation.

### Generic Example Files {#generic-example-files}

**`./nuttx/drivers/null_display.c`**

> The file is a blank 'skeleton' driver that can be used to start your own implementation.

## Details

*(Not preserved: `firmwaredisplay-diagram-01.png` was not captured by the Wayback Machine and no copy survives.)*

### Display Notification Events {#display-notification-events}

The Greybus display class driver is the client of the Display device driver. It automatically registers and unregisters a callback function for display notification events. Your implementation must support exactly one registration. It must also send the appropriate display notification events when appropriate.

Below are the definitions for display notification events, the callback function, and the register and unregister functions.

#### Host Ready {#host-ready}

This operation is used by the client to notify implementations that it is ready to receive display notification events. This operation must be received before the your implementation can send any display notification events.

```c
int (*host_ready)(struct device *dev);
```

#### Display Notification Events

```
enum display_notification_event {
    DISPLAY_NOTIFICATION_EVENT_INVALID     = 0x00,
    DISPLAY_NOTIFICATION_EVENT_FAILURE     = 0x01,
    DISPLAY_NOTIFICATION_EVENT_AVAILABLE   = 0x02,
    DISPLAY_NOTIFICATION_EVENT_UNAVAILABLE = 0x03,
    DISPLAY_NOTIFICATION_EVENT_CONNECT     = 0x04,
    DISPLAY_NOTIFICATION_EVENT_DISCONNECT  = 0x05,
};
```

The display notification events are defined as follows:

- **`DISPLAY_NOTIFICATION_EVENT_INVALID`**: A reserved value, do not use.
- **`DISPLAY_NOTIFICATION_EVENT_FAILURE`**: Send this event if the display device has encountered a catastrophic failure that it cannot recover from.
- **`DISPLAY_NOTIFICATION_EVENT_AVAILABLE`**: Send this event when the display device software is available for operations from the phone. This is typically sent in response to the `host_ready()` call. The phone will not send operations before this event is received.
- **`DISPLAY_NOTIFICATION_EVENT_UNAVAILABLE`**: Send this event if the display device software is no longer available to receive operations from the phone. The phone will not send operations after this event is received.
- **`DISPLAY_NOTIFICATION_EVENT_CONNECT`**: Send this event when the display device hardware is ready to be used (e.g. turned on). For devices that are always connected (e.g. a DSI panel), this event can be sent immediately after the AVAILABLE event. For devices that are intermittently connected (e.g. an HDMI port), this event can be sent after an external device is plugged in.
- **`DISPLAY_NOTIFICATION_EVENT_DISCONNECT`**: Send this event when the display device hardware is no longer ready to be used. For devices that are intermittently connected (e.g. an HDMI port), this event can be sent after an external device is unplugged. For other devices, this event is not typically used.

#### Display Notification Callback {#display-notification-callback}

```c
typedef int (*display_notification_cb)(struct device *dev,
    enum display_notification_event event);
```

The callback function receives a pointer to the device and the display notification event. Clients handle these events as they see fit and return an errno. Your implementation *should* ignore the errno.

#### Register Callback {#register-callback}

```c
int (*register_callback)(struct device *dev, display_notification_cb cb);
```

This operation is used by clients to register a callback handler for display notification events. Your implementation *must* support at exactly one callback.

Callers pass a pointer to the device and a pointer to the callback function.

If a callback is not already registered, your implementation saves the callback function and returns success. If a callback is already registered, then return an errno.

#### Unregister Callback {#unregister-callback}

```c
int (*unregister_callback)(struct device *dev);
```

This operation is used by clients to unregister a previously registered callback handler for display notification events. It is an error to unregister a callback function if one was not previously registered.

Callers pass a pointer to the device.

If a callback is not already registered, your implementation clears the callback function and returns success. If a callback was not already registered, then return an errno.

### Configuration {#configuration}

Below are the configuration operations. Your driver must implement these operations and be prepared to handle them any time after sending a `DISPLAY_NOTIFICATION_EVENT_AVAILALBE` event and before sending a `DISPLAY_NOTIFICATION_EVENT_UNAVAILALBE` event.

#### Display Type {#display-type}

```
enum display_type {
    DISPLAY_TYPE_INVALID = 0x00,
    DISPLAY_TYPE_DSI     = 0x01,
    DISPLAY_TYPE_DP      = 0x02,
};
```

The display type describes the physical display interface:

- **`DISPLAY_TYPE_INVALID`**: Reserved, do not use.
- **`DISPLAY_TYPE_DSI`**: The Display device uses DSI.
- **`DISPLAY_TYPE_DP`**: The Display device uses DisplayPort

#### Display Config Type {#display-config-type}

```
enum display_config_type {
    DISPLAY_CONFIG_TYPE_INVALID  = 0x00,
    DISPLAY_CONFIG_TYPE_EDID_1P3 = 0x01,
    DISPLAY_CONFIG_TYPE_DSI      = 0x02,
};
```

The display config type describes the binary format of the config data returned by get_config().

- **`DISPLAY_CONFIG_TYPE_INVALID`**: Reserved, do not use.
- **`DISPLAY_CONFIG_TYPE_EDID_1P3`**: An EDID binary block as defined by VESA EDID version 1.3.
- **`DISPLAY_CONFIG_TYPE_DSI`**: A custom DSI-specific structure described in detail below.

DisplayPort implementations must use the EDID v1.3 format while DSI implementations must use the DSI format.

#### Get Config Size {#get-config-size}

```c
int (*get_config_size)(struct device *dev, uint32_t *size);
```

This operation requests the size, in bytes, of the configuration data that would be returned by a subsequent `get_config` operation.

Callers pass a pointer to the device and a pointer to a variable to hold the size.

Your implementation fills in the size and returns an appropriate errno value.

#### Get Config {#get-config}

```c
int (*get_config)(struct device *dev, uint8_t *display_type,
        uint8_t *config_type, uint32_t *size, uint8_t **config);
```

This operation requests the configuration or configurations supported by the display device.

Callers pass a pointer to the device and a pointers to a variable to the display type, display config type, config size, and config data.

Your implementation fills in the display type, config type, size, and config data and returns an appropriate errno value. If a config of size 0 is returned with an errno of 0, then the client will attempt to read the display configuration from another source (e.g. directly over DisplayPort). The exact format of the configuration data is discussed in more detail below.

#### Set Config {#set-config}

```c
int (*set_config)(struct device *dev, uint8_t index);
```

The EDID v1.3 format has the ability to specify more than one supported configuration. If this is the case, clients may want to select a configuration other than the default. The set_config operation allows clients to select, by zero-based index, the desired configuration.

Callers pass a pointer to the device and the zero-based index of the desired configuration.

Your implementation verifies the index and, if valid selects, the configuration. Otherwise, returns an errno. All implementations must support at least one configuration (index of 0) even if they return an zero-length config data.

### Configuration Data {#configuration-data}

For DSI Display devices, the config data is formatted as a custom binary structure. Some of these fields may not be important to the DSI panel itself, but are necessary for the phone.

#### DSI Mode {#dsi-mode}

```
enum display_config_dsi_mode {
    DISPLAY_CONFIG_DSI_MODE_VIDEO   = 0x00,
    DISPLAY_CONFIG_DSI_MODE_COMMAND = 0x01,
};
```

Selects DSI Command or Video Mode.

#### DSI Swap {#dsi-swap}

```
enum display_config_dsi_swap {
    DISPLAY_CONFIG_DSI_SWAP_RGB_TO_RGB = 0x00,
    DISPLAY_CONFIG_DSI_SWAP_RGB_TO_RBG = 0x01,
    DISPLAY_CONFIG_DSI_SWAP_RGB_TO_BGR = 0x02,
    DISPLAY_CONFIG_DSI_SWAP_RGB_TO_BRG = 0x03,
    DISPLAY_CONFIG_DSI_SWAP_RGB_TO_GRB = 0x04,
    DISPLAY_CONFIG_DSI_SWAP_RGB_TO_GBR = 0x05,
};
```

Selects the pixel color swapping. The default is no swapping (`DISPLAY_CONFIG_DSI_SWAP_RGB_TO_RGB`).

#### Continuous Clock {#continuous-clock}

```
enum display_config_dsi_continuous_clock {
    DISPLAY_CONFIG_DSI_CONTINUOUS_CLOCK_DISABLED = 0x00,
    DISPLAY_CONFIG_DSI_CONTINUOUS_CLOCK_ENABLED  = 0x01,
};
```

Selects if the DSI clock pair should be run continuously or just during transfers.

#### EOT Mode {#eot-mode}

```
enum display_config_dsi_eot_mode {
    DISPLAY_CONFIG_DSI_EOT_MODE_NONE   = 0x00,
    DISPLAY_CONFIG_DSI_EOT_MODE_APPEND = 0x01,
};
```

Selects if EOT should be append during DSI transmission.

#### VSync Mode {#vsync-mode}

```
enum display_config_dsi_vsync_mode {
    DISPLAY_CONFIG_DSI_VSYNC_MODE_NONE = 0x00,
    DISPLAY_CONFIG_DSI_VSYNC_MODE_GPIO = 0x01,
    DISPLAY_CONFIG_DSI_VSYNC_MODE_DCS  = 0x02,
};
```

Selects the vertical sync (vsync) mode:

- **`DISPLAY_CONFIG_DSI_VSYNC_MODE_NONE`**: No vsync
- **`DISPLAY_CONFIG_DSI_VSYNC_MODE_GPIO`**: Use GPIO for vsync
- **`DISPLAY_CONFIG_DSI_VSYNC_MODE_DCS`**: Use a DCS command for vsync

#### DSI Traffic Mode {#dsi-traffic-mode}

```
enum display_config_dsi_traffic_mode {
    DISPLAY_CONFIG_DSI_TRAFFIC_MODE_NON_BURST_SYNC_PULSE = 0x00,
    DISPLAY_CONFIG_DSI_TRAFFIC_MODE_NON_BURST_SYNC_EVENT = 0x01,
    DISPLAY_CONFIG_DSI_TRAFFIC_MODE_BURST                = 0x02,
};
```

Selects the DSI traffic mode.

Selects the vertical sync (vsync) mode:

- **`DISPLAY_CONFIG_DSI_TRAFFIC_MODE_NON_BURST_SYNC_PULSE`**: Sync pulse
- **`DISPLAY_CONFIG_DSI_TRAFFIC_MODE_NON_BURST_SYNC_EVENT`**: Sync event
- **`DISPLAY_CONFIG_DSI_TRAFFIC_MODE_BURST`**: Burst

#### DSI Pixel Packing {#dsi-pixel-packing}

```
enum display_config_dsi_pixel_packing {
    DISPLAY_CONFIG_DSI_PIXEL_PACKING_UNPACKED = 0x00,
};
```

Selects the pixel packing mode. Only unpacked is currently supported.

#### DSI Config {#dsi-config}

```c
struct display_dsi_config {
    /* MIPI manufacturer ID (http://mid.mipi.org) */
    uint16_t manufacturer_id;
    /* display_config_dsi_mode */
    uint8_t mode;
    /* 1-4 lanes */
    uint8_t num_lanes;

    /* pixels */
    uint16_t width;
    /* pixels */
    uint16_t height;

    /* millimeters */
    uint16_t physical_width_dim;
    /* millimeters */
    uint16_t physical_length_dim;

    /* frames-per-second */
    uint8_t framerate;
    /* bits-per-pixel */
    uint8_t bpp;
    /* must be zero */
    uint16_t reserved0;

    /* Hz */
    uint64_t clockrate;

    /* nanoseconds */
    uint16_t t_clk_pre;
    /* nanoseconds */
    uint16_t t_clk_post;

    /* display_config_dsi_continuous_clock */
    uint8_t continuous_clock;
    /* display_config_dsi_eot_mode */
    uint8_t eot_mode;
    /* display_config_dsi_vsync_mode */
    uint8_t vsync_mode;
    /* display_config_dsi_traffic_mode */
    uint8_t traffic_mode;

    /* DSI virtual channel (VC) ID */
    uint8_t virtual_channel_id;
    /* display_config_dsi_swap */
    uint8_t color_order;
    /* display_config_dsi_pixel_packing* */
    uint8_t pixel_packing;
    /* must be zero */
    uint8_t reserved1;

    /* pixels */
    uint16_t horizontal_front_porch;
    uint16_t horizontal_sync_pulse_width;
    uint16_t horizontal_sync_skew;
    uint16_t horizontal_back_porch;
    uint16_t horizontal_left_border;
    uint16_t horizontal_right_border;

    /* lines */
    uint16_t vertical_front_porch;
    uint16_t vertical_sync_pulse_width;
    uint16_t vertical_back_porch;
    uint16_t vertical_top_border;
    uint16_t vertical_bottom_border;
    uint16_t reserved2;
};
```

The DSI config structure includes all of the necessary parameters for configuring both RX and TX DSI interfaces on the phone, APBA, and APBE.

##### DSI Config

- **`manufacturer_id`:** MIPI manufacturer ID (<http://mid.mipi.org>) of the DSI display

##### DSI Interface {#dsi-interface}

- **`mode`:** Video or command DSI mode (`display_config_dsi_mode`).
- **`num_lanes`:** Number of DSI lanes. Only 1 through 4 are supported.

##### Format {#format}

- **`width`:** Display width in pixels.
- **`height`:** Display height in pixels.
- **`physical_width_dim`:** Display width in millimeters.
- **`physical_length_dim`:** Display height in millimeters.
- **`framerate`:** Display frame rate in frames-per-second.
- **`bpp`:** Bits per pixel (e.g. 24-bits, 8-bits for red, green, and blue).

##### Timing {#timing}

- **`clockrate`:** Desired clock-rate in Hz. This rate is not guaranteed. It may need to be adjusted based on specific hardware.
- **`t_clk_pre`:** `T_CLK_PRE` in nanoseconds.
- **`t_clk_post`:** `T_CLK_POST` in nanoseconds.

##### Options {#options}

- **`continuous_clock`:** Clock mode (`display_config_dsi_continuous_clock`)
- **`eot_mode: EOT mode`:** (`display_config_dsi_eot_mode`)
- **`vsync_mode`:** Vsync mode (`display_config_dsi_vsync_mode`)
- **`traffic_mode`:** Traffic mode (`display_config_dsi_traffic_mode`)
- **`virtual_channel_id`:** DSI virtual channel (VC) ID
- **`color_order`:** Color order (`display_config_dsi_swap`)
- **`pixel_packing`:** Pixel packing mode (`display_config_dsi_pixel_packing`)

##### Horizontal {#horizontal}

All vertical parameters are measured in *pixels*.

- **`horizontal_front_porch`**
- **`horizontal_sync_pulse_width`**
- **`horizontal_sync_skew`**
- **`horizontal_back_porch`**
- **`horizontal_left_border`**
- **`horizontal_right_border`**

##### Vertical {#vertical}

All vertical parameters are measured in *lines*.

- **`vertical_front_porch`**
- **`vertical_sync_pulse_width`**
- **`vertical_back_porch`**
- **`vertical_top_border`**
- **`vertical_bottom_border`**

##### Reserved {#reserved}

- **`reserved0`:** Reserved, must be zero.
- **`reserved1`:** Reserved, must be zero.
- **`reserved2`:** Reserved, must be zero.

### State {#state}

#### Display State {#display-state}

```
enum display_state {
    DISPLAY_STATE_OFF = 0x00,
    DISPLAY_STATE_ON  = 0x01,
};
```

The display state describes whether the Display device is on or off.

- **`DISPLAY_STATE_OFF`:** Off
- **`DISPLAY_STATE_ON`:** On

#### Get State {#get-state}

```c
int (*get_state)(struct device *dev, uint8_t *state);
```

This operation requests the current state of the Display device.

Callers pass a pointer to the device and a pointer to a variable to the state.

Your implementation fills in the current state and returns an appropriate errno value.

#### Set State {#set-state}

```c
int (*set_state)(struct device *dev, uint8_t state);
```

This operation sets the current state of the Display device.

Callers pass a pointer to the device and a the new state.

Your implementation changes state (if appropriate) and returns an appropriate errno value.

## Motorola High-Speed Bridge DSI Display {#motorola-high-speed-bridge-dsi-display}

### Introduction {#introduction}

Instead of writing a Display device driver, many DSI panels can make use of the generic MHB DSI Display driver. In these cases, your code just needs to implement the three panel-specific functions to configure the MHB DSI Display driver.

The steps are:

- Enable the `CONFIG_MHB_DSI_DISPLAY` configuration in your target's defconfig.
- Copy the example driver at ./nuttx/drivers/display/tdi_546_1080p.c into your own file.
- Add config entries in ./nuttx/drivers/display/Kconfig
- Add your new config to your target's defconfig.
- Add makefile entries in ./nuttx/drivers/display/Make.defs.
- Implement the functions in your target .c file.

### Details {#details}

#### MHB DSI Config {#mhb-dsi-config}

```c
struct mhb_cdsi_config {
    /* Common */
    uint8_t direction; /* RX: 0 (CDSI -> UniPro), TX: 1 (UniPro -> CDSI) */
    uint8_t mode;                    /* DSI: 0, CSI: 1 */
    uint8_t rx_num_lanes;            /* 1 to 4 */
    uint8_t tx_num_lanes;            /* 1 to 4 */
    uint32_t rx_bits_per_lane;       /* bits-per-lane */
    uint32_t tx_bits_per_lane;       /* bits-per-lane */
    /* RX only */
    uint32_t hs_rx_timeout;
    /* TX only */
    uint32_t pll_frs;
    uint32_t pll_prd;
    uint32_t pll_fbd;
    uint32_t framerate;              /* frames-per-second */
    uint32_t width;                  /* pixels */
    uint32_t height;                 /* pixels */
    uint32_t physical_width;         /* millimeters */
    uint32_t physical_height;        /* millimeters */
    uint32_t bpp;                    /* bits-per-pixel */
    uint32_t vss_control_payload;
    uint8_t bta_enabled;             /* 0: disabled, 1: enabled */
    uint8_t continuous_clock;        /* 0: off, 1: on */
    uint8_t blank_packet_enabled;
    uint8_t video_mode;              /* 0: video, 1: command */
    uint8_t color_bar_enabled;       /* 0: disabled */
    uint8_t keep_alive;              /* 0: disabled */
    uint8_t t_clk_pre;               /* nanoseconds */
    uint8_t t_clk_post;              /* nanoseconds */
    /* CSI only */
    /* DSI only */
    uint8_t horizontal_front_porch;  /* pixels */
    uint8_t horizontal_back_porch;   /* pixels */
    uint8_t horizontal_pulse_width;  /* pixels */
    uint8_t horizontal_sync_skew;    /* pixels */
    uint8_t horizontal_left_border;  /* pixels */
    uint8_t horizontal_right_border; /* pixels */
    uint8_t vertical_front_porch;    /* lines */
    uint8_t vertical_back_porch;     /* lines */
    uint8_t vertical_pulse_width;    /* lines */
    uint8_t vertical_top_border;     /* lines */
    uint8_t vertical_bottom_border;  /* lines */
    uint8_t vsync_mode;              /* 0: none, 1: gpio, 2: dcs */
} __attribute__((packed));
```

The MHB DSI Display driver uses a DSI config structure similar to that of the Display device interface. However, there are a few additional fields that are needed specifically for the APBE implementation.

The additional fields include:

- **`pll_frs`:** PLL FRS
- **`pll_prd`:** PLL PRD
- **`pll_fbd`:** PLL FBD

You can set these values to override the default PLL settings used to configure the APBE to achieve the corresponding bits-per-lane. See the Appendix for a table of valid PLL settings.

#### DSI Panel Info {#dsi-panel-info}

```c
struct mhb_dsi_panel_info {
    uint16_t supplier_id;
    uint8_t id0; /* optional */
    uint8_t id1; /* optional */
    uint8_t id2; /* optional */
} __attribute__((packed));
```

The DSI panel information structure includes the MIPI supplier ID and optionally up to three additional identifiers.

These values correspond to the respective DCS read results of:

- read_DDB_start (0xa1)
- 0xda
- 0xdb
- 0xdc

#### C-Types {#c-types}

```c
/* DSI and DCS */
#define MHB_CTYPE_HS_FLAG    (0x0)
#define MHB_CTYPE_LP_FLAG    (0x8)
#define MHB_CTYPE_SHORT_FLAG (0x0)
#define MHB_CTYPE_LONG_FLAG  (0x4)

#define MHB_CTYPE_HS_SHORT (MHB_CTYPE_HS_FLAG|MHB_CTYPE_SHORT_FLAG)
#define MHB_CTYPE_HS_LONG  (MHB_CTYPE_HS_FLAG|MHB_CTYPE_LONG_FLAG)
#define MHB_CTYPE_LP_SHORT (MHB_CTYPE_LP_FLAG|MHB_CTYPE_SHORT_FLAG)
#define MHB_CTYPE_LP_LONG  (MHB_CTYPE_LP_FLAG|MHB_CTYPE_LONG_FLAG)
```

These are the definitions for the C-Types. These correspond directly to the MIPI D-Phy specification.

#### D-Types {#d-types}

```c
/* Data Types for Processor-sourced Packets */
#define MHB_DTYPE_GEN_SHORT_WRITE0 0x03
#define MHB_DTYPE_GEN_SHORT_WRITE1 0x13
#define MHB_DTYPE_GEN_SHORT_WRITE2 0x23
#define MHB_DTYPE_GEN_READ0        0x04
#define MHB_DTYPE_GEN_READ1        0x14
#define MHB_DTYPE_GEN_READ2        0x24
#define MHB_DTYPE_DCS_WRITE0       0x05
#define MHB_DTYPE_DCS_WRITE1       0x15
#define MHB_DTYPE_DCS_READ0        0x06
#define MHB_DTYPE_MAX_RET_PKT      0x37
#define MHB_DTYPE_GEN_LONG_WRITE   0x29
#define MHB_DTYPE_DCS_LONG_WRITE   0x39
```

These are the definitions for the D-Types. These correspond directly to the MIPI D-Phy and DCS specifications.

#### DSI Command {#dsi-command}

```c
struct mhb_cdsi_cmd {
    uint8_t ctype;  /* MHB_CTYPE_* */
    uint8_t dtype;  /* MHB_DTYPE_* */
    uint16_t length;
    uint32_t delay; /* minimum microseconds to wait after command */
    union {
        uint16_t spdata;
        uint32_t lpdata[2];
    } u;
} __attribute__((packed));
```

This structure is used to specify a single DCS command to be written either during the panel on or off sequence.

Specify the appropriate C-Types and D-Types from the `MHB_CTYPE_*` and `MHB_DTYPE_*` definitions. Set the length of the data for both short and long packets.

Optionally set a delay, in microseconds, to wait after this command is written.

Set the data field depending on the packet type. For short packets, use spdata and for long packets, use lpdata. Data *must* be stored in the least-significant bytes.

##### Short Packet Example {#short-packet-example}

```
{ .ctype = MHB_CTYPE_LP_SHORT, .dtype = MHB_DTYPE_DCS_WRITE0, .length = 2, .u = { .spdata = 0x0011 }, .delay = 120000 }, /* exit_sleep_mode */
```

This sends a command with the following details:

- A short packet.
- A DCS write with 0 additional parameters, one parameter is automatically included.
- The automatic parameter is 0x11 which is the exit sleep mode command.
- The length of the data is 2 bytes (one byte for the D-Type and one byte for the parameter).
- Wait 120 milliseconds after sending.

##### Long Packet Example {#long-packet-example}

{ .ctype = MHB_CTYPE_LP_LONG, .dtype = MHB_DTYPE_DCS_LONG_WRITE, .length = 5, .u = { .lpdata = { 0x0002cf2a, 0x00000000 } }, .delay = 0 }, / *set_column_address* /

This sends a command with the following details:

- A long packet.
- A DCS long write.
- The data is 0x2a 0xcf 0x02 0x00 0x00. The 0x2a is the set_column_address command, 0xcf 0x02 0x00 0x00 byte-reversed is 0x000002cf which corresponds to 719. This is the max column for a 720p panel. Note that only the least-significant byte of lpdata[1] is used. The other bytes are ignored.
- The length is 5 bytes (one byte for the command and four bytes for the value).
- Do not wait after sending.

#### Get Config

```c
int _mhb_dsi_display_get_config(uint8_t instance,
    const struct mhb_dsi_panel_info *panel_info,
    const struct mhb_cdsi_config **cfg,
    size_t *size);
```

This function is used to specify the panel-specific configuration.

Callers pass a pointer to the panel info (if available) and pointers to variables to receive the configuration and configuration size.

Your implementation fills in the configuration and the size, in bytes, of the configuration. Your implementation *may* use the panel information to choose the appropriate configuration. However, the panel information may not always be available.

#### Get On-Commands {#get-on-commands}

```c
int _mhb_dsi_display_get_on_commands(uint8_t instance,
    const struct mhb_dsi_panel_info *panel_info,
    const struct mhb_cdsi_cmd **cmds,
    size_t *size);
```

This function is used to specify the panel-specific DCS commands to send before a panel is turned on.

Callers pass a pointer to the panel info (if available) and pointers to variables to receive the commands and command size.

Your implementation fills in the array of commands and the size, in bytes, of the array of commands. Your implementation may use the panel information to choose the appropriate commands. However, the panel information may not always be available.

#### Get Off-Commands {#get-off-commands}

```c
int _mhb_dsi_display_get_off_commands(uint8_t instance,
    const struct mhb_dsi_panel_info *panel_info,
    const struct mhb_cdsi_cmd **cmds,
    size_t *size);
```

This function is used to specify the panel-specific DCS commands to send before a panel is turned off.

Callers pass a pointer to the panel info (if available) and pointers to variables to receive the commands and command size.

Your implementation fills in the array of commands and the size, in bytes, of the array of commands. Your implementation *may* use the panel information to choose the appropriate commands. However, the panel information may not always be available.

## Greybus Manifest {#greybus-manifest}

The Greybus Manifest requires at least two entries for a Display class:

- The Display class
- A Bundle

If your Display device requires additional hardware to function, include those device classes in the same bundle. If your Display device has optional hardware that is useful, but not required to function, you may want to include it in its own bundle.

### Simple Display {#simple-display}

```ini
[cport-descriptor 2]
bundle = 2
protocol = 0xee        ; Display-Ext

[bundle-descriptor 2]
class = 0x0c           ; Display (bundle)
```

### Display and Backlight {#display-and-backlight}

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

### Display, Backlight, and Buttons {#display-backlight-and-buttons}

```ini
[cport-descriptor 2]
bundle = 2
protocol = 0xee        ; Display-Ext

[cport-descriptor 3]
bundle = 2
protocol = 0x0f        ; Lights

[bundle-descriptor 2]
class = 0x0c           ; Display (bundle)

[cport-descriptor 5]
bundle = 3
protocol = 0x05        ; HID

[bundle-descriptor 3]
class = 0x05           ; HID (bundle)
```

## Appendix: PLL Script {#appendix-pll-script}

The following is a Python 3 script to determine the appropriate PLL settings. It accepts the desired Mbps/lane as the argument.

```
#!/usr/bin/env python3
import sys

def measure(hz, pll_frs, pll_prd, pll_fbd):
    pll_vco = 2.0 * 19.2 * (float(pll_fbd) + 1.0) / (float(pll_prd) + 1.0)
    pll_vco_valid = (pll_vco > 1000.0 and pll_vco < 2000.0)

    hsck = pll_vco / (2.0 ** (float(pll_frs) + 1.0))
    hsck_valid = (hsck > 80.0 and hsck < 1000.0)

    valid = pll_vco_valid and hsck_valid
    if not valid:
        return

    delta = abs(hz - hsck)
    error = delta / hz * 100

    return (hz, hsck, delta, error, pll_frs, pll_prd, pll_fbd, pll_vco)

def find_valid(hz, pll_frs_width=2, pll_prd_width=4, pll_fbd_width=7, num_results=5):
    results = []

    for pll_frs in range(0, 2**pll_frs_width):
        for pll_prd in range(0, 2**pll_prd_width):
            for pll_fbd in range(0, 2**pll_fbd_width):
                result = measure(hz, pll_frs, pll_prd, pll_fbd)
                if result:
                    results.append(result)

    return sorted(results, key=lambda r: r[2])

def display_results(results):
    fmt = '{:^12}{:^12}{:^12}{:^7}{:^9}{:^9}{:^9}'
    print(fmt.format('Target', 'Actual', 'delta', 'error', 'pll_frs', 'pll_prd', 'pll_fbd'))
    print(fmt.format('(Mbps/lane)', '(Mbps/lane)', '(Mbps/lane)', '(%)', '', '', ''))
    print('-' * 70)

    for result in results:
        print('{:^12}{:^12.1f}{:^12.1f}{:^7.2}{:^9}{:^9}{:^9}'.format(*result))

    print()

if __name__ == '__main__':

    for arg in sys.argv[1:]:
        results = find_valid(hz=float(arg))
        display_results(results[0:5])
```

A sample session for an input of 807 Mbps/lane are as follows:

```console
$ ./pll.py 807
   Target      Actual      delta     error  pll_frs  pll_prd  pll_fbd 
(Mbps/lane) (Mbps/lane) (Mbps/lane)   (%)                              
----------------------------------------------------------------------
    807        806.4        0.6      0.074     0        0       41    
    807        806.4        0.6      0.074     0        1       83    
    807        806.4        0.6      0.074     0        2       125   
    807        812.8        5.8      0.72      0        2       126   
    807        800.0        7.0      0.87      0        2       124
```

The results from the script show the top five valid combinations of PLL settings that achieve an actual 806.4 Mbps/lanel. Any one of the top three results has an error of 0.074%.

## Appendix: PLL Table

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td>Frequency(MHz)</td>
<td>PLL_FRS</td>
<td>PLL_PRD</td>
<td>PLL_FBD</td>
</tr>
</thead>
<tr><td>80-81</td><td>3</td><td>1</td><td>66</td></tr>
<tr><td>80-81</td><td>3</td><td>2</td><td>100</td></tr>
<tr><td>81-82</td><td>3</td><td>0</td><td>33</td></tr>
<tr><td>81-82</td><td>3</td><td>1</td><td>67</td></tr>
<tr><td>81-82</td><td>3</td><td>2</td><td>101</td></tr>
<tr><td>82-83</td><td>3</td><td>1</td><td>68</td></tr>
<tr><td>82-83</td><td>3</td><td>2</td><td>102</td></tr>
<tr><td>83-84</td><td>3</td><td>2</td><td>103</td></tr>
<tr><td>84</td><td>3</td><td>0</td><td>34</td></tr>
<tr><td>84</td><td>3</td><td>1</td><td>69</td></tr>
<tr><td>84</td><td>3</td><td>2</td><td>104</td></tr>
<tr><td>84-85</td><td>3</td><td>2</td><td>105</td></tr>
<tr><td>85-86</td><td>3</td><td>1</td><td>70</td></tr>
<tr><td>85-86</td><td>3</td><td>2</td><td>106</td></tr>
<tr><td>86-87</td><td>3</td><td>0</td><td>35</td></tr>
<tr><td>86-87</td><td>3</td><td>1</td><td>71</td></tr>
<tr><td>86-87</td><td>3</td><td>2</td><td>107</td></tr>
<tr><td>87-88</td><td>3</td><td>1</td><td>72</td></tr>
<tr><td>87-88</td><td>3</td><td>2</td><td>108</td></tr>
<tr><td>88</td><td>3</td><td>2</td><td>109</td></tr>
<tr><td>88-89</td><td>3</td><td>0</td><td>36</td></tr>
<tr><td>88-89</td><td>3</td><td>1</td><td>73</td></tr>
<tr><td>88-89</td><td>3</td><td>2</td><td>110</td></tr>
<tr><td>89-90</td><td>3</td><td>2</td><td>111</td></tr>
<tr><td>90</td><td>3</td><td>1</td><td>74</td></tr>
<tr><td>90-91</td><td>3</td><td>2</td><td>112</td></tr>
<tr><td>91-92</td><td>3</td><td>0</td><td>37</td></tr>
<tr><td>91-92</td><td>3</td><td>1</td><td>75</td></tr>
<tr><td>91-92</td><td>3</td><td>2</td><td>113</td></tr>
<tr><td>92</td><td>3</td><td>2</td><td>114</td></tr>
<tr><td>92-93</td><td>3</td><td>1</td><td>76</td></tr>
<tr><td>92-93</td><td>3</td><td>2</td><td>115</td></tr>
<tr><td>93-94</td><td>3</td><td>0</td><td>38</td></tr>
<tr><td>93-94</td><td>3</td><td>1</td><td>77</td></tr>
<tr><td>93-94</td><td>3</td><td>2</td><td>116</td></tr>
<tr><td>94-95</td><td>3</td><td>1</td><td>78</td></tr>
<tr><td>94-95</td><td>3</td><td>2</td><td>117</td></tr>
<tr><td>95-96</td><td>3</td><td>2</td><td>118</td></tr>
<tr><td>96</td><td>3</td><td>0</td><td>39</td></tr>
<tr><td>96</td><td>3</td><td>1</td><td>79</td></tr>
<tr><td>96</td><td>3</td><td>2</td><td>119</td></tr>
<tr><td>96-97</td><td>3</td><td>2</td><td>120</td></tr>
<tr><td>97-98</td><td>3</td><td>1</td><td>80</td></tr>
<tr><td>97-98</td><td>3</td><td>2</td><td>121</td></tr>
<tr><td>98-99</td><td>3</td><td>0</td><td>40</td></tr>
<tr><td>98-99</td><td>3</td><td>1</td><td>81</td></tr>
<tr><td>98-99</td><td>3</td><td>2</td><td>122</td></tr>
<tr><td>99-100</td><td>3</td><td>1</td><td>82</td></tr>
<tr><td>99-100</td><td>3</td><td>2</td><td>123</td></tr>
<tr><td>100</td><td>3</td><td>2</td><td>124</td></tr>
<tr><td>100-101</td><td>3</td><td>0</td><td>41</td></tr>
<tr><td>100-101</td><td>3</td><td>1</td><td>83</td></tr>
<tr><td>100-101</td><td>3</td><td>2</td><td>125</td></tr>
<tr><td>101-102</td><td>3</td><td>2</td><td>126</td></tr>
<tr><td>102</td><td>3</td><td>1</td><td>84</td></tr>
<tr><td>102-103</td><td>3</td><td>2</td><td>127</td></tr>
<tr><td>103-104</td><td>3</td><td>0</td><td>42</td></tr>
<tr><td>103-104</td><td>3</td><td>1</td><td>85</td></tr>
<tr><td>104-105</td><td>3</td><td>1</td><td>86</td></tr>
<tr><td>105-106</td><td>3</td><td>0</td><td>43</td></tr>
<tr><td>105-106</td><td>3</td><td>1</td><td>87</td></tr>
<tr><td>106-107</td><td>3</td><td>1</td><td>88</td></tr>
<tr><td>108</td><td>3</td><td>0</td><td>44</td></tr>
<tr><td>108</td><td>3</td><td>1</td><td>89</td></tr>
<tr><td>109-110</td><td>3</td><td>1</td><td>90</td></tr>
<tr><td>110-111</td><td>3</td><td>0</td><td>45</td></tr>
<tr><td>110-111</td><td>3</td><td>1</td><td>91</td></tr>
<tr><td>111-112</td><td>3</td><td>1</td><td>92</td></tr>
<tr><td>112-113</td><td>3</td><td>0</td><td>46</td></tr>
<tr><td>112-113</td><td>3</td><td>1</td><td>93</td></tr>
<tr><td>114</td><td>3</td><td>1</td><td>94</td></tr>
<tr><td>115-116</td><td>3</td><td>0</td><td>47</td></tr>
<tr><td>115-116</td><td>3</td><td>1</td><td>95</td></tr>
<tr><td>116-117</td><td>3</td><td>1</td><td>96</td></tr>
<tr><td>117-118</td><td>3</td><td>0</td><td>48</td></tr>
<tr><td>117-118</td><td>3</td><td>1</td><td>97</td></tr>
<tr><td>118-119</td><td>3</td><td>1</td><td>98</td></tr>
<tr><td>120</td><td>3</td><td>0</td><td>49</td></tr>
<tr><td>120</td><td>3</td><td>1</td><td>99</td></tr>
<tr><td>121-122</td><td>3</td><td>1</td><td>100</td></tr>
<tr><td>122-123</td><td>3</td><td>0</td><td>50</td></tr>
<tr><td>122-123</td><td>3</td><td>1</td><td>101</td></tr>
<tr><td>123-124</td><td>3</td><td>1</td><td>102</td></tr>
<tr><td>124-125</td><td>3</td><td>0</td><td>51</td></tr>
<tr><td>124-125</td><td>3</td><td>1</td><td>103</td></tr>
<tr><td>126</td><td>2</td><td>3</td><td>104</td></tr>
<tr><td>126-127</td><td>2</td><td>2</td><td>78</td></tr>
<tr><td>127-128</td><td>2</td><td>1</td><td>52</td></tr>
<tr><td>127-128</td><td>2</td><td>3</td><td>105</td></tr>
<tr><td>128</td><td>2</td><td>2</td><td>79</td></tr>
<tr><td>128-129</td><td>2</td><td>3</td><td>106</td></tr>
<tr><td>129-130</td><td>2</td><td>0</td><td>26</td></tr>
<tr><td>129-130</td><td>2</td><td>1</td><td>53</td></tr>
<tr><td>129-130</td><td>2</td><td>2</td><td>80</td></tr>
<tr><td>129-130</td><td>2</td><td>3</td><td>107</td></tr>
<tr><td>130-131</td><td>2</td><td>3</td><td>108</td></tr>
<tr><td>131-132</td><td>2</td><td>2</td><td>81</td></tr>
<tr><td>132</td><td>2</td><td>1</td><td>54</td></tr>
<tr><td>132</td><td>2</td><td>3</td><td>109</td></tr>
<tr><td>132-133</td><td>2</td><td>2</td><td>82</td></tr>
<tr><td>133-134</td><td>2</td><td>3</td><td>110</td></tr>
<tr><td>134-135</td><td>2</td><td>0</td><td>27</td></tr>
<tr><td>134-135</td><td>2</td><td>1</td><td>55</td></tr>
<tr><td>134-135</td><td>2</td><td>2</td><td>83</td></tr>
<tr><td>134-135</td><td>2</td><td>3</td><td>111</td></tr>
<tr><td>135-136</td><td>2</td><td>3</td><td>112</td></tr>
<tr><td>136</td><td>2</td><td>2</td><td>84</td></tr>
<tr><td>136-137</td><td>2</td><td>1</td><td>56</td></tr>
<tr><td>136-137</td><td>2</td><td>3</td><td>113</td></tr>
<tr><td>137-138</td><td>2</td><td>2</td><td>85</td></tr>
<tr><td>138</td><td>2</td><td>3</td><td>114</td></tr>
<tr><td>139-140</td><td>2</td><td>0</td><td>28</td></tr>
<tr><td>139-140</td><td>2</td><td>1</td><td>57</td></tr>
<tr><td>139-140</td><td>2</td><td>2</td><td>86</td></tr>
<tr><td>139-140</td><td>2</td><td>3</td><td>115</td></tr>
<tr><td>140-141</td><td>2</td><td>2</td><td>87</td></tr>
<tr><td>140-141</td><td>2</td><td>3</td><td>116</td></tr>
<tr><td>141-142</td><td>2</td><td>1</td><td>58</td></tr>
<tr><td>141-142</td><td>2</td><td>3</td><td>117</td></tr>
<tr><td>142-143</td><td>2</td><td>2</td><td>88</td></tr>
<tr><td>142-143</td><td>2</td><td>3</td><td>118</td></tr>
<tr><td>144</td><td>2</td><td>0</td><td>29</td></tr>
<tr><td>144</td><td>2</td><td>1</td><td>59</td></tr>
<tr><td>144</td><td>2</td><td>2</td><td>89</td></tr>
<tr><td>144</td><td>2</td><td>3</td><td>119</td></tr>
<tr><td>145-146</td><td>2</td><td>2</td><td>90</td></tr>
<tr><td>145-146</td><td>2</td><td>3</td><td>120</td></tr>
<tr><td>146-147</td><td>2</td><td>1</td><td>60</td></tr>
<tr><td>146-147</td><td>2</td><td>3</td><td>121</td></tr>
<tr><td>147-148</td><td>2</td><td>2</td><td>91</td></tr>
<tr><td>147-148</td><td>2</td><td>3</td><td>122</td></tr>
<tr><td>148-149</td><td>2</td><td>0</td><td>30</td></tr>
<tr><td>148-149</td><td>2</td><td>1</td><td>61</td></tr>
<tr><td>148-149</td><td>2</td><td>2</td><td>92</td></tr>
<tr><td>148-149</td><td>2</td><td>3</td><td>123</td></tr>
<tr><td>150</td><td>2</td><td>3</td><td>124</td></tr>
<tr><td>150-151</td><td>2</td><td>2</td><td>93</td></tr>
<tr><td>151-152</td><td>2</td><td>1</td><td>62</td></tr>
<tr><td>151-152</td><td>2</td><td>3</td><td>125</td></tr>
<tr><td>152</td><td>2</td><td>2</td><td>94</td></tr>
<tr><td>152-153</td><td>2</td><td>3</td><td>126</td></tr>
<tr><td>153-154</td><td>2</td><td>0</td><td>31</td></tr>
<tr><td>153-154</td><td>2</td><td>1</td><td>63</td></tr>
<tr><td>153-154</td><td>2</td><td>2</td><td>95</td></tr>
<tr><td>153-154</td><td>2</td><td>3</td><td>127</td></tr>
<tr><td>155-156</td><td>2</td><td>2</td><td>96</td></tr>
<tr><td>156</td><td>2</td><td>1</td><td>64</td></tr>
<tr><td>156-157</td><td>2</td><td>2</td><td>97</td></tr>
<tr><td>158-159</td><td>2</td><td>0</td><td>32</td></tr>
<tr><td>158-159</td><td>2</td><td>1</td><td>65</td></tr>
<tr><td>158-159</td><td>2</td><td>2</td><td>98</td></tr>
<tr><td>160</td><td>2</td><td>2</td><td>99</td></tr>
<tr><td>160-161</td><td>2</td><td>1</td><td>66</td></tr>
<tr><td>161-162</td><td>2</td><td>2</td><td>100</td></tr>
<tr><td>163-164</td><td>2</td><td>0</td><td>33</td></tr>
<tr><td>163-164</td><td>2</td><td>1</td><td>67</td></tr>
<tr><td>163-164</td><td>2</td><td>2</td><td>101</td></tr>
<tr><td>164-165</td><td>2</td><td>2</td><td>102</td></tr>
<tr><td>165-166</td><td>2</td><td>1</td><td>68</td></tr>
<tr><td>166-167</td><td>2</td><td>2</td><td>103</td></tr>
<tr><td>168</td><td>2</td><td>0</td><td>34</td></tr>
<tr><td>168</td><td>2</td><td>1</td><td>69</td></tr>
<tr><td>168</td><td>2</td><td>2</td><td>104</td></tr>
<tr><td>169-170</td><td>2</td><td>2</td><td>105</td></tr>
<tr><td>170-171</td><td>2</td><td>1</td><td>70</td></tr>
<tr><td>171-172</td><td>2</td><td>2</td><td>106</td></tr>
<tr><td>172-173</td><td>2</td><td>0</td><td>35</td></tr>
<tr><td>172-173</td><td>2</td><td>1</td><td>71</td></tr>
<tr><td>172-173</td><td>2</td><td>2</td><td>107</td></tr>
<tr><td>174-175</td><td>2</td><td>2</td><td>108</td></tr>
<tr><td>175-176</td><td>2</td><td>1</td><td>72</td></tr>
<tr><td>176</td><td>2</td><td>2</td><td>109</td></tr>
<tr><td>177-178</td><td>2</td><td>0</td><td>36</td></tr>
<tr><td>177-178</td><td>2</td><td>1</td><td>73</td></tr>
<tr><td>177-178</td><td>2</td><td>2</td><td>110</td></tr>
<tr><td>179-180</td><td>2</td><td>2</td><td>111</td></tr>
<tr><td>180</td><td>2</td><td>1</td><td>74</td></tr>
<tr><td>180-181</td><td>2</td><td>2</td><td>112</td></tr>
<tr><td>182-183</td><td>2</td><td>0</td><td>37</td></tr>
<tr><td>182-183</td><td>2</td><td>1</td><td>75</td></tr>
<tr><td>182-183</td><td>2</td><td>2</td><td>113</td></tr>
<tr><td>184</td><td>2</td><td>2</td><td>114</td></tr>
<tr><td>184-185</td><td>2</td><td>1</td><td>76</td></tr>
<tr><td>185-186</td><td>2</td><td>2</td><td>115</td></tr>
<tr><td>187-188</td><td>2</td><td>0</td><td>38</td></tr>
<tr><td>187-188</td><td>2</td><td>1</td><td>77</td></tr>
<tr><td>187-188</td><td>2</td><td>2</td><td>116</td></tr>
<tr><td>188-189</td><td>2</td><td>2</td><td>117</td></tr>
<tr><td>189-190</td><td>2</td><td>1</td><td>78</td></tr>
<tr><td>190-191</td><td>2</td><td>2</td><td>118</td></tr>
<tr><td>192</td><td>2</td><td>0</td><td>39</td></tr>
<tr><td>192</td><td>2</td><td>1</td><td>79</td></tr>
<tr><td>192</td><td>2</td><td>2</td><td>119</td></tr>
<tr><td>193-194</td><td>2</td><td>2</td><td>120</td></tr>
<tr><td>194-195</td><td>2</td><td>1</td><td>80</td></tr>
<tr><td>195-196</td><td>2</td><td>2</td><td>121</td></tr>
<tr><td>196-197</td><td>2</td><td>0</td><td>40</td></tr>
<tr><td>196-197</td><td>2</td><td>1</td><td>81</td></tr>
<tr><td>196-197</td><td>2</td><td>2</td><td>122</td></tr>
<tr><td>198-199</td><td>2</td><td>2</td><td>123</td></tr>
<tr><td>199-200</td><td>2</td><td>1</td><td>82</td></tr>
<tr><td>200</td><td>2</td><td>2</td><td>124</td></tr>
<tr><td>201-202</td><td>2</td><td>0</td><td>41</td></tr>
<tr><td>201-202</td><td>2</td><td>1</td><td>83</td></tr>
<tr><td>201-202</td><td>2</td><td>2</td><td>125</td></tr>
<tr><td>203-204</td><td>2</td><td>2</td><td>126</td></tr>
<tr><td>204</td><td>2</td><td>1</td><td>84</td></tr>
<tr><td>204-205</td><td>2</td><td>2</td><td>127</td></tr>
<tr><td>206-207</td><td>2</td><td>0</td><td>42</td></tr>
<tr><td>206-207</td><td>2</td><td>1</td><td>85</td></tr>
<tr><td>208-209</td><td>2</td><td>1</td><td>86</td></tr>
<tr><td>211-212</td><td>2</td><td>0</td><td>43</td></tr>
<tr><td>211-212</td><td>2</td><td>1</td><td>87</td></tr>
<tr><td>213-214</td><td>2</td><td>1</td><td>88</td></tr>
<tr><td>216</td><td>2</td><td>0</td><td>44</td></tr>
<tr><td>216</td><td>2</td><td>1</td><td>89</td></tr>
<tr><td>218-219</td><td>2</td><td>1</td><td>90</td></tr>
<tr><td>220-221</td><td>2</td><td>0</td><td>45</td></tr>
<tr><td>220-221</td><td>2</td><td>1</td><td>91</td></tr>
<tr><td>223-224</td><td>2</td><td>1</td><td>92</td></tr>
<tr><td>225-226</td><td>2</td><td>0</td><td>46</td></tr>
<tr><td>225-226</td><td>2</td><td>1</td><td>93</td></tr>
<tr><td>228</td><td>2</td><td>1</td><td>94</td></tr>
<tr><td>230-231</td><td>2</td><td>0</td><td>47</td></tr>
<tr><td>230-231</td><td>2</td><td>1</td><td>95</td></tr>
<tr><td>232-233</td><td>2</td><td>1</td><td>96</td></tr>
<tr><td>235-236</td><td>2</td><td>0</td><td>48</td></tr>
<tr><td>235-236</td><td>2</td><td>1</td><td>97</td></tr>
<tr><td>237-238</td><td>2</td><td>1</td><td>98</td></tr>
<tr><td>240</td><td>2</td><td>0</td><td>49</td></tr>
<tr><td>240</td><td>2</td><td>1</td><td>99</td></tr>
<tr><td>242-243</td><td>2</td><td>1</td><td>100</td></tr>
<tr><td>244-245</td><td>2</td><td>0</td><td>50</td></tr>
<tr><td>244-245</td><td>2</td><td>1</td><td>101</td></tr>
<tr><td>247-248</td><td>2</td><td>1</td><td>102</td></tr>
<tr><td>249-250</td><td>2</td><td>0</td><td>51</td></tr>
<tr><td>249-250</td><td>2</td><td>1</td><td>103</td></tr>
<tr><td>252</td><td>1</td><td>3</td><td>104</td></tr>
<tr><td>252-253</td><td>1</td><td>2</td><td>78</td></tr>
<tr><td>254-255</td><td>1</td><td>1</td><td>52</td></tr>
<tr><td>254-255</td><td>1</td><td>3</td><td>105</td></tr>
<tr><td>256</td><td>1</td><td>2</td><td>79</td></tr>
<tr><td>256-257</td><td>1</td><td>3</td><td>106</td></tr>
<tr><td>259-260</td><td>1</td><td>0</td><td>26</td></tr>
<tr><td>259-260</td><td>1</td><td>1</td><td>53</td></tr>
<tr><td>259-260</td><td>1</td><td>2</td><td>80</td></tr>
<tr><td>259-260</td><td>1</td><td>3</td><td>107</td></tr>
<tr><td>261-262</td><td>1</td><td>3</td><td>108</td></tr>
<tr><td>262-263</td><td>1</td><td>2</td><td>81</td></tr>
<tr><td>264</td><td>1</td><td>1</td><td>54</td></tr>
<tr><td>264</td><td>1</td><td>3</td><td>109</td></tr>
<tr><td>265-266</td><td>1</td><td>2</td><td>82</td></tr>
<tr><td>266-267</td><td>1</td><td>3</td><td>110</td></tr>
<tr><td>268-269</td><td>1</td><td>0</td><td>27</td></tr>
<tr><td>268-269</td><td>1</td><td>1</td><td>55</td></tr>
<tr><td>268-269</td><td>1</td><td>2</td><td>83</td></tr>
<tr><td>268-269</td><td>1</td><td>3</td><td>111</td></tr>
<tr><td>271-272</td><td>1</td><td>3</td><td>112</td></tr>
<tr><td>272</td><td>1</td><td>2</td><td>84</td></tr>
<tr><td>273-274</td><td>1</td><td>1</td><td>56</td></tr>
<tr><td>273-274</td><td>1</td><td>3</td><td>113</td></tr>
<tr><td>275-276</td><td>1</td><td>2</td><td>85</td></tr>
<tr><td>276</td><td>1</td><td>3</td><td>114</td></tr>
<tr><td>278-279</td><td>1</td><td>0</td><td>28</td></tr>
<tr><td>278-279</td><td>1</td><td>1</td><td>57</td></tr>
<tr><td>278-279</td><td>1</td><td>2</td><td>86</td></tr>
<tr><td>278-279</td><td>1</td><td>3</td><td>115</td></tr>
<tr><td>280-281</td><td>1</td><td>3</td><td>116</td></tr>
<tr><td>281-282</td><td>1</td><td>2</td><td>87</td></tr>
<tr><td>283-284</td><td>1</td><td>1</td><td>58</td></tr>
<tr><td>283-284</td><td>1</td><td>3</td><td>117</td></tr>
<tr><td>284-285</td><td>1</td><td>2</td><td>88</td></tr>
<tr><td>285-286</td><td>1</td><td>3</td><td>118</td></tr>
<tr><td>288</td><td>1</td><td>0</td><td>29</td></tr>
<tr><td>288</td><td>1</td><td>1</td><td>59</td></tr>
<tr><td>288</td><td>1</td><td>2</td><td>89</td></tr>
<tr><td>288</td><td>1</td><td>3</td><td>119</td></tr>
<tr><td>290-291</td><td>1</td><td>3</td><td>120</td></tr>
<tr><td>291-292</td><td>1</td><td>2</td><td>90</td></tr>
<tr><td>292-293</td><td>1</td><td>1</td><td>60</td></tr>
<tr><td>292-293</td><td>1</td><td>3</td><td>121</td></tr>
<tr><td>294-295</td><td>1</td><td>2</td><td>91</td></tr>
<tr><td>295-296</td><td>1</td><td>3</td><td>122</td></tr>
<tr><td>297-298</td><td>1</td><td>0</td><td>30</td></tr>
<tr><td>297-298</td><td>1</td><td>1</td><td>61</td></tr>
<tr><td>297-298</td><td>1</td><td>2</td><td>92</td></tr>
<tr><td>297-298</td><td>1</td><td>3</td><td>123</td></tr>
<tr><td>300</td><td>1</td><td>3</td><td>124</td></tr>
<tr><td>300-301</td><td>1</td><td>2</td><td>93</td></tr>
<tr><td>302-303</td><td>1</td><td>1</td><td>62</td></tr>
<tr><td>302-303</td><td>1</td><td>3</td><td>125</td></tr>
<tr><td>304</td><td>1</td><td>2</td><td>94</td></tr>
<tr><td>304-305</td><td>1</td><td>3</td><td>126</td></tr>
<tr><td>307-308</td><td>1</td><td>0</td><td>31</td></tr>
<tr><td>307-308</td><td>1</td><td>1</td><td>63</td></tr>
<tr><td>307-308</td><td>1</td><td>2</td><td>95</td></tr>
<tr><td>307-308</td><td>1</td><td>3</td><td>127</td></tr>
<tr><td>310-311</td><td>1</td><td>2</td><td>96</td></tr>
<tr><td>312</td><td>1</td><td>1</td><td>64</td></tr>
<tr><td>313-314</td><td>1</td><td>2</td><td>97</td></tr>
<tr><td>316-317</td><td>1</td><td>0</td><td>32</td></tr>
<tr><td>316-317</td><td>1</td><td>1</td><td>65</td></tr>
<tr><td>316-317</td><td>1</td><td>2</td><td>98</td></tr>
<tr><td>320</td><td>1</td><td>2</td><td>99</td></tr>
<tr><td>321-322</td><td>1</td><td>1</td><td>66</td></tr>
<tr><td>323-324</td><td>1</td><td>2</td><td>100</td></tr>
<tr><td>326-327</td><td>1</td><td>0</td><td>33</td></tr>
<tr><td>326-327</td><td>1</td><td>1</td><td>67</td></tr>
<tr><td>326-327</td><td>1</td><td>2</td><td>101</td></tr>
<tr><td>329-330</td><td>1</td><td>2</td><td>102</td></tr>
<tr><td>331-332</td><td>1</td><td>1</td><td>68</td></tr>
<tr><td>332-333</td><td>1</td><td>2</td><td>103</td></tr>
<tr><td>336</td><td>1</td><td>0</td><td>34</td></tr>
<tr><td>336</td><td>1</td><td>1</td><td>69</td></tr>
<tr><td>336</td><td>1</td><td>2</td><td>104</td></tr>
<tr><td>339-340</td><td>1</td><td>2</td><td>105</td></tr>
<tr><td>340-341</td><td>1</td><td>1</td><td>70</td></tr>
<tr><td>342-343</td><td>1</td><td>2</td><td>106</td></tr>
<tr><td>345-346</td><td>1</td><td>0</td><td>35</td></tr>
<tr><td>345-346</td><td>1</td><td>1</td><td>71</td></tr>
<tr><td>345-346</td><td>1</td><td>2</td><td>107</td></tr>
<tr><td>348-349</td><td>1</td><td>2</td><td>108</td></tr>
<tr><td>350-351</td><td>1</td><td>1</td><td>72</td></tr>
<tr><td>352</td><td>1</td><td>2</td><td>109</td></tr>
<tr><td>355-356</td><td>1</td><td>0</td><td>36</td></tr>
<tr><td>355-356</td><td>1</td><td>1</td><td>73</td></tr>
<tr><td>355-356</td><td>1</td><td>2</td><td>110</td></tr>
<tr><td>358-359</td><td>1</td><td>2</td><td>111</td></tr>
<tr><td>360</td><td>1</td><td>1</td><td>74</td></tr>
<tr><td>361-362</td><td>1</td><td>2</td><td>112</td></tr>
<tr><td>364-365</td><td>1</td><td>0</td><td>37</td></tr>
<tr><td>364-365</td><td>1</td><td>1</td><td>75</td></tr>
<tr><td>364-365</td><td>1</td><td>2</td><td>113</td></tr>
<tr><td>368</td><td>1</td><td>2</td><td>114</td></tr>
<tr><td>369-370</td><td>1</td><td>1</td><td>76</td></tr>
<tr><td>371-372</td><td>1</td><td>2</td><td>115</td></tr>
<tr><td>374-375</td><td>1</td><td>0</td><td>38</td></tr>
<tr><td>374-375</td><td>1</td><td>1</td><td>77</td></tr>
<tr><td>374-375</td><td>1</td><td>2</td><td>116</td></tr>
<tr><td>377-378</td><td>1</td><td>2</td><td>117</td></tr>
<tr><td>379-380</td><td>1</td><td>1</td><td>78</td></tr>
<tr><td>380-381</td><td>1</td><td>2</td><td>118</td></tr>
<tr><td>384</td><td>1</td><td>0</td><td>39</td></tr>
<tr><td>384</td><td>1</td><td>1</td><td>79</td></tr>
<tr><td>384</td><td>1</td><td>2</td><td>119</td></tr>
<tr><td>387-388</td><td>1</td><td>2</td><td>120</td></tr>
<tr><td>388-389</td><td>1</td><td>1</td><td>80</td></tr>
<tr><td>390-391</td><td>1</td><td>2</td><td>121</td></tr>
<tr><td>393-394</td><td>1</td><td>0</td><td>40</td></tr>
<tr><td>393-394</td><td>1</td><td>1</td><td>81</td></tr>
<tr><td>393-394</td><td>1</td><td>2</td><td>122</td></tr>
<tr><td>396-397</td><td>1</td><td>2</td><td>123</td></tr>
<tr><td>398-399</td><td>1</td><td>1</td><td>82</td></tr>
<tr><td>400</td><td>1</td><td>2</td><td>124</td></tr>
<tr><td>403-404</td><td>1</td><td>0</td><td>41</td></tr>
<tr><td>403-404</td><td>1</td><td>1</td><td>83</td></tr>
<tr><td>403-404</td><td>1</td><td>2</td><td>125</td></tr>
<tr><td>406-407</td><td>1</td><td>2</td><td>126</td></tr>
<tr><td>408</td><td>1</td><td>1</td><td>84</td></tr>
<tr><td>409-410</td><td>1</td><td>2</td><td>127</td></tr>
<tr><td>412-413</td><td>1</td><td>0</td><td>42</td></tr>
<tr><td>412-413</td><td>1</td><td>1</td><td>85</td></tr>
<tr><td>417-418</td><td>1</td><td>1</td><td>86</td></tr>
<tr><td>422-423</td><td>1</td><td>0</td><td>43</td></tr>
<tr><td>422-423</td><td>1</td><td>1</td><td>87</td></tr>
<tr><td>427-428</td><td>1</td><td>1</td><td>88</td></tr>
<tr><td>432</td><td>1</td><td>0</td><td>44</td></tr>
<tr><td>432</td><td>1</td><td>1</td><td>89</td></tr>
<tr><td>436-437</td><td>1</td><td>1</td><td>90</td></tr>
<tr><td>441-442</td><td>1</td><td>0</td><td>45</td></tr>
<tr><td>441-442</td><td>1</td><td>1</td><td>91</td></tr>
<tr><td>446-447</td><td>1</td><td>1</td><td>92</td></tr>
<tr><td>451-452</td><td>1</td><td>0</td><td>46</td></tr>
<tr><td>451-452</td><td>1</td><td>1</td><td>93</td></tr>
<tr><td>456</td><td>1</td><td>1</td><td>94</td></tr>
<tr><td>460-461</td><td>1</td><td>0</td><td>47</td></tr>
<tr><td>460-461</td><td>1</td><td>1</td><td>95</td></tr>
<tr><td>465-466</td><td>1</td><td>1</td><td>96</td></tr>
<tr><td>470-471</td><td>1</td><td>0</td><td>48</td></tr>
<tr><td>470-471</td><td>1</td><td>1</td><td>97</td></tr>
<tr><td>475-476</td><td>1</td><td>1</td><td>98</td></tr>
<tr><td>480</td><td>1</td><td>0</td><td>49</td></tr>
<tr><td>480</td><td>1</td><td>1</td><td>99</td></tr>
<tr><td>484-485</td><td>1</td><td>1</td><td>100</td></tr>
<tr><td>489-490</td><td>1</td><td>0</td><td>50</td></tr>
<tr><td>489-490</td><td>1</td><td>1</td><td>101</td></tr>
<tr><td>494-495</td><td>1</td><td>1</td><td>102</td></tr>
<tr><td>499-500</td><td>1</td><td>0</td><td>51</td></tr>
<tr><td>499-500</td><td>1</td><td>1</td><td>103</td></tr>
<tr><td>504</td><td>0</td><td>3</td><td>104</td></tr>
<tr><td>505-506</td><td>0</td><td>2</td><td>78</td></tr>
<tr><td>508-509</td><td>0</td><td>1</td><td>52</td></tr>
<tr><td>508-509</td><td>0</td><td>3</td><td>105</td></tr>
<tr><td>512</td><td>0</td><td>2</td><td>79</td></tr>
<tr><td>513-514</td><td>0</td><td>3</td><td>106</td></tr>
<tr><td>518-519</td><td>0</td><td>0</td><td>26</td></tr>
<tr><td>518-519</td><td>0</td><td>1</td><td>53</td></tr>
<tr><td>518-519</td><td>0</td><td>2</td><td>80</td></tr>
<tr><td>518-519</td><td>0</td><td>3</td><td>107</td></tr>
<tr><td>523-524</td><td>0</td><td>3</td><td>108</td></tr>
<tr><td>524-525</td><td>0</td><td>2</td><td>81</td></tr>
<tr><td>528</td><td>0</td><td>1</td><td>54</td></tr>
<tr><td>528</td><td>0</td><td>3</td><td>109</td></tr>
<tr><td>531-532</td><td>0</td><td>2</td><td>82</td></tr>
<tr><td>532-533</td><td>0</td><td>3</td><td>110</td></tr>
<tr><td>537-538</td><td>0</td><td>0</td><td>27</td></tr>
<tr><td>537-538</td><td>0</td><td>1</td><td>55</td></tr>
<tr><td>537-538</td><td>0</td><td>2</td><td>83</td></tr>
<tr><td>537-538</td><td>0</td><td>3</td><td>111</td></tr>
<tr><td>542-543</td><td>0</td><td>3</td><td>112</td></tr>
<tr><td>544</td><td>0</td><td>2</td><td>84</td></tr>
<tr><td>547-548</td><td>0</td><td>1</td><td>56</td></tr>
<tr><td>547-548</td><td>0</td><td>3</td><td>113</td></tr>
<tr><td>550-551</td><td>0</td><td>2</td><td>85</td></tr>
<tr><td>552</td><td>0</td><td>3</td><td>114</td></tr>
<tr><td>556-557</td><td>0</td><td>0</td><td>28</td></tr>
<tr><td>556-557</td><td>0</td><td>1</td><td>57</td></tr>
<tr><td>556-557</td><td>0</td><td>2</td><td>86</td></tr>
<tr><td>556-557</td><td>0</td><td>3</td><td>115</td></tr>
<tr><td>561-562</td><td>0</td><td>3</td><td>116</td></tr>
<tr><td>563-564</td><td>0</td><td>2</td><td>87</td></tr>
<tr><td>566-567</td><td>0</td><td>1</td><td>58</td></tr>
<tr><td>566-567</td><td>0</td><td>3</td><td>117</td></tr>
<tr><td>569-570</td><td>0</td><td>2</td><td>88</td></tr>
<tr><td>571-572</td><td>0</td><td>3</td><td>118</td></tr>
<tr><td>576</td><td>0</td><td>0</td><td>29</td></tr>
<tr><td>576</td><td>0</td><td>1</td><td>59</td></tr>
<tr><td>576</td><td>0</td><td>2</td><td>89</td></tr>
<tr><td>576</td><td>0</td><td>3</td><td>119</td></tr>
<tr><td>580-581</td><td>0</td><td>3</td><td>120</td></tr>
<tr><td>582-583</td><td>0</td><td>2</td><td>90</td></tr>
<tr><td>585-586</td><td>0</td><td>1</td><td>60</td></tr>
<tr><td>585-586</td><td>0</td><td>3</td><td>121</td></tr>
<tr><td>588-589</td><td>0</td><td>2</td><td>91</td></tr>
<tr><td>590-591</td><td>0</td><td>3</td><td>122</td></tr>
<tr><td>595-596</td><td>0</td><td>0</td><td>30</td></tr>
<tr><td>595-596</td><td>0</td><td>1</td><td>61</td></tr>
<tr><td>595-596</td><td>0</td><td>2</td><td>92</td></tr>
<tr><td>595-596</td><td>0</td><td>3</td><td>123</td></tr>
<tr><td>600</td><td>0</td><td>3</td><td>124</td></tr>
<tr><td>601-602</td><td>0</td><td>2</td><td>93</td></tr>
<tr><td>604-605</td><td>0</td><td>1</td><td>62</td></tr>
<tr><td>604-605</td><td>0</td><td>3</td><td>125</td></tr>
<tr><td>608</td><td>0</td><td>2</td><td>94</td></tr>
<tr><td>609-610</td><td>0</td><td>3</td><td>126</td></tr>
<tr><td>614-615</td><td>0</td><td>0</td><td>31</td></tr>
<tr><td>614-615</td><td>0</td><td>1</td><td>63</td></tr>
<tr><td>614-615</td><td>0</td><td>2</td><td>95</td></tr>
<tr><td>614-615</td><td>0</td><td>3</td><td>127</td></tr>
<tr><td>620-621</td><td>0</td><td>2</td><td>96</td></tr>
<tr><td>624</td><td>0</td><td>1</td><td>64</td></tr>
<tr><td>627-628</td><td>0</td><td>2</td><td>97</td></tr>
<tr><td>633-634</td><td>0</td><td>0</td><td>32</td></tr>
<tr><td>633-634</td><td>0</td><td>1</td><td>65</td></tr>
<tr><td>633-634</td><td>0</td><td>2</td><td>98</td></tr>
<tr><td>640</td><td>0</td><td>2</td><td>99</td></tr>
<tr><td>643-644</td><td>0</td><td>1</td><td>66</td></tr>
<tr><td>646-647</td><td>0</td><td>2</td><td>100</td></tr>
<tr><td>652-653</td><td>0</td><td>0</td><td>33</td></tr>
<tr><td>652-653</td><td>0</td><td>1</td><td>67</td></tr>
<tr><td>652-653</td><td>0</td><td>2</td><td>101</td></tr>
<tr><td>659-660</td><td>0</td><td>2</td><td>102</td></tr>
<tr><td>662-663</td><td>0</td><td>1</td><td>68</td></tr>
<tr><td>665-666</td><td>0</td><td>2</td><td>103</td></tr>
<tr><td>672</td><td>0</td><td>0</td><td>34</td></tr>
<tr><td>672</td><td>0</td><td>1</td><td>69</td></tr>
<tr><td>672</td><td>0</td><td>2</td><td>104</td></tr>
<tr><td>678-679</td><td>0</td><td>2</td><td>105</td></tr>
<tr><td>681-682</td><td>0</td><td>1</td><td>70</td></tr>
<tr><td>684-685</td><td>0</td><td>2</td><td>106</td></tr>
<tr><td>691-692</td><td>0</td><td>0</td><td>35</td></tr>
<tr><td>691-692</td><td>0</td><td>1</td><td>71</td></tr>
<tr><td>691-692</td><td>0</td><td>2</td><td>107</td></tr>
<tr><td>697-698</td><td>0</td><td>2</td><td>108</td></tr>
<tr><td>700-701</td><td>0</td><td>1</td><td>72</td></tr>
<tr><td>704</td><td>0</td><td>2</td><td>109</td></tr>
<tr><td>710-711</td><td>0</td><td>0</td><td>36</td></tr>
<tr><td>710-711</td><td>0</td><td>1</td><td>73</td></tr>
<tr><td>710-711</td><td>0</td><td>2</td><td>110</td></tr>
<tr><td>716-717</td><td>0</td><td>2</td><td>111</td></tr>
<tr><td>720</td><td>0</td><td>1</td><td>74</td></tr>
<tr><td>723-724</td><td>0</td><td>2</td><td>112</td></tr>
<tr><td>729-730</td><td>0</td><td>0</td><td>37</td></tr>
<tr><td>729-730</td><td>0</td><td>1</td><td>75</td></tr>
<tr><td>729-730</td><td>0</td><td>2</td><td>113</td></tr>
<tr><td>736</td><td>0</td><td>2</td><td>114</td></tr>
<tr><td>739-740</td><td>0</td><td>1</td><td>76</td></tr>
<tr><td>742-743</td><td>0</td><td>2</td><td>115</td></tr>
<tr><td>748-749</td><td>0</td><td>0</td><td>38</td></tr>
<tr><td>748-749</td><td>0</td><td>1</td><td>77</td></tr>
<tr><td>748-749</td><td>0</td><td>2</td><td>116</td></tr>
<tr><td>755-756</td><td>0</td><td>2</td><td>117</td></tr>
<tr><td>758-759</td><td>0</td><td>1</td><td>78</td></tr>
<tr><td>761-762</td><td>0</td><td>2</td><td>118</td></tr>
<tr><td>768</td><td>0</td><td>0</td><td>39</td></tr>
<tr><td>768</td><td>0</td><td>1</td><td>79</td></tr>
<tr><td>768</td><td>0</td><td>2</td><td>119</td></tr>
<tr><td>774-775</td><td>0</td><td>2</td><td>120</td></tr>
<tr><td>777-778</td><td>0</td><td>1</td><td>80</td></tr>
<tr><td>780-781</td><td>0</td><td>2</td><td>121</td></tr>
<tr><td>787-788</td><td>0</td><td>0</td><td>40</td></tr>
<tr><td>787-788</td><td>0</td><td>1</td><td>81</td></tr>
<tr><td>787-788</td><td>0</td><td>2</td><td>122</td></tr>
<tr><td>793-794</td><td>0</td><td>2</td><td>123</td></tr>
<tr><td>796-797</td><td>0</td><td>1</td><td>82</td></tr>
<tr><td>800</td><td>0</td><td>2</td><td>124</td></tr>
<tr><td>806-807</td><td>0</td><td>0</td><td>41</td></tr>
<tr><td>806-807</td><td>0</td><td>1</td><td>83</td></tr>
<tr><td>806-807</td><td>0</td><td>2</td><td>125</td></tr>
<tr><td>812-813</td><td>0</td><td>2</td><td>126</td></tr>
<tr><td>816</td><td>0</td><td>1</td><td>84</td></tr>
<tr><td>819-820</td><td>0</td><td>2</td><td>127</td></tr>
<tr><td>825-826</td><td>0</td><td>0</td><td>42</td></tr>
<tr><td>825-826</td><td>0</td><td>1</td><td>85</td></tr>
<tr><td>835-836</td><td>0</td><td>1</td><td>86</td></tr>
<tr><td>844-845</td><td>0</td><td>0</td><td>43</td></tr>
<tr><td>844-845</td><td>0</td><td>1</td><td>87</td></tr>
<tr><td>854-855</td><td>0</td><td>1</td><td>88</td></tr>
<tr><td>864</td><td>0</td><td>0</td><td>44</td></tr>
<tr><td>864</td><td>0</td><td>1</td><td>89</td></tr>
<tr><td>873-874</td><td>0</td><td>1</td><td>90</td></tr>
<tr><td>883-884</td><td>0</td><td>0</td><td>45</td></tr>
<tr><td>883-884</td><td>0</td><td>1</td><td>91</td></tr>
<tr><td>892-893</td><td>0</td><td>1</td><td>92</td></tr>
<tr><td>902-903</td><td>0</td><td>0</td><td>46</td></tr>
<tr><td>902-903</td><td>0</td><td>1</td><td>93</td></tr>
<tr><td>912</td><td>0</td><td>1</td><td>94</td></tr>
<tr><td>921-922</td><td>0</td><td>0</td><td>47</td></tr>
<tr><td>921-922</td><td>0</td><td>1</td><td>95</td></tr>
<tr><td>931-932</td><td>0</td><td>1</td><td>96</td></tr>
<tr><td>940-941</td><td>0</td><td>0</td><td>48</td></tr>
<tr><td>940-941</td><td>0</td><td>1</td><td>97</td></tr>
<tr><td>950-951</td><td>0</td><td>1</td><td>98</td></tr>
<tr><td>960</td><td>0</td><td>0</td><td>49</td></tr>
<tr><td>960</td><td>0</td><td>1</td><td>99</td></tr>
<tr><td>969-970</td><td>0</td><td>1</td><td>100</td></tr>
<tr><td>979-980</td><td>0</td><td>0</td><td>50</td></tr>
<tr><td>979-980</td><td>0</td><td>1</td><td>101</td></tr>
<tr><td>988-989</td><td>0</td><td>1</td><td>102</td></tr>
<tr><td>998-999</td><td>0</td><td>0</td><td>51</td></tr>
<tr><td>998-999</td><td>0</td><td>1</td><td>103</td></tr>
</table>
</div></div>

[< Previous Page
**Raw Protocol**](raw.md)

[Next Page >
**Lights Protocol**](lights.md)

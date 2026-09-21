---
title: "Examples: Audio Personality Card"
source_url: http://developer.motorola.com/build/examples/audio
source_capture: 2016 Squarespace portal
---

# Examples: Audio Personality Card

## Overview {#overview}

Audio Personality Card provides an example of a Moto Mod with audio output/speaker.

This card comes with [TFA9890 speaker Amplifier](http://www.nxp.com/products/media-and-audio-processing/audio-amplifiers/audio-amplifiers-for-portable-devices/boosted-class-d-audio-amplifier-with-speaker-boost-protection-algorithm:TFA9890UK), a class-D audio amplifier with a 9.5V on chip boosted. The audio channel interfaces with the Host system via the I2S interface. Logic interface is accessed via I2C and GPIO.

## Before you begin... {#before-you-begin}

#### Required Hardware {#required-hardware}

This app and example requires a **Moto Z**, **Reference Moto Mod**, and an **Audio Personality Card**. To get started, you'll need to buy the required hardware.

#### Software and Tools {#software-and-tools}

See the [Build > Tools](../tools/index.md) section to set up your development environment and learn about building from source, flashing firmware, and how to debug & log.

#### Download Example Source Code {#download-example-source-code}

- **Open source application code** for the MDK Audio App is available at <https://github.com/jksim/mdkaudio>.
- **Open source firmware code** for this example is located at <https://github.com/jksim/nuttx> - specifically:
  - Build Target: <https://github.com/jksim/nuttx/tree/master/nuttx/configs/hdk/muc/speaker>
  - Source Directory: <https://github.com/jksim/nuttx/tree/master/nuttx/configs/hdk/muc/src>

#### Download Schematics & More {#download-schematics-more}

We also provide schematics, layouts, BOMs, and CAD files for this example. See the [Downloads](#downloads) section at the end of this page.

#### 'MDK Audio' App {#-mdk-audio-app}

The MDK Audio App will only work on Moto Z devices.

- [MDK Audio app (rebuilt from source; was on Google Play Store)](../../assets/apks/mdkaudio.apk)
- [MDK Audio app (rebuilt from source; was on Lenovo App Store)](../../assets/apks/mdkaudio.apk)

For more details, see the [Moto Mods Android Application](#application) section further down this page.

#### Community and Support {#community-and-support}

Ask questions, engage with the developer community, and get support for this example in the [Moto Mods group at element14.com](https://www.element14.com/community/groups/moto-mods). Also check out our [Support](../../support/index.md) page.

## Electrical Details {#electrical}

#### Block Diagram

Speaker card connected to HDK and phone.

*(Diagram coming soon...)*

#### Pin Connection Table {#pin-connection-table}

*(Table coming soon...)*

#### Schematic & Layout {#schematic-layout}

See the [Downloads](#downloads) section at the end of this page for the schematic, layout and more.

## Hardware Setup {#hardware}

To use the Audio Personality Card, first detach the Reference Moto Mod from the Moto Z. Locate [dip switch A1](../mdk-user-guide/reference-moto-mod.md#overview) on the Mod and turn it off and [dip switch A2](../mdk-user-guide/reference-moto-mod.md#overview) on to enable using Audio from the example card, then insert the card into the Mod following [these instructions](../mdk-user-guide/reference-moto-mod.md#example-personality-cards). The Reference Moto Mod can be attached back to the Moto Z after that.

## Firmware Development {#firmware}

Follow [these instructions](../tools/index.md) to setup your firmware development environment and download source code if it has not been done already.The Moto Mods base firmware has a target for the Speaker Personality Card. The information below details the steps to create firmware for the Speaker Personality Card as if this support did not exist and needed to be added.

Speaker card utilizes tfa9890 speaker amplifier which features a 9.5 V boosted audio system with adaptive sound maximizer and speaker protection to drive a loudspeaker. It supports audio input for playback on standard I2S interface. Registers on the tfa9890 are read and written using I2C with slave address of 0x34.

#### New Build Target {#new-build-target}

Create a new build target for the Speaker Personality Card using hdk/muc/base_powered target as the base.

```console
$ cd $BUILD_TOP/nuttx/nuttx/configs/hdk/muc
$ mkdir speaker
$ cp base_powered/* speaker/
```

Switch to using the new build target.

```console
$ cd $BUILD_TOP/nuttx/nuttx/tools
$ ./configure.sh hdk/muc/speaker
```

The new target does not support required functionality yet. The [Mods Audio and I2S Management](../../explore/firmware/audio.md) protocols need to be added to support necessary functionality, Along with I2C bus to talk TFA9890 IC.

#### I2S Management Protocol {#i2s-management-protocol}

##### Files {#files}

- `nuttx/drivers/greybus/i2s-gb-direct-mgmt.c` - I2S Management protocol for raw I2S case uses a hardware specific device driver to set up and control I2S bus. Make below configuration changes to enable it.

##### Configuration Changes {#configuration-changes}

Set the configuration options to enable I2S Management Protocol.

```console
$ cd $BUILD_TOP/nuttx/nuttx
$ make menuconfig
```
```
Device Drivers  --->  
[*] Greybus support  --->
[*]   Mods I2S Support
```

#### Mods Audio Protocol {#mods-audio-protocol}

##### Files

- `nuttx/drivers/greybus/audio-gb.c` - Mods Audio protocol uses hardware specific device driver to enable/disable audio devices, set/get volume and set stream info. To enable it make below configuration changes.

##### Configuration Changes

Enable Mods Audio protocol and select custom audio chip device driver options as shown below

```console
$ cd $BUILD_TOP/nuttx/nuttx
$ make menuconfig
```
```
Device Drivers  --->  
[*] Greybus support  --->
[*]   Mods Audio support
           Select a audio dev driver (use custom audio chip driver)
```

Make above two configuration changes and save the change to nuttx/configs/hdk/muc/speaker/defconfig,

#### Device Driver Implementation Details {#device-driver-implementation-details}

##### Kconfig {#kconfig}

Add below config options to the Kconfig located at nuttx/configs/hdk/muc/Kconfig, needed to enable tfa9890 device driver needed for speaker personality card. Greybus config dependencies GREYBUS_MODS_AUDIO, GREYBUS_MODS_AUDIO_CUSTOM and GREYBUS_MODS_I2S_PHY are enabled by the config changes done to enable I2S Management Protocol and Mods Audio Protocol.

```
config MODS_AUDIO_TFA9890
    bool "Audio TFA9890 Speaker"
    default n
    depends on GREYBUS_MODS_AUDIO && GREYBUS_MODS_AUDIO_CUSTOM
    depends on GREYBUS_MODS_I2S_PHY
    select DEVICE_CORE
    select I2C
    select I2C_TRANSFER
    select I2C_WRITEREAD
    ---help---
        Enable Audio TFA9890 Speaker Support

config MODS_TFA9890_I2C_BUS
    int "TFA9890 I2C Bus Number"
    default 1
    depends on MODS_AUDIO_TFA9890
    ---help---
        I2C bus to use to communicate with device (default 1).

if MODS_AUDIO_TFA9890
choice
    prompt "Select a tfa9890 config mono or stereo"
config MODS_AUDIO_TFA9890_STEREO
    bool "STEREO"
config MODS_AUDIO_TFA9890_MONO
    bool "MONO"
endchoice
endif

config MODS_TFA9890_LEFT_I2C_ADDR
    int "TFA9890 LEFT I2C ADDR"
    default 52
    depends on MODS_AUDIO_TFA9890_STEREO
    ---help---
        I2C addr to use to communicate with device (default 52).

config MODS_TFA9890_RIGHT_I2C_ADDR
    int "TFA9890 RIGHT I2C ADDR"
    default 53
    depends on MODS_AUDIO_TFA9890_STEREO
    ---help---
        I2C addr to use to communicate with device (default 53).

config MODS_TFA9890_MONO_I2C_ADDR
    int "TFA9890 MONO I2C ADDR"
    default 52
    depends on MODS_AUDIO_TFA9890_MONO
    ---help---
        I2C addr to use to communicate with device (default 52).
```

##### Configuration changes: {#configuration-changes-}

After making change to kconfig, Enable device driver and its dependencies as shown below

```console
$ cd $BUILD_TOP/nuttx/nuttx
$ make menuconfig
```

->Enable I2C Driver support

```
Device Drivers  --->  
[*] I2C Driver support  --->
[*]  Support the I2C transfer() method
[*] Support the I2C writeread() method
```

-> Enable TFA9890 device driver, set up the I2C bus to 3 and address to 0x34, and select mono configuration as speaker personality card uses single speaker.

```
Board Selection  --->  
[*] Audio TFA9890 Speaker --->
(3) Tfa9890 I2C Bus Number
                  Select a tfa9890 config mono or stereo (MONO) --->
            (52) TFA9890 MONO I2C ADDR
```

Make above configuration changes and save the file to nuttx/configs/hdk/muc/speaker/defconfig.

#### Driver and Device Initialization {#driver-and-device-initialization}

Device drivers are initialized in nuttx/configs/hdk/muc/src/stm32_boot.c
Add I2S management and mods audio devices to the devices[] list, and include gpio type resources needed to reset and enable. The GPIOs are defined in nuttx/configs/hdk/muc/include/mods.h

```c
#ifdef CONFIG_MODS_AUDIO_TFA9890
static struct device_resource tfa9890_audio_resources[] = {
    {
       .name   = "audio_en",
       .type   = DEVICE_RESOURCE_TYPE_GPIO,
       .start  = GPIO_MODS_DEMO_ENABLE,
       .count  = 1,
    },
    {
       .name   = "rst_ls",
       .type   = DEVICE_RESOURCE_TYPE_GPIO,
       .start  = GPIO_MODS_RST_LS,
       .count  = 1,
    },
};

#ifdef CONFIG_MODS_AUDIO_TFA9890
    {
        .type = DEVICE_TYPE_I2S_HW,
        .name   = "tfa9890_i2s_direct_driver",
        .desc   = "TFA9890 I2S Direct Driver",
        .id   = 1,
    },
    {
        .type = DEVICE_TYPE_MUC_AUD_HW,
        .name   = "audio_tfa9890_device_driver",
        .desc   = "Audio Tfa9890 Device Driver",
        .id   = 2,
        .resources = tfa9890_audio_resources,
        .resource_count = ARRAY_SIZE(tfa9890_audio_resources),
    },
#endif
```

##### Device audio driver interface Implementation: {#device-audio-driver-interface-implementation-}

Device driver is implemented in nuttx/configs/hdk/muc/src/stm32_audio_tfa9890.c This file implements and device_audio.h interfaces.

**Greybus Commands:**

```c
/* Mods Audio Commands */
#define GB_AUDIO_GET_VOLUME_DB_RANGE         0x02
#define GB_AUDIO_GET_SUPPORTED_USE_CASES   0x03
#define GB_AUDIO_SET_CAPTURE_USE_CASE           0x04
#define GB_AUDIO_SET_PLAYBACK_USE_CASE         0x05
#define GB_AUDIO_SET_VOLUME                                0x06
#define GB_AUDIO_SET_SYSTEM_VOLUME                0x07
#define GB_AUDIO_GET_SUPPORTED_DEVICES        0x08
#define GB_AUDIO_DEVICES_REPORT_EVENT           0x09
#define GB_AUDIO_ENABLE_DEVICES                    0x0a

/* I2S Management Commands */
#define GB_I2S_MGMT_TYPE_PROTOCOL_VERSION               0x01
#define GB_I2S_MGMT_TYPE_GET_SUPPORTED_CONFIGURATIONS   0x02
#define GB_I2S_MGMT_TYPE_SET_CONFIGURATION              0x03
#define GB_I2S_MGMT_TYPE_GET_PROCESSING_DELAY           0x05
#define GB_I2S_MGMT_TYPE_ACTIVATE_CPORT                 0x07
#define GB_I2S_MGMT_TYPE_DEACTIVATE_CPORT               0x08
#define GB_I2S_MGMT_TYPE_REPORT_EVENT                   0x09
#define GB_I2S_MGMT_TYPE_ACTIVATE_PORT                  0x0a
#define GB_I2S_MGMT_TYPE_DEACTIVATE_PORT                0x0b
#define GB_I2S_MGMT_TYPE_START                          0x0c
#define GB_I2S_MGMT_TYPE_STOP                           0x0d
```

**Macros:**

Define the supported input and output audio devices bit masks. Loudspeaker is the output device and Echo reference
Is the input device used by Moto Z’s dsp for echo cancellation during speakerphone voip and voice calls.

```c
#define TFA9890_SUPPORTED_OUT_DEVICES   DEV_AUDIO_DEVICE_OUT_LOUDSPEAKER
#define TFA9890_SUPPORTED_IN_DEVICES    DEV_AUDIO_DEVICE_IN_EC_REF
```

Define the supported playback and capture use cases bit masks

```c
#define TFA9890_SUPPORTED_PLAYBACK_USE_CASES (DEV_AUDIO_PLAYBACK_MUSIC_USE_CASE | \
                           DEV_AUDIO_PLAYBACK_VOICE_CALL_SPKR_USE_CASE | \
                           DEV_AUDIO_PLAYBACK_RINGTONE_USE_CASE | \
                           DEV_AUDIO_PLAYBACK_SONIFICATION_USE_CASE)
#define TFA9890_SUPPORTED_CAPTURE_USE_CASES  DEV_AUDIO_CAPTURE_DEFAULT_USE_CASE
```

**Methods Description:**
tfa9890_aud_dev_probe() - get gpio resources, set reset line low and initialize device drivers private structure.
tfa9890_aud_dev_open() - Initializes I2C interface and tfa9890 chip with initial/default registers.
tfa9890_aud_dev_get_supported_use_cases(): return supported use cases

```c
use_cases->playback_usecases = TFA9890_SUPPORTED_PLAYBACK_USE_CASES;
    use_cases->capture_usecases = TFA9890_SUPPORTED_CAPTURE_USE_CASES;
```

tfa9890_aud_dev_get_vol_db_range(): return support volume range, min is -12750 millibles with steps size is 50 millibles.

```c
/* 127.5 db */
    vol_range->min = -12750;
    /* 0.5 db steps */
    vol_range->step = 50;
```

tfa9890_aud_dev_get_supp_devices(): return supported devices

```c
devices->in_devices = TFA9890_SUPPORTED_IN_DEVICES;
    devices->out_devices = TFA9890_SUPPORTED_OUT_DEVICES;
```

tfa9890_aud_dev_enable_devices(): Input and output devices to be enabled/disabled. For tfa9890 as there is only one device that is supported, there is nothing to set up on the IC to enable routing to particular device. So simply save the bit masks, and when it is time to start playback check if the device is enabled.

```c
priv->out_enabled_devices = devices->out_devices;
```

tfa9890_aud_dev_set_volume(): Update the volume control register on the chip with the received volume step from Moto Z
tfa9890_aud_dev_set_sys_volume(): Update the AGC gains applied to the stream based on the attenuation applied by the Moto Z on the input stream and the current use case. AGC gains tuned per volume step are stored in the tfa9890_music_table_preset[], tfa9890_voice_table_preset[], and tfa9890_ringtone_table_preset[] tables defined in tfa9890_firmware.h file.
tfa9890_aud_dev_set_current_use_case(): Current use case type voice, ringer etc is sent by the Moto Z. Tfa9890 uses the use case and system volume information received from the Moto Z to update the AGC gains. AGC gains are stored in the tfa9890_music_table_preset[], tfa9890_voice_table_preset[], and tfa9890_ringtone_table_preset[] in tfa9890_firmware.h file.
tfa9890_aud_dev_close(): pull the audio enable gpio low to disable audio.

```
if (priv->en_gpio >= 0) {
        /* disable audio */
        gpio_set_value(priv->en_gpio, 0);
    }
```

**Device I2S interface Implementation:**
Device driver is implemented in nuttx/configs/hdk/muc/src/stm32_audio_tfa9890.c This file implements and device_i2s.h interfaces.

**Macros:**
Define sample rates, pcm format/bit per sample supported, I2S protocol type and clock edge on which frame changes level, and rx/tx data is latched.

```c
#define TFA9890_I2S_RATE_MASK    DEVICE_I2S_PCM_RATE_48000
#define TFA9890_I2S_PCM_FMT_MASK    DEVICE_I2S_PCM_FMT_16
#define TFA9890_I2S_PROTOCOL_MASK    DEVICE_I2S_PROTOCOL_I2S
#define TFA9890_I2S_WCLK_PALARITY_MASK    DEVICE_I2S_POLARITY_NORMAL
#define TFA9890_I2S_WCLK_EDGE_MASK    DEVICE_I2S_EDGE_RISING
#define TFA9890_I2S_RXCLK_EDGE_MASK    DEVICE_I2S_EDGE_RISING
#define TFA9890_I2S_TXCLK_EDGE_MASK    DEVICE_I2S_EDGE_FALLING
```

**Structures:**
Default I2S configuration for tfa9890, IC will operate in this config for all use cases.

```c
static const struct device_i2s_pcm tfa9890_i2s_pcm = {
    .rate       = TFA9890_I2S_RATE_MASK,
    .channels   = 2,
    .format     = TFA9890_I2S_PCM_FMT_MASK,
};

static const struct device_i2s_dai tfa9890_i2s_dai = {
    .protocol            = TFA9890_I2S_PROTOCOL_MASK,
    .wclk_polarity       = TFA9890_I2S_WCLK_PALARITY_MASK,
    .wclk_change_edge    = TFA9890_I2S_WCLK_EDGE_MASK,
    .data_tx_edge        = TFA9890_I2S_TXCLK_EDGE_MASK,
    .data_rx_edge        = TFA9890_I2S_RXCLK_EDGE_MASK,
};
```

**Methods Description:**

tfa9890_i2s_direct_op_get_caps(): return I2S DAI and pcm configurations defined for slave role. Tfa9890
Only supports slave role.

```
if (clk_role != DEVICE_I2S_ROLE_SLAVE)
        return -EINVAL;

    memcpy(i2s_dai, &tfa9890_i2s_dai, sizeof(struct device_i2s_dai));
    memcpy(i2s_pcm, &tfa9890_i2s_pcm, sizeof(struct device_i2s_pcm));
```

tfa9890_i2s_direct_op_set_config_masks(): Sanity check configurations bit masks received as only one bit per config mask should be set, and verify if the default configuration supported by tfa9890 is received. As only only default configuration is defined in supported configurations we don't need to update tfa9890 registers with different configurations, default register set up supports the default configuration.

```
/*
     * check if cfg is valid for now, as only one default
     * configuration is supported.
     */

    if (!ONE_BIT_IS_SET(i2s_dai->protocol) ||
          !ONE_BIT_IS_SET(i2s_dai->wclk_polarity) ||
          !ONE_BIT_IS_SET(i2s_dai->wclk_change_edge) ||
          !ONE_BIT_IS_SET(i2s_dai->data_rx_edge) ||
          !ONE_BIT_IS_SET(i2s_dai->data_tx_edge) ||
          !ONE_BIT_IS_SET(i2s_pcm->rate) ||
          !ONE_BIT_IS_SET(i2s_pcm->format)) {
         lldbg("ERROR: i2s configuration more than 1 bit set\n");
         return -EINVAL;
    }

    if (i2s_pcm->channels < 0 || i2s_pcm->channels > 2) {
         lldbg("ERROR:i2s channels configuration invalid\n");
         return -ERANGE;
    }

     /* Check that bit field settings match our capabilities */
    if (((i2s_dai->protocol & TFA9890_I2S_PROTOCOL_MASK) !=
                                              TFA9890_I2S_PROTOCOL_MASK)||
         ((i2s_dai->wclk_polarity & TFA9890_I2S_WCLK_PALARITY_MASK) !=
                                              TFA9890_I2S_WCLK_PALARITY_MASK) ||
         ((i2s_dai->wclk_change_edge & TFA9890_I2S_WCLK_EDGE_MASK) !=
                                              TFA9890_I2S_WCLK_EDGE_MASK) ||
         ((i2s_dai->data_rx_edge & TFA9890_I2S_RXCLK_EDGE_MASK) !=
                                              TFA9890_I2S_RXCLK_EDGE_MASK) ||
         ((i2s_dai->data_tx_edge & TFA9890_I2S_TXCLK_EDGE_MASK) !=
                                              TFA9890_I2S_TXCLK_EDGE_MASK) ||
         ((i2s_pcm->rate & TFA9890_I2S_RATE_MASK) !=
                                              TFA9890_I2S_RATE_MASK) ||
         ((i2s_pcm->format & TFA9890_I2S_PCM_FMT_MASK) !=
                                              TFA9890_I2S_PCM_FMT_MASK)) {
        lldbg("ERROR:failed matching tfa9890 capabilities\n");
        return -EINVAL;
    }

    if (clk_role != DEVICE_I2S_ROLE_SLAVE)
        return -EINVAL;
```

tfa9890_i2s_direct_op_start_receiver(): Start receiving playback stream, power up IC and load DSP firmware.
tfa9890_i2s_direct_op_stop_receiver(): Stop amplifier and Power down IC.
tfa9890_i2s_direct_op_start_transmitter(): tfa9890 loops back the output signal from the last stage after all the processing is done, no set up is needed
tfa9890_i2s_direct_op_stop_transmitter() : Nothing to do for tfa9890, Ec ref loopback stops when receiver stop happens.

#### Sequence Diagram: {#sequence-diagram-}

##### Message Sequence On Attach: {#message-sequence-on-attach-}

*(Diagram coming soon…)*

##### Mods Audio and I2S GB Message Sequence in audio session {#mods-audio-and-i2s-gb-message-sequence-in-audio-session}

*(Diagram coming soon…)*

#### Hardware Manifest {#hardware-manifest}

HDK will use audio bundle to support speaker card.
Manifest settings for speaker card is at nuttx/apps/greybus-utils/manifests/hdk-speaker.mnfs
Use base-powered.mnfs as base version and add audio bundle listed below to it,

```ini
; I2S MGMT on CPort 4
[cport-descriptor 4]
bundle = 3
protocol = 0x0a

; Mods audio on CPort 5
[cport-descriptor 5]
bundle = 3
protocol = 0xf0

; Audio related Bundle 3
[bundle-descriptor 3]
class = 0x0a
```

Also Update product string

```ini
; Interface product string (id can't be 0)
[string-descriptor 2]
string = MDK-MHB-SPEAKER
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
(hdk-speaker) manifest name
```

#### Building and Flashing Firmware {#building-and-flashing-firmware}

The new target supports all required functionality now. The firmware can be built and flashed into the Reference Moto Mod. Make sure that the Moto Mod is running in development mode as per [these instructions](index.md) or build and flash the development bootloader yourself as [documented here](../tools/build-from-source.md).

#### Test {#test}

Verify MDK-SPEAKER type Moto Mod is enumerated on the phone. Play music from any Android application to test speaker.

## Moto Mods Android Application {#application}

#### Audio card sample APK {#audio-card-sample-apk}

The Moto Audio card sample APK is an open source project, works as an downloadable Android app, to show the capability of Audio personality card.

#### Install APK {#install-apk}

Download and install the Audio card sample app - see [MDK Audio app (rebuilt from source; was on Google Play Store)](../../assets/apks/mdkaudio.apk)

#### Source code {#source-code}

The source code of the MDK Battery APK is published at <https://github.com/jksim/mdkaudio>.

To build the sample APK from source code, please download and install Android Studio from Android Developer Site, then import the [mdkaudio project](https://github.com/jksim/mdkaudio) into Android Studio. See [Developer Tools: Setup Your Development Environment](../tools/setup-environment.md) for more info.

#### Reference for ModManager interface & query Mod statues: {#reference-for-modmanager-interface-query-mod-statues-}

See [Hello World! documentation](hello-world.md#reference) for implementation of MotoMods interface creation and query.

#### Verify {#verify}

Attach Audio card to phone, then install and launch Audio card sample apk, play music or make a phone call to test speaker:

*(Screenshot coming soon...)*

## Downloads {#downloads}

This section contains the downloadable files associated with this example.

Before downloading, please read through the [Moto Mods Development Kit Terms & Conditions](../../legal/mdk-terms-and-conditions.md):

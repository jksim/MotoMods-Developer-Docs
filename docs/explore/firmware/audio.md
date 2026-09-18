---
title: "Moto Mods Firmware: Audio Protocol"
source_url: http://developer.motorola.com/explore/firmware/audio
source_capture: 2016 Squarespace portal
---

# Moto Mods Firmware: Audio Protocol

## Overview

The Moto Mods audio capability is enabled by the Audio bundle which is comprised of the I2S Management and the Mods Audio Greybus protocols.

This page is comprised of 2 key sections:

- [**Raw I2S Interface**](#raw-i2s-interface)
  - The [**I2S Management Protocol**](#i2s-management-protocol) is used to query and configure the I2S digital audio interface, and start, stop audio streaming on I2S.
  - The [**Mods Audio Protocol**](#mods-audio-protocol) allows the Moto Z to enable & disable audio devices supported by the Moto Mod (such as speaker, mic etc.) and control volume on the Moto Mod. It also allows the Moto Z to share current stream volume level and stream type info to allow the Moto Mod to provide optimized audio experience.
  - See the [**Usage**](#usage) section for the message flow diagrams of the Moto Z to Moto Mods communication.
- [**Moto High Speed Bridge Audio**](#moto-high-speed-bridge-audio)
  - When the Moto High Speed Bridge is in use you need to use Audio tunneling over that interface. See the Moto High Speed Bridge Audio section for implementation details for this functionality.

## Raw I2S Interface {#raw-i2s-interface}

### Hardware Manifest {#hardware-manifest}

```ini
; I2S MGMT Phy on CPort AA
[cport-descriptor AA]
bundle = BB
protocol = 0x0a

; Audio on CPort CC
[cport-descriptor CC]
bundle = BB
protocol = 0xf0

; Audio related Bundle BB
[bundle-descriptor BB]
class = 0x0a
```

**`AA`** is a unique integer (within your hardware manifest) defining which CPort is used for the I2S Management Interface.

**`CC`** is a unique integer (within your hardware manifest) defining which CPort is used for the audio Interface.

**`BB`** is a unique integer (within your hardware manifest) defining which Bundle the audio and I2S management CPort’s are a member of.

### Implementation {#implementation}

To enable the Raw I2S Interface, you must include both the [I2S Management Protocol](#i2s-management-protocol) and [Mods Audio Protocols](#mods-audio-protocol). The [Usage](#usage) section on this page shows the message sequence diagram of these working together.

Menuconfig options for Audio Protocol:

```
Device Driver Support
    Greybus Support
        [*] Mods I2S support
        [*] Mods Audio support
            [-] Use custom audio chip driver
```

### I2S Management Protocol {#i2s-management-protocol}

#### Files {#files}

**`nuttx/include/nuttx/device_i2s.h`**

> This file defines the `device_i2s_type_ops` structure and provides the glue to the Greybus I2S Management protocol.
> Bit Fields - Configuring the Digital Audio Format

Represents pcm format, number of bits per sample. Currently only 16, 24 bit (24 bits in 4 bytes) pcm format is supported:

```
DEVICE_I2S_PCM_FMT_8           BIT(0)
DEVICE_I2S_PCM_FMT_16          BIT(1)
DEVICE_I2S_PCM_FMT_24          BIT(2)
DEVICE_I2S_PCM_FMT_32          BIT(3)
DEVICE_I2S_PCM_FMT_64          BIT(4)
```

Represents different sampling rates. Currently only 8000, 16000, 48000, 96000 samples rates are supported:

```
DEVICE_I2S_PCM_RATE_5512       BIT(0)
DEVICE_I2S_PCM_RATE_8000       BIT(1)
DEVICE_I2S_PCM_RATE_11025      BIT(2)
DEVICE_I2S_PCM_RATE_16000      BIT(3)
DEVICE_I2S_PCM_RATE_22050      BIT(4)
DEVICE_I2S_PCM_RATE_32000      BIT(5)
DEVICE_I2S_PCM_RATE_44100      BIT(6)
DEVICE_I2S_PCM_RATE_48000      BIT(7)
DEVICE_I2S_PCM_RATE_64000      BIT(8)
DEVICE_I2S_PCM_RATE_88200      BIT(9)
DEVICE_I2S_PCM_RATE_96000      BIT(10)
DEVICE_I2S_PCM_RATE_176400     BIT(11)
DEVICE_I2S_PCM_RATE_192000     BIT(12)
```

Represents different I2S protocol standards, Currently only `DEVICE_I2S_ROTOCOL_I2S`, standard I2S is supported:

```
DEVICE_I2S_PROTOCOL_PCM        BIT(0)
DEVICE_I2S_PROTOCOL_I2S        BIT(1)
DEVICE_I2S_PROTOCOL_LR_STEREO  BIT(2)
```

Represents Clock role of the Moto Mod, Currently Moto Z always acts as the Master of the I2S bus:

```
DEVICE_I2S_ROLE_MASTER         BIT(0)
DEVICE_I2S_ROLE_SLAVE          BIT(1)
```

Represents Clock polarity of the frame synchronization line:

```
DEVICE_I2S_POLARITY_NORMAL     BIT(0)
DEVICE_I2S_POLARITY_REVERSED   BIT(1)
```

Represents clock edge on the data line, based on which data is latched in or out of the data line:

```
DEVICE_I2S_EDGE_RISING         BIT(0)
DEVICE_I2S_EDGE_FALLING        BIT(1)
```

---

#### Structures {#structures}

##### device_i2s_pcm: Defining the I2S PCM device {#device_i2s_pcm-defining-the-i2s-pcm-device}

```c
struct device_i2s_pcm {
    uint32_t    format;
    uint32_t    rate;
    uint8_t     channels;
};
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2">Parameters</td>
</tr>
</thead>
<tr>
<td><code>format</code></td>
<td>Bit field specifies number of bits used to represent one PCM Sample.</td>
</tr>
<tr>
<td><code>rate</code></td>
<td>Bit field specifies sample rate of the audio stream.</td>
</tr>
<tr>
<td><code>channels</code></td>
<td>Mono or stereo.</td>
</tr>
</table>
</div></div>

---

##### device_i2s_dai: Defining the I2S DAI device {#device_i2s_dai-defining-the-i2s-dai-device}

```c
struct device_i2s_dai {
    uint32_t    mclk_freq;          /* mclk frequency generated/required */
    uint8_t     protocol;           /* DEVICE_I2S_PROTOCOL_* */
    uint8_t     wclk_polarity;      /* DEVICE_I2S_POLARITY_* */
    uint8_t     wclk_change_edge;   /* DEVICE_I2S_EDGE_* */
    uint8_t     data_rx_edge;       /* DEVICE_I2S_EDGE_* */
    uint8_t     data_tx_edge;       /* DEVICE_I2S_EDGE_* */
};
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2">Parameters</td>
</tr>
</thead>
<tr>
<td><code>mclk_freq</code></td>
<td>Master clock frequency if external clock is used.</td>
</tr>
<tr>
<td><code>protocol</code></td>
<td>Bit field specifies type of I2S protocol used.</td>
</tr>
<tr>
<td><code>wclk_polarity</code></td>
<td>Clock polarity of frame synchronization.</td>
</tr>
<tr>
<td><code>wclk_change_edge</code></td>
<td>Specifies  bit clock edge (falling or rising) which triggers frame synchronization level change.</td>
</tr>
<tr>
<td><code>data_rx_edge</code></td>
<td>Bit Clock Edge (falling or rising) on which audio data is received.</td>
</tr>
<tr>
<td><code>data_tx_edge</code></td>
<td>Bit Clock Edge (falling or rising) on which audio data is transmitted.</td>
</tr>
</table>
</div></div>

---

#### Methods {#methods}

I2S management device driver must implement methods defined in struct `device_i2s_type_ops`.

##### start_receiver {#start_receiver}

```c
int (*start_receiver)(struct device *dev);
```

`start_receiver()` method is called to indicate start of the audio playback session. It is the first method that gets called when audio playback starts, driver should implement this method to startup and prepare I2S DAI before audio streaming starts.

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
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### start_transmitter {#start_transmitter}

`start_transmitter()` method is called to indicate start of the audio capture session. It is the first method that gets called when audio capture starts, driver should implement this method to startup and prepare I2S DAI before audio streaming starts.

```c
int (*start_transmitter)(struct device *dev);
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
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### get_caps {#get_caps}

`get_caps()` method should return all the supported PCM configurations and I2S digital audio interface bus configurations supported by Moto Mod for the specified clock role. It gets called on attaching to Moto Z.

```c
int (*get_caps)(struct device *dev, uint8_t clk_role,   struct device_i2s_pcm *pcm,
                struct device_i2s_dai *dai);
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
<td><code>clk_role</code></td>
<td>Master or Slave, specified by bit fields <code>DEVICE_I2S_ROLE_*</code>.</td>
</tr>
<tr>
<td><code>pcm</code></td>
<td>Driver should update DAI structure with supported I2S bus configurations, protocol, clock polarity and clock edge bit masks.</td>
</tr>
<tr>
<td><code>dai</code></td>
<td>Matches dev passed to the probe function.</td>
</tr>
<thead>
<tr>
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### set_config {#set_config}

`set_config()` specifies pcm and I2S DAI configuration used for the audio stream.

```c
int (*set_config)(struct device *dev, uint8_t clk_role,
                      struct device_i2s_pcm *pcm, struct device_i2s_dai *dai);
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
<td><code>clk_role</code></td>
<td>Master or Slave, specified by bit fields <code>DEVICE_I2S_ROLE_*</code>.</td>
</tr>
<tr>
<td><code>pcm</code></td>
<td>pcm configuration that Moto Z is using for the audio stream, Moto Z will pick one of the combinations of pcm configuration it received from Moto Mod using <code>get_caps()</code> method. Only one bit field per parameter is set to indicate sampling rate, format etc.</td>
</tr>
<tr>
<td><code>dai</code></td>
<td>I2S bus configuration that Moto Z is using for the DAI, Moto Z will pick one of the combinations of I2S DAI configuration it received from Moto Mod using <code>get_caps()</code> method. Only one bit field is set to indicate protocol type, clock polarity and clock edge used for latching data.</td>
</tr>
<thead>
<tr>
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### start_receiver_port {#start_receiver_port}

This method gets called to indicate I2S DAI is activated by Moto Z, frame sync, and bit clock are activated and pcm data is latched on data line.

```c
int (*start_receiver_port)(struct device *dev)
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
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### stop_receiver_port {#stop_receiver_port}

This method gets called to indicate I2S DAI is deactivated by Moto Z, frame sync, and bit clock are stopped, and audio stops streaming.

```c
int (*stop_receiver_port)(struct device *dev)
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
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### start_transmitter_port {#start_transmitter_port}

This method gets called to indicate I2S DAI is activated by Moto Z, frame sync, and bit clock are activated and Moto Z expects Moto Mod to start sending pcm data on data line.

```c
int (*start_transmitter_port)(struct device *dev)
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
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### stop_transmitter_port {#stop_transmitter_port}

This method gets called to indicate I2S DAI is deactivated by Moto Z, frame sync, and bit clock are stopped, and audio stops streaming.

```c
int (*stop_transmitter_port)(struct device *dev)
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
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### register_callback {#register_callback}

I2S management Greybus protocol implementation will call this method register a callback method, that the driver can call to notify Moto Z of any I2S DAI events and failures

```c
int (*register_callback)(struct device *dev, device_i2s_notification_callback cb)
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
<td><code>cb</code></td>
<td>Callback method that driver can use to notify Moto Z of any events.</td>
</tr>
<thead>
<tr>
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### unregister_callback {#unregister_callback}

I2S management Greybus protocol implementation will call this method to unregister callback

```c
int (*unregister_callback)(struct device *dev)
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
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

#### Callbacks {#callbacks}

##### device_i2s_notification_callback {#device_i2s_notification_callback}

Callback method that the driver can call to notify Moto Z of any I2S DAI events and errors.

```c
int (*device_i2s_notification_callback)(struct device *dev, enum device_i2s_event event);
```

## Mods Audio Protocol {#mods-audio-protocol}

### Files

**`nuttx/include/nuttx/device_audio.h`**

> This file defines the `device_aud_dev_type_ops` structure and provides the glue to the Greybus Audio channel.

### Bit Fields {#bit-fields}

##### Audio Playback {#audio-playback}

Use cases for audio playback:

- **`DEV_AUDIO_PLAYBACK_NONE_USE_CASE`**: Default use case, Moto Mod can apply default tuning for this use case.
- **`DEV_AUDIO_PLAYBACK_MUSIC_USE_CASE`**: Music use case typically set while playing audio from music players.
- **`DEV_AUDIO_PLAYBACK_VOICE_CALL_SPKR_USE_CASE`**: Voice/voip call speaker phone use case.
- **`DEV_AUDIO_PLAYBACK_RINGTONE_USE_CASE`**: use case for playing ringtones
- **`DEV_AUDIO_PLAYBACK_SONIFICATION_USE_CASE`**: use case for Notifications and system sounds.

Bit field definition for audio playback:

```
DEV_AUDIO_PLAYBACK_NONE_USE_CASE              BIT(0)
DEV_AUDIO_PLAYBACK_MUSIC_USE_CASE             BIT(1)
DEV_AUDIO_PLAYBACK_VOICE_CALL_SPKR_USE_CASE   BIT(2)
DEV_AUDIO_PLAYBACK_RINGTONE_USE_CASE          BIT(3)
DEV_AUDIO_PLAYBACK_SONIFICATION_USE_CASE      BIT(4)
```

---

##### Audio Capture {#audio-capture}

Use cases for audio capture:

- **`DEV_AUDIO_CAPTURE_DEFAULT_USE_CASE`**: default capture case, Moto Mod can apply default tuning to optimize this device.
- **`DEV_AUDIO_CAPTURE_VOICE_USE_CASE`**: voice/voip calls use case.
- **`DEV_AUDIO_CAPTURE_RAW_USE_CASE`**: no processing applied on the input stream.
- **`DEV_AUDIO_CAPTURE_CAMCORDER_USE_CASE`**: camcorder capture use case.

Bit field definition for audio capture:

```
DEV_AUDIO_CAPTURE_DEFAULT_USE_CASE    BIT(0)
DEV_AUDIO_CAPTURE_VOICE_USE_CASE      BIT(1)
DEV_AUDIO_CAPTURE_RAW_USE_CASE        BIT(2)
DEV_AUDIO_CAPTURE_CAMCORDER_USE_CASE  BIT(3)
```

---

##### Audio Output Device Type {#audio-output-device-type}

Audio output devices:

- **`DEV_AUDIO_DEVICE_OUT_LOUDSPEAKER`**: Loudspeaker
- **`DEV_AUDIO_DEVICE_OUT_HEADSET`**: headset
- **`DEV_AUDIO_DEVICE_OUT_LINE`**: auxiliary output devices such as car stereo and audio docks.
- **`DEV_AUDIO_DEVICE_OUT_HDMI`**: hdmi
- **`DEV_AUDIO_DEVICE_OUT_EARPIECE`**: earpiece used for voice calls only

Bit field definition for audio output devices:

```
DEV_AUDIO_DEVICE_OUT_LOUDSPEAKER     BIT(0)
DEV_AUDIO_DEVICE_OUT_HEADSET         BIT(1)
DEV_AUDIO_DEVICE_OUT_LINE            BIT(2)
DEV_AUDIO_DEVICE_OUT_HDMI            BIT(3)
DEV_AUDIO_DEVICE_OUT_EARPIECE        BIT(4)
```

---

##### Audio Input Device Type {#audio-input-device-type}

Audio input devices:

- **`DEV_AUDIO_DEVICE_IN_MIC`**: Default mic
- **`DEV_AUDIO_DEVICE_IN_HEADSET_MIC`**: mic on the headset
- **`DEV_AUDIO_DEVICE_IN_CAMCORDER_MIC`**: mic optimized for camcorder capture.
- **`DEV_AUDIO_DEVICE_IN_EC_REF`**: Echo reference device, this device loops back the output signal to the Moto Z, so that the Moto Z DSP can use it for for use cases which need echo cancellation. If a use case (such as Voice call speaker phone) needs a echo reference input and Moto Mod does not support `DEV_AUDIO_DEVICE_IN_MIC_EC` device, Moto Z will use `DEV_AUDIO_DEVICE_IN_EC_REF` instead if available so that Moto Z dsp can do echo cancellation. If neither `DEV_AUDIO_DEVICE_IN_MIC_EC` and `DEV_AUDIO_DEVICE_IN_EC_REF` are supported Moto Z will fallback to using internal device.
- **`DEV_AUDIO_DEVICE_IN_FM_TUNER`**: FM device.
- **`DEV_AUDIO_DEVICE_IN_MIC_EC`**: mic which supports echo cancellation, will be used for use cases which need echo cancelled input stream. If a use case demands this device and moto mod does not support it, Moto Z will fallback to the internal device.
- **`DEV_AUDIO_DEVICE_IN_MIC_ECNS`**: mic which supports echo cancellation and noise suppression, will be used for use cases which need echo cancelled and noise suppressed input stream. If a use case demands this device and moto mod does not support it, Moto Z will fallback to the internal device.
- **`DEV_AUDIO_DEVICE_IN_MIC_NS`**: mic which supports noise suppression, will be used for use cases which need noise suppressed input stream. If a use case demands this device and moto mod does not support it, Moto Z will fallback to the internal device.

Bit field definition for audio input devices:

```
DEV_AUDIO_DEVICE_IN_MIC            BIT(0)
DEV_AUDIO_DEVICE_IN_HEADSET_MIC    BIT(1)
DEV_AUDIO_DEVICE_IN_CAMCORDER_MIC  BIT(2)
DEV_AUDIO_DEVICE_IN_EC_REF         BIT(3)
DEV_AUDIO_DEVICE_IN_FM_TUNER       BIT(4)
DEV_AUDIO_DEVICE_IN_MIC_EC         BIT(5)
DEV_AUDIO_DEVICE_IN_MIC_ECNS       BIT(6)
DEV_AUDIO_DEVICE_IN_MIC_NS         BIT(7)
```

---

##### Speaker EQ Presets {#speaker-eq-presets}

Speaker EQ presets for bass enhancement:

- Mod can request Moto Z to apply pre defined bass enhancements EQ filters to to the playback stream over a loudspeaker device.
- **`DEV_AUDIO_SPEAKER_PRESET_EQ_NONE`**: No bass enhancement EQ applied.
- **`DEV_AUDIO_SPEAKER_PRESET_EQ_SMALL`**: EQ and bass enhancement optimized to boost an approximate frequency range of 400Hz - 800Hz.
- **`DEV_AUDIO_SPEAKER_PRESET_EQ_MEDIUM`**: EQ and bass enhancement optimized to boost an approximate frequency range of 150Hz - 300Hz.
- **`DEV_AUDIO_SPEAKER_PRESET_EQ_LARGE`**: EQ and bass enhancement optimized to boost a frequency range below 150Hz.

Definition for Speaker EQ presets:

```
DEV_AUDIO_SPEAKER_PRESET_EQ_NONE     0
DEV_AUDIO_SPEAKER_PRESET_EQ_SMALL    1
DEV_AUDIO_SPEAKER_PRESET_EQ_MEDIUM   2
DEV_AUDIO_SPEAKER_PRESET_EQ_LARGE    3
```

---

#### Structures

##### device_aud_vol_range: Volume Level Configuration {#device_aud_vol_range-volume-level-configuration}

```c
struct device_aud_vol_range {
    int min;
    int step;
};
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
<td><code>event</code></td>
<td>I2S event.</td>
</tr>
<thead>
<tr>
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### device_aud_devices: Audio Device Type Configuration {#device_aud_devices-audio-device-type-configuration}

```c
struct device_aud_devices {
    uint32_t in_devices;
    uint32_t out_devices;
};
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2">Parameters</td>
</tr>
</thead>
<tr>
<td><code>min</code></td>
<td>Specifies minimum volume level supported by Moto Mod in millibels (DB *100).</td>
</tr>
<tr>
<td><code>step</code></td>
<td>Specifies minimum resolution of volume level change per step supported in millibels.</td>
</tr>
</table>
</div></div>

---

##### device_aud_usecases: Audio Use Case Configuration {#device_aud_usecases-audio-use-case-configuration}

```c
struct device_aud_usecases {
    uint32_t playback_usecases;
    uint32_t capture_usecases;
};
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2">Parameters</td>
</tr>
</thead>
<tr>
<td><code>in_devices</code></td>
<td>Bit Field specifies input device types.</td>
</tr>
<tr>
<td><code>out_device</code></td>
<td>Bit Field specifies output device types.</td>
</tr>
</table>
</div></div>

---

#### Audio Format Configuration {#audio-format-configuration}

##### device_aud_pcm_config {#device_aud_pcm_config}

```c
struct device_aud_pcm_config {
    uint32_t    format;     /* DEVICE_I2S_PCM_FMT_* */
    uint32_t    rate;       /* DEVICE_I2S_PCM_RATE_* */
    uint8_t     channels;
};
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2">Parameters</td>
</tr>
</thead>
<tr>
<td><code>format</code></td>
<td>Bit field specifies type of I2S PCM format.</td>
</tr>
<tr>
<td><code>rate</code></td>
<td>Bit field specifies type of I2S PCM bitrate.</td>
</tr>
<tr>
<td><code>channels</code></td>
<td>Specifies number of channels.</td>
</tr>
</table>
</div></div>

---

##### device_aud_i2s_config {#device_aud_i2s_config}

```c
struct device_aud_i2s_config {
    uint32_t    mclk_freq;          /* mclk frequency generated/required */
    uint8_t     protocol;           /* DEVICE_I2S_PROTOCOL_* */
    uint8_t     wclk_polarity;      /* DEVICE_I2S_POLARITY_* */
    uint8_t     wclk_change_edge;   /* DEVICE_I2S_EDGE_* */
    uint8_t     data_rx_edge;       /* DEVICE_I2S_EDGE_* */
    uint8_t     data_tx_edge;       /* DEVICE_I2S_EDGE_* */
};
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2">Parameters</td>
</tr>
</thead>
<tr>
<td><code>mclk_freq</code></td>
<td>Master clock frequency if external clock is used.</td>
</tr>
<tr>
<td><code>protocol</code></td>
<td>Bit field specifies type of I2S protocol used.</td>
</tr>
<tr>
<td><code>wclk_polarity</code></td>
<td>Clock polarity of frame synchronization.</td>
</tr>
<tr>
<td><code>wclk_change_edge</code></td>
<td>Specifies  bit clock edge (falling or rising) which triggers frame synchronization level change.</td>
</tr>
<tr>
<td><code>data_rx_edge</code></td>
<td>Bit Clock Edge (falling or rising) on which audio data is received.</td>
</tr>
<tr>
<td><code>data_tx_edge</code></td>
<td>Bit Clock Edge (falling or rising) on which audio data is transmitted.</td>
</tr>
</table>
</div></div>

---

##### device_aud_dai_config {#device_aud_dai_config}

```c
typedef enum {
    DEVICE_AUDIO_DAI_I2S_TYPE,
} device_audio_dai_type;

struct device_aud_dai_config {
    device_audio_dai_type dai_type;
    union dai_config {
        struct device_aud_i2s_config i2s_dai;
    } config;
};
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2">Parameters</td>
</tr>
</thead>
<tr>
<td><code>device_audio_dai_type</code></td>
<td>Digital Audio Interface type used by audio peripheral.</td>
</tr>
<tr>
<td><code>dai_config</code></td>
<td>Specifies digital audio interface  configuration parameters.</td>
</tr>
</table>
</div></div>

#### Methods

Audio device driver must implement methods defined in `struct device_aud_dev_type_ops` in file `device_audio.h`.

##### get_volume_mb_range {#get_volume_mb_range}

This method is called to query the min volume level in millibels (decibels *100) and the step resolution that the audio class supports on the Moto Mod.

```c
int (*get_volume_mb_range)(struct device *dev,  struct device_aud_vol_range *vol_range)
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2">Parameters</td>
</tr>
</thead>
<tr>
<td><code>device_audio_dai_type</code></td>
<td>Matches dev passed to the probe function.</td>
</tr>
<tr>
<td><code>dai_config</code></td>
<td>Driver should provide minimum vol level and step resolution.</td>
</tr>
<thead>
<tr>
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### get_supported_use_cases {#get_supported_use_cases}

This method will be used to query supported use cases for playback and capture, for which the Moto Mod can provide optimized experience. Moto Z may decide to route a use case to Moto Mod based on the use cases that Moto Mod supports.

```c
int (*get_supported_use_cases)(struct device *dev,  struct device_aud_usecases *use_cases);
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
<td><code>use_cases</code></td>
<td>Driver should provide supported playback and capture use cases, see <code>DEV_AUDIO_PLAYBACK_*</code> and <code>DEV_AUDIO_CAPTURE_*</code> in bit fields.</td>
</tr>
<thead>
<tr>
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>
rld!

---

##### set_current_playback_use_case {#set_current_playback_use_case}

Moto Z will send the use case of the active audio stream, Moto Mod can use this info to optimize audio experience for the particular use case.

```c
int (*set_current_playback_use_case)(struct device *dev, uint32_t use_case)
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
<td><code>use_case</code></td>
<td>Use case of the active audio stream.</td>
</tr>
<thead>
<tr>
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### set_current_capture_use_case {#set_current_capture_use_case}

Moto Z will send the use case of the active capture stream, Moto Mod can use this info to optimize audio experience for the particular use case.

```c
int (*set_current_capture_use_case)(struct device *dev, uint32_t use_case)
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
<td><code>use_case</code></td>
<td>Use case of the active audio stream.</td>
</tr>
<thead>
<tr>
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### set_volume {#set_volume}

Method will be called to set volume level of playback stream, driver will calculate the volume level using this expression (`vol_step*` increment per volume step + `min_vol`). Volume step value of 0 represents mute. For example: `min_vol = -6450 mb`, increment per `volume step = 50 mb`, `volume step = 6`, `volume level = -6150`.

```c
int (*set_volume)(struct device *dev, uint32_t vol_step)
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
<td><code>vol_step</code></td>
<td>Volume step.</td>
</tr>
<thead>
<tr>
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### set_sys_volume {#set_sys_volume}

```c
int (*set_sys_volume)(struct device *dev, int vol_mb)
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
<td><code>vol_mb</code></td>
<td>Volume level/attenuation  applied by Moto Z to the stream.</td>
</tr>
<thead>
<tr>
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### get_supp_devices {#get_supp_devices}

This method will be used to query the supported input and output devices by Moto Mod. See `DEV_AUDIO_DEVICE_OUT_*`, `DEV_AUDIO_DEVICE_IN_*` in bit fields section.

```c
int (*get_supp_devices)(struct device *dev, struct device_aud_devices  *devices)
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
<td><code>devices</code></td>
<td>Bit masks of supported audio devices, input and output.</td>
</tr>
<thead>
<tr>
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### enable_devices {#enable_devices}

Moto Z will select input and output devices needed for current active use cases. Multiple input and output devices may be selected based on the use case.

```c
int (*enable_devices)(struct device *dev, struct device_aud_devices  *devices)
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
<td><code>devices</code></td>
<td>Bit masks of selected audio devices, input and output</td>
</tr>
<thead>
<tr>
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### get_supp_config {#get_supp_config}

This method implementation is optional, will be called from I2S DAI device driver not from audio Greybus channel, if the I2S DAI and the audio device driver have different set of supported pcm and DAI configurations, I2S DAI device driver will query audio device driver interface for the supported configurations and send common set of configurations, over I2S mangement Greybus channel to the Moto Z.

```c
int (*get_supp_config)(struct device *dev, struct device_aud_pcm_config *pcm,
                           struct device_aud_dai_config *dai)
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
<td><code>pcm</code></td>
<td>Driver should update the pcm structure with supported sampling rate, format and channels bit masks.</td>
</tr>
<tr>
<td><code>dai</code></td>
<td>Driver should update DAI structure with supported bus configurations for the specified DAI type, for I2S case protocol, clock polarity and clock edge bit masks.</td>
</tr>
<thead>
<tr>
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### set_config

This method implementation is optional, will be called from I2S DAI device driver not from audio Greybus channel, if the I2S DAI and the audio device driver have different set of supported pcm and DAI configurations, I2S DAI device driver will set the pcm and DAI configurations using this method.

```c
int (*set_config)(struct device *dev, struct device_aud_pcm_config *pcm,
                                                struct device_aud_dai_config *dai)
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
<td><code>pcm</code></td>
<td>pcm configuration that Moto Z is using for the audio stream, Moto Z will pick one of the combinations of pcm configuration it received from Moto Mod using <code>get_supp_config()</code> method. Only one bit field per parameter  is set to indicate sampling rate, format.</td>
</tr>
<tr>
<td><code>dai</code></td>
<td>configuration that Moto Z is using for the DAI, Moto Z will pick one of the combinations of DAI configuration it received from Moto Mod using <code>get_supp_config()</code> method.</td>
</tr>
<thead>
<tr>
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### rx_dai_start {#rx_dai_start}

Method is called by DAI device driver to start receiver audio device driver interface, This will allow audio device driver and DAI driver to startup in sync.

```c
int (*rx_dai_start)(struct device *dev)
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
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### tx_dai_start {#tx_dai_start}

Method is called by DAI device driver to start transmitter audio device driver interface, This will allow audio device driver and DAI driver to startup in sync.

```c
int (*tx_dai_start)(struct device *dev)
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
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### rx_dai_stop {#rx_dai_stop}

Method is called by DAI device driver to stop receiver audio device driver interface, This will allow audio device driver and DAI driver to stop in sync.

```c
int (*rx_dai_stop)(struct device *dev)
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
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### tx_dai_stop {#tx_dai_stop}

Method is called by DAI device driver to stop transmitter audio device driver interface, This will allow audio device driver and DAI driver to stop in sync.

```c
int (*tx_dai_stop)(struct device *dev)
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
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

##### get_spkr_preset_eq {#get_spkr_preset_eq}

This method will be used to query if the Moto Mod needs a predefined bass enhancement EQ filters applied to the input stream for playback back over loudspeaker.

```c
int (*get_spkr_preset_eq)(struct device *dev, int *preset_eq)
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
<td><code>preset_eq</code></td>
<td>Bass enhancement EQ preset <code>DEV_AUDIO_SPEAKER_PRESET_EQ_*</code> (See bit fields section for description of different eq’s).</td>
</tr>
<thead>
<tr>
<td colspan="2">Returns</td>
</tr>
</thead>
<tr>
<td><code>int</code></td>
<td>0 on success, negative errno on error.</td>
</tr>
</table>
</div></div>

---

#### Callbacks

##### report_devices {#report_devices}

The device driver uses this callback to signal changes in currently available input and output devices to the Moto Z. Hotplug detection of Moto Mod-based peripherals such as headset are managed through this callback.

```c
void (*report_devices)(struct device *dev, struct device_aud_devices *devices);
```

### Usage {#usage}

#### Call Flow Diagrams {#call-flow-diagrams}

`GB_I2S_*` messages on I2S Greybus protocol, `GB_AUDIO_*` messages on Mods Audio Greybus protocol. Messages with double arrows indicate Greybus messages from AP that expect mod’s response synchronously.

##### Expected Message Sequence On Attach: {#expected-message-sequence-on-attach-}

*(Not preserved: `fwaudio-diagram-1.png` was not captured by the Wayback Machine and no copy survives.)*

---

##### Mods Audio and I2S GB Message Sequence On Audio Session Start: {#mods-audio-and-i2s-gb-message-sequence-on-audio-session-start-}

*(Not preserved: `fwaudio-diagram-2.png` was not captured by the Wayback Machine and no copy survives.)*

---

#### Example {#example}

See the **Audio Personality Card [LINK]** for an end-to-end example of a Moto Mods audio device.

## Moto High Speed Bridge Audio {#moto-high-speed-bridge-audio}

### Introduction {#introduction}

If a Moto Mod uses the Moto High Speed Bridge, only `device_audio.h` interface needs to be implemented and the generic motorola high speed I2S driver will configure the I2S digital audio interface. The information below provides the specific configuration of the Mods Audio Protocol to enable audio over the Moto High Speed Bridge.

### Hardware Manifest

```ini
; Audio on CPort CC
[cport-descriptor CC]
bundle = BB
protocol = 0xf0

; Audio related Bundle BB
[bundle-descriptor BB]
class = 0xf0
```

**`CC`** is a unique integer (within your hardware manifest) defining which CPort is used for the audio Interface.

**`BB`** is a unique integer (within your hardware manifest) defining which Bundle the audio and I2S management CPort’s are a member of.

### Files

**`nuttx/drivers/mhb/mhb_i2s_audio.c`**

> This file implements `device_i2s.h` and provides a generic driver to be able to configure, start and stop I2S stream.

**`nuttx/drivers/greybus/audio_dummy.c`**

> This file provides a dummy device driver that implements `device_audio.h` interface methods, that can be used as a starting point for writing a device driver to enable motorola high speed bridge audio.

### MHB I2S driver details {#mhb-i2s-driver-details}

#### Structures

##### device_i2s_pcm: Defining I2S PCM Configuration {#device_i2s_pcm-defining-i2s-pcm-configuration}

```c
static const struct device_i2s_pcm tsb_i2s_pcm = {
    .rate = (DEVICE_I2S_PCM_RATE_16000 | DEVICE_I2S_PCM_RATE_48000),
    .format = DEVICE_I2S_PCM_FMT_16 | DEVICE_I2S_PCM_FMT_24,
    .channels = 2,
};
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2">Parameters</td>
</tr>
</thead>
<tr>
<td><code>format</code></td>
<td>I2S High Speed Bridge Audio supports 16 and 24 bit pcm format</td>
</tr>
<tr>
<td><code>rate</code></td>
<td>I2S High Speed Bridge Audio supports 16k and 48k sampling rate.</td>
</tr>
<tr>
<td><code>channels</code></td>
<td>I2S High Speed Bridge Audio supports stereo up to two channels</td>
</tr>
</table>
</div></div>

---

##### device_i2s_dai: Defining I2S DAI Configuration {#device_i2s_dai-defining-i2s-dai-configuration}

```c
static const struct device_i2s_dai tsb_i2s_dai = {
    .protocol = DEVICE_I2S_PROTOCOL_I2S | DEVICE_I2S_PROTOCOL_LR_STEREO,
    .wclk_change_edge = DEVICE_I2S_EDGE_FALLING | DEVICE_I2S_EDGE_RISING,
    .data_rx_edge = DEVICE_I2S_EDGE_RISING,
    .data_tx_edge = DEVICE_I2S_EDGE_FALLING,
    .wclk_polarity = DEVICE_I2S_POLARITY_NORMAL | DEVICE_I2S_POLARITY_REVERSED,
};
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td colspan="2">Parameters</td>
</tr>
</thead>
<tr>
<td><code>mclk_freq</code></td>
<td>Master clock frequency if external clock is used.</td>
</tr>
<tr>
<td><code>protocol</code></td>
<td>I2S High Speed Bridge Audio supports, standard I2S protocol and I2S LR stereo protocol.</td>
</tr>
<tr>
<td><code>wclk_polarity</code></td>
<td>I2S High Speed Bridge Audio supports both normal and reversed clock polarity.</td>
</tr>
<tr>
<td><code>wclk_change_edge</code></td>
<td>I2S High Speed Bridge Audio supports falling and rising edge.</td>
</tr>
<tr>
<td><code>data_rx_edge</code></td>
<td>I2S High Speed Bridge Audio uses rising edge for receiving data.</td>
</tr>
<tr>
<td><code>data_tx_edge</code></td>
<td>I2S High Speed Bridge Audio uses falling edge for transmitting data.</td>
</tr>
</table>
</div></div>

---

#### Methods

MHB I2S driver implements device I2S interface methods defined in `device_i2s_type_ops`. These methods wrap higher level protocol methods detailed above.

##### mhb_i2s_op_get_capabilties() {#mhb_i2s_op_get_capabilties-}

- Implements `int (*get_caps)()` method, returns configurations set supported by both Moto High Speed Bridge I2S interface and the .audio device driver.
- Calls `int (*get_supp_config)()` device audio interface method.

##### mhb_i2s_op_set_config() {#mhb_i2s_op_set_config-}

- Implements `int (*set_config)()` method, configures Moto High Speed Bridge I2S interface and the audio device driver.
- Calls `int (*set_config)()` device audio interface method.

##### mhb_i2s_op_start_tx_stream() {#mhb_i2s_op_start_tx_stream-}

- Implements `int (*start_transmitter_port)()` method, starts Moto High Speed Bridge and audio device driver to start transmitting audio stream.
- Calls `int (*tx_dai_start)()` device audio interface method.

##### mhb_i2s_op_start_rx_stream() {#mhb_i2s_op_start_rx_stream-}

- Implements `int (*start_receiver_port)()` method, starts Moto High Speed Bridge and audio device driver to start receiving audio stream.
- Calls `int (*rx_dai_start)()` device audio interface method.

##### mhb_i2s_op_stop_rx_stream() {#mhb_i2s_op_stop_rx_stream-}

- Implements `int (*stop_transmitter_port)()` method, Stops Moto High Speed Bridge audio and audio device driver to start receiving.
- Calls `int (*tx_dai_start)()` device audio interface method.

##### mhb_i2s_op_stop_tx_stream() {#mhb_i2s_op_stop_tx_stream-}

- Implements `int (*stop_transmitter_port)()` method.
- Stops Moto High Speed Bridge audio and audio device driver to stop transmitting.
- Calls int `(*tx_dai_stop)()` device audio interface method.

##### mhb_i2s_op_register_cb() {#mhb_i2s_op_register_cb-}

- Registers callback to notify Moto z with with any I2S events.

##### mhb_i2s_op_unregister_cb() {#mhb_i2s_op_unregister_cb-}

- De-registers callback.

##### mhb_i2s_op_start_tx() {#mhb_i2s_op_start_tx-}

- Implements `int (*start_transmitter)()` method.
- Turns on Moto High Speed Bridge if it is not only already on and connected.

##### mhb_i2s_op_start_rx() {#mhb_i2s_op_start_rx-}

- Implements `int (*start_receiver)()` method.
- Turns on Moto High Speed Bridge if it is not only already on and connected.

##### mhb_i2s_op_stop_tx() {#mhb_i2s_op_stop_tx-}

- Implements `int (*stop_transmitter)()` method.
- Turns off Moto High Speed Bridge to save power if no rx session is active.

##### mhb_i2s_op_stop_rx() {#mhb_i2s_op_stop_rx-}

- Implements `int (*stop_transmitter)()` method.
- Turns off Moto High Speed Bridge to save power if no tx session is active.

---

#### Implementation Steps {#implementation-steps}

This section provides an example of a specific implementation of the Moto Mods Audio Protocol to enable the Moto High Speed Bridge.

##### Step 1) Configuring the Build Environment {#step-1-configuring-the-build-environment}

Menuconfig options for Moto High Speed Bridge Audio support:

```
Device Driver Support
    [*] Mods High-Speed Bus (MHB) driver support
        [*] MHB I2S Audio
```

---

##### Step 2) Adding the MHB device {#step-2-adding-the-mhb-device}

Add below MHB devices to `devices[]` list in `stm32_boot.c` file along with the device needed to implement the interface.

###### Slave power control device {#slave-power-control-device}

Slave power control device, needed by MHB I2S driver get the Moto High Speed Bridge connection status:

```
{
.type = DEVICE_TYPE_SLAVE_PWRCTRL_HW,
.name = "slave_pwrctrl",
.desc = "slave power control",
        .id   = MHB_ADDR_I2S,
},
```

###### MHB I2S device {#mhb-i2s-device}

MHB I2S device, opened by MHB I2S driver:

```
{
    .type = DEVICE_TYPE_I2S_HW,
    .name = "mhb_i2s_audio",
    .desc = "MHB I2S Driver",
    .id   = 1,
},
```

---

##### Step 3) Implement {#step-3-implement}

Moto Mod needs to implements below interface methods defined in `device_audio.h` to be able to use Moto High Speed Bridge Audio.

The following interface methods must be implemented as defined in the previous **Mods Audio Protocol > Methods section [LINK]**. These methods will be called by MHB I2S driver to configure, start and stop rx/tx streams.

```c
int (*get_supp_config)(struct device *dev, struct device_aud_pcm_config *pcm,
                  struct device_aud_dai_config *dai);
int (*set_config)(struct device *dev, struct device_aud_pcm_config *pcm,
                  struct device_aud_dai_config *dai);
int (*rx_dai_start)(struct device *dev);
int (*tx_dai_start)(struct device *dev);
int (*rx_dai_stop)(struct device *dev);
int (*tx_dai_stop)(struct device *dev);
```

**As an example, an audio dummy device is included in the code. See below for the documentation.**

Add this audio device to enable the audio dummy device driver, to be opened by the Mods Audio Greybus driver:

```c
#ifdef CONFIG_GREYBUS_MODS_AUDIO_DUMMY
    {
        .type = DEVICE_TYPE_MUC_AUD_HW,
        .name = "Audio_Device_Null_Driver",
        .desc = "Audio Device NUll Driver",
        .id   = 2,
    },
#endif
```

Add this audio device (with device id `DEVICE_AUDIO_MHB_ID`) to enable the audio dummy device driver, to be opened by the MHB I2S driver:

```c
#ifdef CONFIG_GREYBUS_MODS_AUDIO_DUMMY
    {
        .type = DEVICE_TYPE_MUC_AUD_HW,
        .name = "Audio_Device_Null_Driver",
        .desc = "Audio Device NUll Driver",
        .id   = DEVICE_AUDIO_MHB_ID,
    },
#endif
```

[< Previous Page
**Power Transfer Protocol**](power-transfer.md)

[Next Page >
**HID Protocol**](hid.md)

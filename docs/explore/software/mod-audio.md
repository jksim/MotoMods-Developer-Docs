---
title: "Moto Z Software: Mod Audio"
source_url: http://developer.motorola.com/explore/software/mod-audio
source_capture: 2016 Squarespace portal
---

# Moto Z Software: Mod Audio

## Audio Moto Mods {#audio-moto-mods}

The Moto Mod Audio-Ext protocol provides a means to fully integrate Moto Mod audio peripherals into Android’s audio framework.

The implementation of audio Moto Mod support has several considerations:

- Flexibility to enable novel or unexpected third-party applications
- Simplicity to provide a low barrier to entry for developers
- Maintainability to allow rapid Android version updates
- Compatibility to behave sensibly with existing Android audio interfaces

Compatibility and maintainability are achieved by conforming to Android’s core audio interfaces. Moto Mod audio devices adhere to the audio device types defined by Android so existing audio APIs and routing rules behave the same for Moto Mod audio devices as they do for any other compliant audio device. A Moto Mod can supersede an audio device built into the Moto Z (e.g. `DEVICE_OUT_EARPIECE`) or add a device that might not exist on the Moto Z (e.g. `DEVICE_OUT_WIRED_HEADPHONE`).

The Android audio devices that may be implemented on Moto Mods are:

- `AudioManager.ANLG_DOCK_HEADSET` (mod loudspeaker / speaker dock)
- `AudioManager.DEVICE_OUT_EARPIECE`
- `AudioManager.DEVICE_OUT_WIRED_HEADSET`
- `AudioManager.DEVICE_OUT_WIRED_HEADPHONE`
- `AudioManager.DEVICE_OUT_LINE`
- `AudioManager.DEVICE_OUT_HDMI`
- `AudioManager.DEVICE_IN_BUILTIN_MIC`
- `AudioManager.DEVICE_IN_BACK_MIC`
- `AudioManager.DEVICE_IN_WIRED_HEADSET`
- `AudioManager.DEVICE_IN_FM_TUNER`

A Moto Mod declares it audio device type(s) through its [Audio Protocol](../firmware/audio.md) firmware.

## Moto Mod Audio API {#moto-mod-audio-api}

There are no additional or proprietary Audio APIs for Moto Mods. An application can manage and control audio playback and playback state on an attached Moto Mod or accessories attached to a Moto Mod through the Android [AudioManager](http://developer.android.com/reference/android/media/AudioManager.html) and [AudioDeviceInfo](http://developer.android.com/reference/android/media/AudioDeviceInfo.html) APIs.

Any change to the system’s audio device state that triggers notifications will behave the same way for Moto Mod hosted audio devices as they do for audio devices integrated on the Moto Z. For example, attaching a headset to your Moto Mod triggers [`ACTION_HEADSET_PLUG`](http://developer.android.com/reference/android/media/AudioManager.html#ACTION_HEADSET_PLUG) and detaching a headset triggers [`ACTION_AUDIO_BECOMING_NOISY`](http://developer.android.com/reference/android/media/AudioManager.html#ACTION_AUDIO_BECOMING_NOISY).

## Audio Routing {#audio-routing}

An audio-capable Moto Mod can take on the same set of roles as an audio device on the Moto Z, including for example the role of loudspeaker, speakerphone, earpiece or headset.

Audio devices implemented on a Moto Mod (e.g. a mod speaker) or connected via a Moto Mod (e.g. connection to a Mod’s line-out jack) behave equivalently to those devices connected directly to an Android phone. If a device exists on both the Moto Mod and the Moto Z, the device on the Moto Mod takes priority.

That said, there are some scenarios that can be implemented with a Moto Mod that don’t have an obvious Android reference behavior.

### Moto Mod Speaker vs Phone Speaker {#moto-mod-speaker-vs-phone-speaker}

Because Moto Mod speakers can provide a very different user experience than most phone’s built-in loudspeaker(s), the Moto Mod loudspeaker device does not supersede the Moto Z loudspeaker in quite the same way that a Moto Mod headset will supersede a Moto Z headset. A Moto Mod speaker will supersede the Moto Z loudspeaker for simple playback operation (e.g. music and the audio portion of video playback). A Moto Mod speaker will only act as a speakerphone for voice calls and other full-duplex use cases when it also supplies a microphone with echo cancellation or supplies an echo reference signal so that it can use the microphone and noise cancellation built into the Moto Z. Moto Mod-aware applications can use Android routing APIs (e.g. [`AudioTrack.setPreferredDevice()`](http://developer.android.com/reference/android/media/AudioTrack.html#setPreferredDevice(android.media.AudioDeviceInfo)(android.media.AudioDeviceInfo))) to switch between the internal loudspeaker ([`TYPE_BUILTIN_SPEAKER`](http://developer.android.com/reference/android/media/AudioDeviceInfo.html#TYPE_BUILTIN_SPEAKER)) and the Moto Mod speaker ([`TYPE_DOCK`](http://developer.android.com/reference/android/media/AudioDeviceInfo.html#TYPE_DOCK)).

The simplest possible Moto Mod audio implementation is a loudspeaker used only for playback. To implement a speakerphone and support full-duplex use cases like voice calls, the Moto Mod must either provide an echo reference signal back to the Moto Z or have its own microphone and echo canceling DSP.

### Multiple audio jacks {#multiple-audio-jacks}

If both the Moto Z and the Moto Mod have headset jacks, some unusual device interactions may result. If the Android audio framework is aware of both `DEVICE_OUT_LINE` and `DEVICE_OUT_HEADSET` (in some combination of Moto Z and Moto Mod jacks), then `DEVICE_OUT_LINE` takes priority for media use cases and `DEVICE_OUT_HEADSET` takes priority for voice use cases. If devices of the same type are connected to both the Moto Z and the Moto Mod, then the Moto Mod path has priority.

### Audio-Ext Protocol and Displays {#audio-ext-protocol-and-displays}

A `DEVICE_OUT_HDMI` Moto Mod device will fine-tune audio on Mods that have both audio and video ports. When a Moto Mod announces support for HDMI audio via Audio-Ext protocol, the `Audio-Ext` output device will take priority over MyDP audio output of the Moto Z but the HDMI plug state in Android is not changed.

This behavior prevents docks with speakers and video output ports (e.g. DisplayPort or HDMI) to prevent a display with audio support from seizing the audio from the mod. If the Moto Mod takes both HDMI and Speaker audio, then audio will be routed to `Audio-Ext` regardless of a connected display’s audio capability.

A Moto Mod that routes audio only over MyDP need not implement `Audio-Ext` or `I2S` protocols at all.

## Connecting an Audio Moto Mod {#connecting-an-audio-moto-mod}

There are two stages to connection of an audio Moto Mod. The first stage is enumeration of the `Audio-Ext` protocol. Enumeration allows the Moto Mod to begin interaction with the Android audio framework; it doesn’t necessarily mean the Moto Mod will route audio.

### Built-in audio devices {#built-in-audio-devices}

If the Moto Mod has built-in audio devices like microphones or speakers, it will typically announce those directly to audio framework immediately upon enumeration of `Audio-Ext` protocol. Audio route updates happen automatically according to the currently active use case(s).

If the Moto Mod has a loudspeaker, any application that has a registered `AudioDeviceInfo` callback will be notified the the route has changed to `TYPE_DOCK`.

Note that it’s **not required** that an audio Moto Mod make available built-in devices on connection to the Moto Z. Audio Moto Mod developers may use proprietary mechanisms to control the Moto Mod behavior in more detail. For example, a speaker Moto Mod might have a “power” button that plugs and unplugs a Moto Mod loudspeaker device from the Android audio framework. Audio-Ext is enumerated the entire time but may have no available devices..

### Pluggable devices {#pluggable-devices}

If the Moto Mod has an accessory jack, it will announce plug detection events to the Android audio framework via the `Audio-Ext` protocol. The audio framework will translate Moto Mod accessory plug events to the corresponding Android plug events that application developers are used to seeing.

Connection or disconnection of a headset on a Moto Mod will trigger `Intent.ACTION_HEADSET_PLUG` with the “state” extra reflecting the new plug state and the “microphone” extra indicating the presence of Mod headset microphone.

Additionally, disconnection of a Moto Mod accessory audio device will trigger `Intent.ACTION_AUDIO_BECOMING_NOISY` if no other pluggable accessory is connected -- just like disconnection of a wired accessory from the Moto Z.

## Detecting whether a Moto Mod supports audio {#detecting-whether-a-moto-mod-supports-audio}

Audio Moto Mods work seamlessly with all Android applications without requiring any changes. A 3rd party application does not need to be aware of Moto Mods to take advantage of new speakers or microphones. If you need to determine whether the Moto Mod supports the Audio-Ext protocol, it can query the ModManager service with the `hasDeclaredProtocol()` function as described below.

```java
if (device.hasDeclaredProtocol(ModProtocol.Protocol.MODS_AUDIO) {
    // This Mod declares it is an audio capable device in its manifest
  }
```

[< Previous Page
**Mod Battery**](mod-battery.md)

[Next Page >
**Mod HID**](mod-hid.md)

## Related references

- [Moto Mods SDK for Android API Reference](http://motorolamobilityllc.github.io/motomods_sdk/com/motorola/mod/package-summary.html)
- [Moto Mods SDK for Android API Reference](http://motorolamobilityllc.github.io/motomods_sdk)
- [Index](http://motorolamobilityllc.github.io/motomods_sdk/index.html)
- [ModListener](http://motorolamobilityllc.github.io/motomods_sdk/index.html?com/motorola/mod/ModListener.html)
- [ModBacklight](http://motorolamobilityllc.github.io/motomods_sdk/index.html?com/motorola/mod/ModBacklight.html)
- [ModBattery](http://motorolamobilityllc.github.io/motomods_sdk/index.html?com/motorola/mod/ModBattery.html)
- [ModConnection](http://motorolamobilityllc.github.io/motomods_sdk/index.html?com/motorola/mod/ModConnection.html)
- [ModContract](http://motorolamobilityllc.github.io/motomods_sdk/index.html?com/motorola/mod/ModContract.html)
- [ModDevice](http://motorolamobilityllc.github.io/motomods_sdk/index.html?com/motorola/mod/ModDevice.html)
- [ModDisplay](http://motorolamobilityllc.github.io/motomods_sdk/index.html?com/motorola/mod/ModDisplay.html)
- [ModInterfaceDelegation](http://motorolamobilityllc.github.io/motomods_sdk/index.html?com/motorola/mod/ModInterfaceDelegation.html)
- [ModManager](http://motorolamobilityllc.github.io/motomods_sdk/index.html?com/motorola/mod/ModManager.html)
- [ModProtocol](http://motorolamobilityllc.github.io/motomods_sdk/index.html?com/motorola/mod/ModProtocol.html)

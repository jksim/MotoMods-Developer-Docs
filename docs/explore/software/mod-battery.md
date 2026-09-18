---
title: "Moto Z Software: Mod Battery"
source_url: http://developer.motorola.com/explore/software/mod-battery
source_capture: 2016 Squarespace portal
---

# Moto Z Software: Mod Battery

## Introduction {#introduction}

Support for Battery and power-providing Moto Mod is integrated natively with the Moto Mod platform. Your Moto Z will automatically leverage an attached Moto Mod battery, based on its declared type, without requiring you to provide an application or use the `ModBattery` Android API.

The Moto Mod Android SDK enables a developer which needs additional information about an attached Moto Mod battery to recognize when an attached Moto Mod has a battery, determine the type of this battery, query the battery capacity and get topical information about its this Moto Mod battery charge level and charging status.

An application can obtain information about a Moto Mod battery through the methods exposed by the Moto Mod SDK’s `ModBattery` class.

## Prerequisites {#prerequisites}

### Android Prerequisites {#android-prerequisites}

#### Development environment {#development-environment}

Before using the classes described below in your application, you must have installed the Moto Mod Android SDK on your development device as described in the tool section.

#### Familiarity with the Android BatteryManager {#familiarity-with-the-android-batterymanager}

You should be familiar with the [Android BatteryManager API](https://developer.android.com/reference/android/os/BatteryManager.html), as the Moto Mod specific battery information returned by the `ModBattery` class closely follows the conventions of Android’s `BatteryManager`.

#### Familiarity with the PTP and Battery Firmware documentation {#familiarity-with-the-ptp-and-battery-firmware-documentation}

The [`Power Transfer`](../firmware/power-transfer.md) and [`Battery`](../firmware/battery.md) firmware developer documentation provide fine-grain control over battery and power-provider configuration. The behavior of a Moto Mod battery will vary based on its PTP configuration and the Moto Mod developer interesting in issuing, or building a power-providing Moto Mod should gain a solid understanding of these protocols first.

### Hardware Prerequisites {#hardware-prerequisites}

Battery specific functions exposed through the Moto Mod Android SDK will only be available if a Moto Mod is attached to your smartphone, if the attached Moto Mod has a well-formed hardware manifest, and if it declares support for the `battery` and `power-transfer-protocol` Greybus class.

## Supported Mod Battery type {#supported-mod-battery-type}

A Moto Mod can embed its own battery. When a Moto Mod is attached to a smartphone, the charge and discharge behavior of the Moto Mod battery is controlled by its firmware `Battery` and `Power-transfer` protocol configuration, as described in the [`Power Transfer`](../firmware/power-transfer.md) and [`Battery`](../firmware/battery.md) firmware developer documentation.

The platform supports different Moto Mod power-provider/battery profiles. A Moto Mod battery must declare its supported profile in the firmware. The device will automatically make optimal use of the battery based on this profile declaration. The supported battery profiles are:

- The Moto Mod declares its battery as a **SUPPLEMENTAL** battery. Your Moto Mod should use this profile when it hosts a battery which **primary function** is to keep your Moto Z powered (e.g: the Moto Mod is a battery pack).
- The Moto Mod declares its battery as a **REMOTE** (or ‘**NEVER**‘ as defined at the [Power Transfer](../firmware/power-transfer.md) firmware page) battery. Your Moto Mod should use this profile when it hosts a battery which sole function is to provide power to the Moto Mod, and never to a Moto Z.

- The Moto Mod declares its battery as a **REMOTE EMERGENCY** (or ‘**LOW POWER SAVER**’ at the [Power Transfer](../firmware/power-transfer.md) firmware page) battery. Your Moto Mod should use this profile when it hosts a battery which primary function is to provide power to the Moto Mod but could be used to power a Moto Z when the smartphone battery gets low.

The Moto Mod could also elect, through its `Power-Transfer` protocol definition, to not receive or provide power to the attached Moto Z. The Moto Mod will need to include its own charging apparatus. The functionality of a Moto Mod battery is automatically controlled by the Moto Z software and based on the battery type declared by the Moto Mod firmware upon attach, an application **can not** change the advertised battery type of a Moto Mod. The Moto Mod SDK only enables any application to track charge, discharge and information about a Moto Mod battery.

## Standard Battery behavior

The user experience on a Moto Z will vary slightly based on the declared battery profile. This section provides a short overview of the behavioral differences experienced on a Moto Z when different types of Moto Mod batteries are attached.

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td></td>
<td>A Moto Mod battery provides power to Moto Z</td>
<td>A charging Moto Z can charge the Moto Mod battery</td>
<td>The status bar indicates when Moto Mod is providing power to Moto Z</td>
<td>Moto Z Settings and Quick settings show the charge level of the Moto Mod battery</td>
</tr>
</thead>
<tr>
<td><strong>SUPPLEMENTAL</strong></td>
<td>Yes, to keep the Moto Z charged</td>
<td>Yes</td>
<td>Yes</td>
<td>Yes</td>
</tr>
<tr>
<td><strong>REMOTE (‘NEVER’)</strong></td>
<td>No</td>
<td>Yes</td>
<td>No</td>
<td>Yes</td>
</tr>
<tr>
<td><strong>EMERGENCY (‘Low power saver’)</strong></td>
<td>Yes, buy only when the Moto Z battery is Low</td>
<td>Yes</td>
<td>Yes</td>
<td>Yes</td>
</tr>
</table>
</div></div>

## Top-Off vs. Efficiency mode

Under the Moto Mod settings for a battery, the user can choose to set a supplemental battery usage policy to “top-off” or “efficiency” through Moto Mod settings.

- In the **default mode** (the default usage policy of a battery), your Moto Z will use a supplemental battery to always stay **fully** charged (100%) as long as the Moto Mod battery can provide power.
- In **EFFICIENCY** mode, your Moto Z will leverage the attached supplemental battery optimally, and will stay charged at 80% (not 100%) as long as the Moto Mod battery can provide power

## Working with a Moto Mod Battery: Added ModBattery Class {#working-with-a-moto-mod-battery-added-modbattery-class}

The Moto Mod SDK provides an additional `ModBattery` class which enables an application to know what the declared battery profile of the attached Moto Mod battery is, query the capacity, charge level and charging status of a Moto Mod battery.

### Determining whether the attached ModDevice embeds a battery {#determining-whether-the-attached-moddevice-embeds-a-battery}

To detect when a Moto Mod is attached, your application should listen on Moto Mod `ACTION_MOD_ATTACH` and `ACTION_MOD_DETACH` intents - or register a `ModListener` - as described at the Mod Management page. Once a Moto Mod is attached to your device, an application can use the `ModDevice.hasDeclaredProtocol()` function to check whether the attached `ModDevice` declares the `BATTERY` and `PTP` (power transfer) protocol.

```java
if (device.hasDeclaredProtocol(ModProtocol.Protocol.BATTERY)) {
    // We know this device has a battery and supports battery metering
    }

if (device.hasDeclaredProtocol(ModProtocol.Protocol.PTP)) {
    // We know this device can provide or receive power to the Moto Z
    }
```

The state and level of this Moto Mod battery will be automatically reported by the `ModBattery` class and its associated method. `ModBattery` will only be available when a battery device is present and has enumerated successfully. As the power transfer logic between the Moto Mod and and the Moto Z is automatically controlled by the Moto Z, there are no exposed functions for an application to change this predefined behavior.

### Working with the ModBattery Class {#working-with-the-modbattery-class}

If an attached Moto Mod supports the BATTERY protocol, and your application wants to get information about this Moto Mod battery, it **must** first acquire a `ModBattery` object by calling the `ModManager.getClassManager()` function, after your application verified that a `ModDevice` is attached and that this `ModDevice` supports the battery protocol.

The code sample below shows how to get access to the `ModBattery` class from the `ModManager`. Your application should first confirm that the attached Moto Mod declares support for the `PTP` and `BATTERY` protocols, as shown above.

```java
if (device.hasDeclaredProtocol(ModProtocol.Protocol.BATTERY)) {
    ModBattery mb = (ModBattery)mManager.getClassManager(modDev,
    ModProtocol.Protocol.BATTERY);
    ...
    }
```

### Getting the Moto Mod Battery Capacity {#getting-the-moto-mod-battery-capacity}

When a battery Moto Mod is attached, an Android application can determine the maximum capacity of the attached Moto Mod battery by calling the `ModBattery.getBatteryCapacity()` method. This method will return the capacity of the attached battery in mAH, or `Long.MIN_VALUE` if the Moto Mod did not return its capacity through greybus.

The code sample below shows how to retrieve the Moto Mod battery capacity.

```java
if (device.hasDeclaredProtocol(ModProtocol.Protocol.BATTERY)) {
    ModBattery mb = (ModBattery)mManager.getClassManager(modDev,
    ModProtocol.Protocol.BATTERY);
    if (mb != null) {
      modbatterycapacity = mb.getBatteryCapacity();
```

### Getting the Moto Mod Battery Level {#getting-the-moto-mod-battery-level}

When a battery Moto Mod is attached, an Android application can track changes in the battery charge level by using the `ModBattery.getBatteryLevel()` method. This method will return the charge level of the attached battery as a percentage (0-100).

The code sample below shows how to retrieve the Moto Mod battery level.

```java
if (device.hasDeclaredProtocol(ModProtocol.Protocol.BATTERY)) {
    ModBattery mb = (ModBattery)mManager.getClassManager(modDev,
    ModProtocol.Protocol.BATTERY);
    if (mb != null) {
      modbatterylevel = mb.getBatteryLevel(); 
      // we know what the battery level is
```

### Determining the declared type of the attached Moto Mod battery {#determining-the-declared-type-of-the-attached-moto-mod-battery}

The `ModBattery.getBatteryType()` method returns the type of the battery on the Moto Mod. `ModBattery.getBatteryType()` will return either `BATTERY_USAGE_TYPE_SUPPLEMENTAL`, `BATTERY_USAGE_TYPE_REMOTE`, `BATTERY_USAGE_TYPE_EMERGENCY` or `BATTERY_USAGE_TYPE_UNKNOWN`.

The code sample below shows how to retrieve the Moto Mod battery type.

```java
if (device.hasDeclaredProtocol(ModProtocol.Protocol.BATTERY)) {
    ModBattery mb = (ModBattery)mManager.getClassManager(modDev,
    ModProtocol.Protocol.BATTERY);
    if (mb != null) {
      modbatterytype = mb.getBatteryType();
```

### Determining whether a ModBattery is charging or discharging {#determining-whether-a-modbattery-is-charging-or-discharging}

The `ModBattery.getBatteryStatus()` method enables your application to determine whether the battery on the Moto Mod is charging or discharging. A Moto Mod battery could be charging when your Moto Z is plugged in a USB-C charger, or when the Moto Mod itself has its own charging apparatus and is attached to a charger.

The value returned by `ModBattery.getBatteryStatus()` follows the convention set forth by Android for reporting device battery charge status. An application can use this value to determine whether the Moto Mod battery is charging, discharging or full.

```java
if (device.hasDeclaredProtocol(ModProtocol.Protocol.BATTERY)) {
    ModBattery mb = (ModBattery)mManager.getClassManager(modDev,
    ModProtocol.Protocol.BATTERY);
    if (mb != null) {
      modbatterystatus = mb.getBatteryStatus();
```

<div class="md-typeset__scrollwrap"><div class="md-typeset__table">
<table class="pure-table pure-table-bordered">
<thead>
<tr>
<td>Returned Constant</td>
<td>Value</td>
<td>Details</td>
</tr>
</thead>
<tr>
<td><code>BATTERY_STATUS_UNKNOWN</code></td>
<td>1</td>
<td>The Mod Battery status is not known</td>
</tr>
<tr>
<td><code>BATTERY_STATUS_CHARGING</code></td>
<td>2</td>
<td>The Mod Battery is charging </td>
</tr>
<tr>
<td><code>BATTERY_STATUS_DISCHARGING</code></td>
<td>3</td>
<td>The Mod Battery is discharging</td>
</tr>
<tr>
<td><code>BATTERY_STATUS_NOT_CHARGING</code></td>
<td>4</td>
<td>The Mod Battery is not charging</td>
</tr>
<tr>
<td><code>BATTERY_STATUS_FULL</code></td>
<td>5</td>
<td>The Mod Battery is full</td>
</tr>
</table>
</div></div>

### Determining whether your Moto Z is charging from an attached Moto Mod {#determining-whether-your-moto-z-is-charging-from-an-attached-moto-mod}

The `ModBattery.isPlugTypeMod()` method enables your application to determine whether the attached Moto Mod can charge the phone. `ModManager.isPlugTypeMod()` will return true if no external charger is attached and the device can be charged from the Moto Mod battery.

## When a battery reports issues {#when-a-battery-reports-issues}

If a Moto Mod embeds a battery, the Moto Mod is responsible for thermal mitigation and reporting errors to the smartphone. Motorola has defined a vendor specific channel to report asynchronous Moto Mod errors, including thermal, current and oem specific data.

An application which needs to listen for these sudden capabilities change (as an example, a thermal incident on the Moto Mod causing the Moto Mod to report it is operating in a reduced state) can register a [`ModListener`](mod-management.md) (as described below).

This listener `onCapabilityChanged()` function will be called back when the Moto Mod reports a capability change event. An application can then use the `ModManager.getCapabilityLevel()` and `ModManager.getCapabilityReason()` to determine the cause of this capability change, as described in the [Mod Management software](mod-management.md) and [Mod Management firmware](../firmware/mod-management.md) documents.

An application which needs to be immediately informed of capability change on an attached battery should register a listener with the `com.motorola.mod.ModManager.registerModListener()` API.

```java
mManager.registerModListener(MainActivity.this, new int[] {ModProtocol.BATTERY});
```

## More Information

For more information, see the [ModBattery Javadoc API](http://motorolamobilityllc.github.io/motomods_sdk/com/motorola/mod/ModBattery.html).

[< Previous Page
**Mod Display**](mod-display.md)

[Next Page >
**Mod Audio**](mod-audio.md)

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

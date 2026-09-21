---
title: "Examples: MDK Utility"
source_url: http://developer.motorola.com/build/examples/mdk-utility
source_capture: 2016 Squarespace portal
---

# Examples: MDK Utility

## Overview {#overview}

The ‘MDK Utility’ Android App has two core functions...

#### 1) To Provide Flashing & Developer Support {#1-to-provide-flashing-developer-support}

MDK Utility is a simple app that displays basic status information for the Reference Moto Mod attached to your Moto Z. It can also be used to flash development firmware on your Reference Moto Mod.

> Jump down to the [Flashing & Developer Support](#flashing) section below for more detail...

#### 2) To Provide a ‘Hello World’ example (aka ‘Blinky’) {#2-to-provide-a-hello-world-example-aka-blinky-}

This app also provides an end-to-end ‘Hello World’ example that shows how to control the LED on the Reference Moto Mod. Source code is made available so you can use this in your own projects.

> Visit the [Hello World](hello-world.md) page for more detail...

## Before you begin... {#before-you-begin}

#### Required Hardware {#required-hardware}

This app and example requires a **Moto Z** and **Reference Moto Mod**. To get started, you'll need to buy the required hardware.

#### Software and Tools {#software-and-tools}

See the [Build > Tools](../tools/index.md) section to set up your development environment and learn about building from source, flashing firmware, and how to debug & log.

#### Download Example Source Code {#download-example-source-code}

- **Source Code** for the MDK Utility App is available at <https://github.com/jksim/mdkutility>.

#### Download MDK Utility App {#download-mdk-utility-app}

The MDK Utility App will only work on Moto Z devices.

- [MDK Utility app (rebuilt from source; was on Google Play Store)](../../assets/apks/mdkutility.apk)
- [MDK Utility app (rebuilt from source; was on Lenovo App Store)](../../assets/apks/mdkutility.apk)

For more details, see the [Moto Mods Android Application](#application) section further down this page.

#### Community and Support {#community-and-support}

Ask questions, engage with the developer community, and get support for this example in the [Moto Mods group at element14.com](https://www.element14.com/community/groups/moto-mods). Also check out our [Support](../../support/index.md) page.

## Moto Mods Android Application {#application}

#### Install APK {#install-apk}

Download and install the [MDK Utility app (rebuilt from source; was on Google Play Store)](../../assets/apks/mdkutility.apk).

#### MDK Utility sample APK {#mdk-utility-sample-apk}

The Moto MDK Utility sample apk is an open source project, works as an downloadable Android app, to show the capability of flashing MDK firmware.

After installing and running the MDK Utility, you’ll see the following:

The top section presents status information for *any* Moto Mod currently attached to your Moto Z. In addition, if the Reference Moto Mod (running the stock bootloader) is attached with a Personality Card inserted, you will see the name of the card along with a unique PID.

> **NOTE:** Always detach the Reference Moto Mod from your Moto Z before attempting to insert or remove a Personality Card.

Besides providing details on the attached Moto Mod, developers can use this application to flash firmware. To help protect your prototypes, the MDK Utility only allows firmware updates for Developer VID 0x42. If your Reference Moto Mod is in Example Mode, use the Set Mode to switch to Developer before flashing your prototype firmware. See the [Flashing Firmware](../tools/flashing-firmware.md) page for flashing details.

The final feature of the MDK Utility is an LED Control which requires the default Example Mode firmware. Detach your Reference Moto Mod and remove any Personality Card (you can leave the Perforated or HAT Adapter Boards in) and reattach. If you are in Developer Mode, Set Mode back to Example. If prompted, select Continue when the Moto Mod Development Kit requests a firmware update. Once the Reference Moto Mod is updated with the blinky firmware, the LED Light option will be enabled. Hit the switch, and a blinking LED on the Reference Moto Mod will let you know everything is working properly.

#### Source code {#source-code}

The source code of the MDK Utility sample APK is published at <https://github.com/jksim/mdkutility>.

To build the sample APK from source code, please [download and install Android Studio from Android Developer Site](http://developer.android.com/sdk/index.html), then import the [mdkutility project](https://github.com/jksim/mdkutility) into Android Studio. See [Developer Tools: Setup Your Development Environment](../tools/setup-environment.md) for more info.

#### Reference for ModManager interface & query Mod statues: {#reference-for-modmanager-interface-query-mod-statues-}

See [Hello World! documentation](hello-world.md#reference) for implementation of MotoMods interface creation and query.

## Flashing & Developer Support {#flashing}

For details on using the MDK Utility for flashing, see the [Flashing Firmware](../tools/flashing-firmware.md) section.

The code below shows how to implement this, should you choose to handle flashing in your own application. The Moto Mods platform supports automatic firmware downloads for certified Moto Mods (see our [Partner section](../../partner/certification-program.md) to learn more about certifying your Moto Mod).

##### Reference for firmware update intents listener: {#reference-for-firmware-update-intents-listener-}

```java
/** Register for firmware update related intents */
modEventReceiver = new MyBroadcastReceiver();
IntentFilter filter = new IntentFilter(ModManager.ACTION_MOD_FIRMWARE_UPDATE_DONE);
filter.addAction(ModManager.ACTION_MOD_FIRMWARE_UPDATE_START);
filter.addAction(ModManager.ACTION_MOD_ENUMERATION_DONE);
filter.addAction(ModManager.ACTION_REQUEST_CONSENT_FOR_UNSECURE_FIRMWARE_UPDATE);
filter.addAction(ModManager.ACTION_MOD_ERROR);
context.registerReceiver(modEventReceiver, filter, ModManager.PERMISSION_MOD_INTERNAL, null);
/** Register for firmware request intent with higher priority to overlap ModManager */
requestFwReceiver = new MyBroadcastReceiver();
filter = new IntentFilter(ModManager.ACTION_MOD_REQUEST_FIRMWARE);
filter.setPriority(IntentFilter.SYSTEM_HIGH_PRIORITY);
/**
* Request the broadcaster who send these intents must hold permission PERMISSION_MOD_INTERNAL,
* to avoid the intent from fake senders. For future details, refer to:
* https://developer.android.com/reference/android/content/Context.html#registerReceiver
*/
context.registerReceiver(requestFwReceiver, filter, ModManager.PERMISSION_MOD_INTERNAL, null);
```

##### Reference for flashing firmware: {#reference-for-flashing-firmware-}

```java
/** Generate the URI permissions for ModService, to access firmware files URIs */
for (Uri u : pendingUri) {
   context.grantUriPermission("com.motorola.modservice",
           u, Intent.FLAG_GRANT_READ_URI_PERMISSION);
}
try {
   /** Provide the firmware file uris to ModManager for update */
   result = modManager.requestUpdateFirmware(modDevice, pendingUri);
} catch (IllegalArgumentException e) {
   result = FIRMWARE_UPDATE_ILLEGAL_EXCEPTION;
   Log.e(Constants.TAG, "modManager.requestUpdateFirmware illegal failed.");
   e.printStackTrace();
} catch (SecurityException e) {
   result = FIRMWARE_UPDATE_SECURITY_EXCEPTION;
   Log.e(Constants.TAG, "modManager.requestUpdateFirmware security failed.");
   e.printStackTrace();
} catch (Exception e) {
   result = FIRMWARE_UPDATE_FAILED;
   Log.e(Constants.TAG, "modManager.requestUpdateFirmware failed.");
   e.printStackTrace();
}
```

##### Reference for handling firmware update intents: {#reference-for-handling-firmware-update-intents-}

```java
if (ModManager.ACTION_MOD_FIRMWARE_UPDATE_DONE.equals(action)) {
   /** The firmware update of the mod completed, with result in extra ModManager.EXTRA_RESULT_CODE */
   int result = intent.getIntExtra(ModManager.EXTRA_RESULT_CODE, -1);
} else if (ModManager.ACTION_MOD_ENUMERATION_DONE.equals(action)) {
   /** Phone has finished enumerating all the functionality of mod */
} else if (ModManager.ACTION_MOD_FIRMWARE_UPDATE_START.equals(action)) {
   /** The device starts firmware update on an attached mod */
} else if (ModManager.ACTION_MOD_REQUEST_FIRMWARE.equals(action)) {
   /** The mod is being attached to the device but but is unable to boot due to
    * missing or invalid firmware, and request user space to give the firmware. */
   // TODO: This intent is broadcast when a mod missing or invalid firmware.
   // If you are developing the consumer mod, call abortBroadcast() here and
   // provide the according consumer firmware for the mod.
   /* Code Example:
   if (consumerMod) {
       abortBroadcast();
       if (modManager != null && modDevice != null) {
           modManager.requestUpdateFirmware(modDevice, consumerFirmwareUris);
       }
   } else {
       // Notify UI that ModManager is requesting the firmware for this mod
   }
   */
   if (getModDevice() != null) {
       if (getModDevice().getVendorId() == Constants.VID_DEVELOPER) {
           /**
            * Currently mod is Developer Mode, abort this intent,
            * so ModManager will not receive it to do firmware update, instead
            * need handle the update in by self. Refer to
            * MainActivity:handler:handleMessage(MSG_REQUEST_FIRMWARE);
            */
           abortBroadcast();
       }
   }
   /** Notify MainActivity:handler to execute flashing */
   notifyListeners(MSG_REQUEST_FIRMWARE);
} else if (ModManager.ACTION_MOD_ERROR.equals(action)) {
   /** An error happened to the mod */
   int error = intent.getIntExtra(ModManager.EXTRA_MOD_ERROR, -1);
   Log.e(Constants.TAG, "EXTRA_MOD_ERROR: " + error);
}
```

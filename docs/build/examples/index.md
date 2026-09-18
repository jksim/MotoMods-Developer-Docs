---
title: "Examples: Overview"
source_url: http://developer.motorola.com/build/examples
source_capture: 2016 Squarespace portal
---

# Examples: Overview

While documentation is great, it’s sometimes easier to see the full solution end to end.  That’s why we’re providing several examples to help walk you through the software and firmware interactions.  But without the hardware details it really isn’t the full story, so we’ve created several Personality Cards that each showcase a different aspect of the Moto Mods platform.  The electrical and mechanical schematics for each Personality Card will be available for download to help accelerate your own circuit designs, or just to experiment by changing the software or firmware.  These Personality Cards take full advantage of the Reference Moto Mod, and can be inserted and removed just like the Perforated Board.  The Personality Cards serve as the natural progression of your design through schematic and layout from the Perforated Board.

## MDK Utility {#mdk-utility}

When you purchase your [Moto Mods Software Development Kit](../../hardware/mdk.md), you’ll get the **Reference Moto Mod**, a **Perforated Board**, and a **cover** to help protect your projects while on the go. Simply snap it to the back of your Moto Z, and you’ll be taken to the Play Store to download the MDK Utility. This isn’t a custom functionality, your Moto Mod gets the same support with just a couple lines of code.

[View MDK Utility Example](mdk-utility.md) | [View 'Hello World!' Example](hello-world.md) | [Buy Now](https://www.element14.com/community/docs/DOC-82858/l/moto-mod-developer-kit-mdk)

## Personality Cards {#personality-cards}

Four Personality Cards are available to help teach you how the hardware, software, and firmware interact:

### Audio Personality Card

The Audio Personality is an example of adding a simple Loudspeaker to your Moto Z.  With the example firmware, you can modify it to represent different audio devices to better understand Android audio routing.  Modify the Android application and firmware to add a Raw protocol to simulate a hot-plug device, like an external headset (or speakers with an on/off switch).

[View Example](audio.md) | [Learn More](../../hardware/audio-personality-card.md) | [Buy Now](https://www.element14.com/community/docs/DOC-82892/l/moto-mods-audio-personality-card)

### Battery Personality Card

The Battery Personality is an example of how your Moto Mod would add a rechargeable battery to add capacity to your Moto Z.  Not only can you learn the basics of charging and system interaction, by modifying the firmware you can experiment with different battery profiles or even use as a battery pack for a device attached via the Reference Moto Mod’s Type C port.

[View Example](battery.md) | [Learn More](../../hardware/battery-personality-card.md) | [Buy Now](https://www.element14.com/community/docs/DOC-82910/l/moto-mods-battery-personality-card)

### Display Personality Card

This Display personality is an example of a DSI based display attached through the Moto Bridge.  It’s a great way to dig into MuC/Moto Bridge interaction and how the MHB IPC works.  Just insert into the Reference Moto Mod, attach to your Moto Z, and you’ll get instant display mirroring.  With its peer Android application, you’ll be able to see how Presentation works to provide custom content to the Secondary Display.

[View Example](display.md) | [Learn More](../../hardware/display-personality-card.md) | [Buy Now](https://www.element14.com/community/docs/DOC-82911/l/moto-mods-display-personality-card)

### Sensor Personality Card

The Sensor Personality Card is an example of how you would add a custom sensor that doesn’t exist in Android.  This instance utilizes a thermistor hooked to an analog to digital converter on the MuC to measure outside temperature; and uses the Raw protocol to pass that to an Android application for visual output.

[View Example](sensor.md) | [Learn More](../../hardware/temperature-sensor-personality-card.md) | [Buy Now](https://www.element14.com/community/docs/DOC-82912/l/moto-mods-temperature-sensor-personality-card)

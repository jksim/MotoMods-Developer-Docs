---
title: "Moto Mods Developer Documentation"
---

# Moto Mods Developer Documentation

*A restored archive of the developer documentation Motorola published at
`developer.motorola.com` between 2016 and 2018.*

Moto Mods snap onto the back of a Moto Z phone and extend it with hardware the
phone does not have — speakers, projectors, batteries, cameras, displays, and
whatever else a developer could build. The platform was opened up with a
development kit, a firmware stack built on **NuttX** and **Greybus**, and an
Android SDK. Motorola took the portal offline; these pages are what the Wayback
Machine preserved of it.

<div class="mm-home-grid" markdown>

[**Get Started** :material-rocket-launch:<br><small>What you need, and how the pieces fit together.</small>](get-started.md){ .mm-home-card }

[**Explore the Platform** :material-sitemap:<br><small>System architecture, the eleven Greybus firmware protocols, and the Android APIs.</small>](explore/index.md){ .mm-home-card }

[**Build a Prototype** :material-tools:<br><small>The MDK user guide, developer tooling, and nine worked examples.</small>](build/index.md){ .mm-home-card }

[**Hardware** :material-chip:<br><small>The Reference Moto Mod, perforated board, HAT adapter, and personality cards.</small>](hardware/index.md){ .mm-home-card }

[**Downloads** :material-download:<br><small>Schematics, design files, example project archives, and ModLib.</small>](downloads.md){ .mm-home-card }

[**Partner & Certification** :material-certificate:<br><small>The certification programme and the licence terms it ran under.</small>](partner/index.md){ .mm-home-card }

</div>

## How a Moto Mod works

Every Moto Mod carries a **Moto Mod Microcontroller (MuC)** — an STM32L476
running NuttX — which brings up the interface to the phone, enumerates the
protocols the Mod supports, and manages power and firmware updates. A separate
**Moto High Speed Bridge (MHB)** carries display and camera traffic when it is
needed, and stays powered down when it is not.

Underneath, the platform speaks [Greybus](explore/system-architecture.md), the
open-source protocol from Project Ara. Greybus lets a driver running on the Mod
appear to Android as though it were local hardware, so a Mod speaker joins the
normal audio routing and a Mod battery joins the normal charging logic without
anyone writing a bespoke kernel driver.

Mods with custom hardware that Android has no concept of — sensors, instruments,
arbitrary USB devices — use the [Raw protocol](explore/software/mod-raw-devices.md)
to talk to a companion Android app instead.

## Where to start reading

| If you want to… | Start at |
| --- | --- |
| Understand the platform end to end | [System Architecture](explore/system-architecture.md) |
| Implement a firmware protocol | [Firmware: Overview](explore/firmware/index.md) |
| Write the Android side | [Android Software: Overview](explore/software/index.md) |
| Put hardware together | [MDK Overview](build/mdk-user-guide/index.md) |
| Copy working code | [Examples](build/examples/index.md) |
| Set up a toolchain | [Set Up Your Environment](build/tools/setup-environment.md) |

!!! note "This is an archive"
    Moto Mods is a discontinued product. Download links, forums, purchase
    links and contact forms are preserved as they were written and no longer
    lead anywhere live. See [About This Archive](about.md) for what was
    recovered, what is missing, and where each page came from.

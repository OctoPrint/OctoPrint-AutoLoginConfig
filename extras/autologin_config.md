---
layout: plugin

id: autologin_config
title: OctoPrint-AutoLoginConfig
description: TODO
authors:
  - Charlie Powell
license: AGPLv3

date: today's date in format YYYY-MM-DD, e.g. 2020-11-15

homepage: https://github.com/cp2004/OctoPrint-AutoLoginConfig
source: https://github.com/cp2004/OctoPrint-AutoLoginConfig
archive: https://github.com/cp2004/OctoPrint-AutoLoginConfig/archive/main.zip

tags:
  - settings
  - configuration
  - autologin
  - autologinlocal
  - accesscontrol

screenshots:
  - url: /assets/img/plugins/autologin_config/instructions.png
    alt: instructions
    caption: Instructions for configuration
  - url: /assets/img/plugins/autologin_config/config.png
    alt: configuration
    caption: Configuration UI
  - ...

featuredimage: /assets/img/plugins/autologin_config/config.png

compatibility:
  octoprint:
    - 1.5.0

  os:
    - linux
    - windows
    - macos
    - freebsd

  python: ">=2.7,<4"
---

Allows for UI configuration of AutoLoginLocal - an OctoPrint feature that automatically logs in a user from a local network.

<div class="alert alert-block">
    <div class="row-fluid">
        <p>
            <i class="fas fa-exclamation-triangle fa-3x pull-left text-error" style="margin-right: 0.5em;"></i>
            <strong>Do not use this if you cannot trust EVERYONE on your local network.</strong> And I really
            mean everyone. If you ignore this and then someone takes over your OctoPrint instance, installs
            malware on it and makes your printer print an endless stream of benchies, that's on you.
        </p>
    </div>
</div>

**This plugin requires access control to be enabled & set up correctly on OctoPrint 1.4.0 or newer.**

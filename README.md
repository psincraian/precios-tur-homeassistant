# Precios TUR

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]

## Overview

The Precios TUR integration for Home Assistant allows you to track the current gas prices from the TUR (Tarifa de Último Recurso) service. This integration fetches data from the TUR API and provides sensors to monitor different types of gas rates.

## How It Works

This integration uses the TUR API to fetch the latest gas prices. It sets up sensors in Home Assistant to display the current variable rate, fixed rate, and total rate for the selected category (TUR1, TUR2, or TUR3). The data is updated periodically to ensure you always have the latest information.

**This integration will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Show info from TUR API

## Sensors

The integration exposes the following sensors:

- **Variable Rate**: Shows the current variable gas rate.
- **Fixed Rate**: Shows the current fixed gas rate.

Each sensor is named according to the selected category (TUR1, TUR2, or TUR3) during the configuration.


## Installation

### Using HACS

Click on

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=psincraian&repository=precios-tur-homeassistant)


### Manual

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `precios_tur`.
1. Download _all_ the files from the `custom_components/precios_tur/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Precios TUR"

## Configuration

Configuration is done in the UI. When adding the integration, you will be prompted to enter the API URL and select the category (TUR1, TUR2, or TUR3).

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[commits-shield]: https://img.shields.io/github/commit-activity/y/psincraian/precios-tur-homeassistant.svg
[commits]: https://github.com/psincraian/precios-tur-homeassistant/commits/main
[exampleimg]: example.png
[license-shield]: https://img.shields.io/github/license/psincraian/precios-tur-homeassistant.svg
[maintenance-shield]: https://img.shields.io/badge/maintainer-Petru%20Sincraian-blue.svg
[releases-shield]: https://img.shields.io/github/release/psincraian/precios-tur-homeassistant.svg
[releases]: https://github.com/psincraian/precios-tur-homeassistant/releases

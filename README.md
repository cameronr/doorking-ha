# Doorking 1812AP

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

This component only works with the Doorking 1812AP with an ethernet connection.
It connects to the Doorking over ethernet to get the status and open/close the gate.
I sniffed the traffic from the windows client to reverse "engineer" the protocol but only just enough to get the open/close and status commands working.

**This integration will set up the following platforms.**

| Platform | Description                         |
| -------- | ----------------------------------- |
| `switch` | Opens (on) or closes (off) the gate |

## Installation

Manual Installation. To control your installation yourself, download the doorking-ha repo, and then copy the `custom_components/doorking_1812ap` directory into a corresponding `custom_components/doorking_1812ap` within your Home Assistant configuration directory. Then restart Home Assistant.

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

---

[integration_blueprint]: https://github.com/cameronr/doorking-ha
[buymecoffee]: https://www.buymeacoffee.com/ludeeus
[commits-shield]: https://img.shields.io/github/commit-activity/y/cameronr/doorking-ha.svg?style=for-the-badge
[commits]: https://github.com/cameronr/doorking-ha/commits/main
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/cameronr/doorking-ha.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40cameronr-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/cameronr/doorking-ha.svg?style=for-the-badge
[releases]: https://github.com/cameronr/doorking-ha/releases

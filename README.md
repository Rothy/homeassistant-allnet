# Allnet Integration for Home Assistant

Custom integration for automatic discovery and control of Allnet devices (ALL3500, ALL3073, etc.) in Home Assistant.

## Features

 **Automatic Device Discovery**: Automatically scans all available sensors and actors
 **Supported Sensors**:
   - Temperature (°C/°F)
   - Humidity (%)
   - Air Pressure (hPa/Pa)
   - Additional sensors are automatically detected

 **Supported Actors**: Switches/Relays (on/off)
 **Config Flow**: Easy setup via UI
 **Polling**: Automatic updates every 60 seconds

## Installation

### Via SSH/Terminal (Recommended)

1. Open the **Terminal & SSH** add-on in Home Assistant
2. Run the following commands:

```bash
mkdir -p /config/custom_components/allnet
cd /config/custom_components/allnet
git clone https://github.com/Rothy/homeassistant-allnet.git .
ha core restart
```

3. After restart, go to **Settings**  **Devices & Services**  **Add Integration**
4. Search for **"Allnet"**
5. Enter your device credentials:
   - **Host**: e.g., `192.168.178.4`
   - **Username**: e.g., `ha`
   - **Password**: Your device password

### Manual Installation

1. Download this repository
2. Copy the contents to `/config/custom_components/allnet/`
3. Restart Home Assistant
4. Follow steps 3-5 from above

## Configuration

The integration will automatically discover:
- All active sensors (temperature, humidity, pressure, etc.)
- All available actors/switches

## Supported Devices

- Allnet ALL3500
- Allnet ALL3073
- Other Allnet devices with XML API

## Example Automation

```yaml
automation:
  - alias: "Turn on miner at high temperature"
    trigger:
      - platform: numeric_state
        entity_id: sensor.allnet_internal
        above: 25
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.allnet_miner
```

## Troubleshooting

### Connection Failed
- Check IP address and network connectivity
- Test with: `curl -u "username:password" "http://192.168.178.4/xml/?mode=info"`
- Verify username and password

### No Sensors/Actors Found
- Check in the Allnet web UI if sensors are enabled
- View logs: **Settings**  **System**  **Logs**

## API Documentation

This integration uses the Allnet XML API:
- `/xml/?mode=info` - Device information
- `/xml/?mode=sensor&type=list` - List all sensors
- `/xml/?mode=actor&type=list` - List all actors
- `/xml/?mode=actor&id=X&action=1/0` - Control actor

### Resources
- [Allnet ALL3500 Product Page](https://www.allnet.de/produkte/neuheiten/p/all3500/)
- [Allnet ALL3073 Product Page](https://www.allnet.de/produkte/neuheiten/p/all3073/)
- [Allnet Support & Documentation](https://www.allnet.de/service/support/)

## Development

Contributions are welcome! This integration can serve as a foundation for an official Home Assistant integration.

### Structure
```
custom_components/allnet/
 __init__.py          # Integration setup
 config_flow.py       # Config flow (UI setup)
 const.py             # Constants
 allnet_api.py        # API client
 sensor.py            # Sensor platform
 switch.py            # Switch platform
 manifest.json        # Integration manifest
 strings.json         # UI strings
 translations/        # Translations
     de.json
     en.json
```

## License

MIT License

## Author

Created for the Home Assistant community

## Repository

https://github.com/Rothy/homeassistant-allnet

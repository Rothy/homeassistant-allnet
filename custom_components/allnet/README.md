# Allnet Integration für Home Assistant

Diese Custom Integration ermöglicht die automatische Integration von Allnet-Geräten (ALL3500, ALL3073, etc.) in Home Assistant.

## Features

✅ **Automatische Geräteerkennung**: Scannt automatisch alle verfügbaren Sensoren und Aktoren
✅ **Unterstützte Sensoren**:
   - Temperatur (°C/°F)
   - Luftfeuchtigkeit (%)
   - Luftdruck (hPa/Pa)
   - Weitere Sensoren werden automatisch erkannt

✅ **Unterstützte Aktoren**: Schalter/Relais (ein/aus)
✅ **Config Flow**: Einfache Einrichtung über die UI
✅ **Polling**: Automatische Updates alle 60 Sekunden

## Installation

### Manuelle Installation

1. Kopiere den Ordner `custom_components/allnet` in dein Home Assistant `config/custom_components/` Verzeichnis
2. Starte Home Assistant neu
3. Gehe zu Einstellungen → Geräte & Dienste → Integration hinzufügen
4. Suche nach "Allnet"
5. Gib die IP-Adresse, Benutzername und Passwort ein

### Über SSH/Terminal

```bash
# Kopiere die Integration
scp -r custom_components/allnet root@homeassistant.local:/config/custom_components/

# Oder per Terminal auf dem HA-System:
cd /config
mkdir -p custom_components
# ... dann Dateien kopieren
```

## Konfiguration

Nach der Installation:

1. **Einstellungen** → **Geräte & Dienste** → **Integration hinzufügen**
2. Suche nach **"Allnet"**
3. Gib folgende Daten ein:
   - **IP-Adresse**: z.B. `192.168.178.4`
   - **Benutzername**: z.B. `ha`
   - **Passwort**: Dein Gerätepasswort

Die Integration erkennt automatisch:
- Alle aktiven Sensoren (Temperatur, Luftfeuchtigkeit, Luftdruck, etc.)
- Alle verfügbaren Aktoren/Schalter

## Unterstützte Geräte

- Allnet ALL3500
- Allnet ALL3073
- Andere Allnet-Geräte mit XML-API

## Beispiel Automatisierung

```yaml
automation:
  - alias: "Mine einschalten bei hoher Temperatur"
    trigger:
      - platform: numeric_state
        entity_id: sensor.allnet_intern
        above: 25
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.allnet_mine
```

## Fehlerbehebung

### Verbindung fehlgeschlagen
- Prüfe IP-Adresse und Netzwerkverbindung
- Teste mit: `curl -u "ha:PASSWORT" "http://192.168.178.4/xml/?mode=info"`
- Prüfe Benutzername und Passwort

### Keine Sensoren/Aktoren gefunden
- Prüfe in der Allnet Web-UI, ob Sensoren aktiviert sind
- Logs anschauen: Einstellungen → System → Logs

## API-Dokumentation

Die Integration nutzt die XML-API von Allnet:
- `/xml/?mode=info` - Geräteinfo
- `/xml/?mode=sensor&id=X&simple` - Sensor auslesen
- `/xml/?mode=actor&id=X` - Aktor-Status
- `/xml/?mode=actor&id=X&action=1/0` - Aktor schalten

## Entwicklung

Beiträge sind willkommen! Diese Integration kann als Basis für eine offizielle Home Assistant Integration dienen.

### Struktur
```
custom_components/allnet/
├── __init__.py          # Integration Setup
├── config_flow.py       # Config Flow (UI Setup)
├── const.py             # Konstanten
├── allnet_api.py        # API Client
├── sensor.py            # Sensor Platform
├── switch.py            # Switch Platform
├── manifest.json        # Integration Manifest
├── strings.json         # UI Strings
└── translations/        # Übersetzungen
    ├── de.json
    └── en.json
```

## Lizenz

MIT License

## Autor

Erstellt für das Home Assistant Architekten-Projekt

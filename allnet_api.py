"""API Client for Allnet devices."""
import logging
import xml.etree.ElementTree as ET
from typing import Any

import httpx

_LOGGER = logging.getLogger(__name__)


class AllnetDevice:
    """Represent an Allnet device."""

    def __init__(self, host: str, username: str, password: str) -> None:
        """Initialize the Allnet device."""
        self.host = host
        self.username = username
        self.password = password
        self.base_url = f"http://{host}"

    def _make_request(self, endpoint: str) -> str:
        """Make HTTP request to device."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = httpx.get(
                url,
                auth=(self.username, self.password),
                timeout=10.0,
            )
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as err:
            _LOGGER.error("HTTP error occurred: %s", err)
            raise

    def get_device_info(self) -> dict[str, Any]:
        """Get device information."""
        response = self._make_request("/xml/?mode=info")
        root = ET.fromstring(response)
        
        info = {}
        hardware = root.find("hardware")
        if hardware is not None:
            info["model"] = hardware.findtext("model", "Unknown")
            info["mac"] = hardware.findtext("mac", "")
            info["revision"] = hardware.findtext("revision", "")
        
        info["firmware"] = root.findtext("firmware", "")
        
        device = root.find("device")
        if device is not None:
            info["name"] = device.findtext("name", "Allnet Device")
            info["uptime"] = device.findtext("uptime", "")
        
        return info

    def get_sensor(self, sensor_id: int) -> dict[str, Any] | None:
        """Get data for a specific sensor."""
        try:
            response = self._make_request(f"/xml/?mode=sensor&id={sensor_id}&simple")
            root = ET.fromstring(response)
            
            name = root.findtext("name", "").strip()
            current = root.findtext("current", "").strip()
            unit = root.findtext("unit", "").strip()
            
            # Skip disabled sensors or sensors without valid data
            if current in ("disabled", "", "no recorded value") or not name:
                return None
            
            return {
                "id": sensor_id,
                "name": name,
                "value": current,
                "unit": unit,
            }
        except Exception as err:
            _LOGGER.debug("Could not read sensor %d: %s", sensor_id, err)
            return None

    def get_all_sensors(self) -> list[dict[str, Any]]:
        """Discover and get all available sensors using list API."""
        sensors = []
        try:
            response = self._make_request("/xml/?mode=sensor&type=list")
            root = ET.fromstring(response)
            
            for sensor in root.findall("sensor"):
                sensor_id = int(sensor.findtext("id", "0"))
                name = sensor.findtext("name", "").strip()
                current = sensor.findtext("current", "").strip()
                unit = sensor.findtext("unit", "").strip()
                
                # Skip disabled sensors or sensors with errors/no data
                if current in ("disabled", "error", "", "no recorded value") or not name:
                    continue
                
                sensors.append({
                    "id": sensor_id,
                    "name": name,
                    "value": current,
                    "unit": unit,
                })
        except Exception as err:
            _LOGGER.error("Could not get sensor list: %s", err)
        
        return sensors

    def get_actor(self, actor_id: int) -> dict[str, Any] | None:
        """Get data for a specific actor."""
        try:
            response = self._make_request(f"/xml/?mode=actor&id={actor_id}")
            root = ET.fromstring(response)
            
            name = root.findtext("name", "").strip()
            state = root.findtext("state", "").strip()
            
            # Skip actors without valid data
            if not name or state == "":
                return None
            
            return {
                "id": actor_id,
                "name": name,
                "state": state,
            }
        except Exception as err:
            _LOGGER.debug("Could not read actor %d: %s", actor_id, err)
            return None

    def get_all_actors(self) -> list[dict[str, Any]]:
        """Discover and get all available actors using list API."""
        actors = []
        try:
            response = self._make_request("/xml/?mode=actor&type=list")
            root = ET.fromstring(response)
            
            for actor in root.findall("actor"):
                actor_id = int(actor.findtext("id", "0"))
                name = actor.findtext("name", "").strip()
                state = actor.findtext("state", "").strip()
                
                # Skip actors without valid data
                if not name or state == "":
                    continue
                
                actors.append({
                    "id": actor_id,
                    "name": name,
                    "state": state,
                })
        except Exception as err:
            _LOGGER.error("Could not get actor list: %s", err)
        
        return actors

    def set_actor(self, actor_id: int, state: bool) -> None:
        """Set actor state."""
        action = 1 if state else 0
        self._make_request(f"/xml/?mode=actor&id={actor_id}&action={action}")

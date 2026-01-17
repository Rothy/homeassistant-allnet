"""Support for Allnet sensors."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfPressure,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Allnet sensors from a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    device = hass.data[DOMAIN][config_entry.entry_id]["device"]

    entities = []
    
    if coordinator.data and "sensors" in coordinator.data:
        for sensor_data in coordinator.data["sensors"]:
            entities.append(AllnetSensor(coordinator, device, sensor_data))

    async_add_entities(entities)


class AllnetSensor(CoordinatorEntity, SensorEntity):
    """Representation of an Allnet sensor."""

    def __init__(self, coordinator, device, sensor_data: dict[str, Any]) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._sensor_id = sensor_data["id"]
        self._attr_name = f"Allnet {sensor_data['name']}"
        self._attr_unique_id = f"{device.host}_sensor_{self._sensor_id}"
        
        # Determine device class and unit based on sensor unit
        unit = sensor_data.get("unit", "").lower()
        
        if "°c" in unit or "c" == unit:
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
            self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        elif "°f" in unit or "f" == unit:
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
            self._attr_native_unit_of_measurement = UnitOfTemperature.FAHRENHEIT
        elif "%" in unit or "rh" in unit or "feucht" in sensor_data["name"].lower():
            self._attr_device_class = SensorDeviceClass.HUMIDITY
            self._attr_native_unit_of_measurement = PERCENTAGE
        elif "hpa" in unit or "mbar" in unit or "druck" in sensor_data["name"].lower():
            self._attr_device_class = SensorDeviceClass.PRESSURE
            self._attr_native_unit_of_measurement = UnitOfPressure.HPA
        elif "pa" in unit:
            self._attr_device_class = SensorDeviceClass.PRESSURE
            self._attr_native_unit_of_measurement = UnitOfPressure.PA
        else:
            self._attr_native_unit_of_measurement = sensor_data.get("unit", "")
        
        # Set state class for numeric sensors
        if self._attr_device_class:
            self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> float | str | None:
        """Return the state of the sensor."""
        if not self.coordinator.data or "sensors" not in self.coordinator.data:
            return None
        
        for sensor in self.coordinator.data["sensors"]:
            if sensor["id"] == self._sensor_id:
                try:
                    # Try to convert to float for numeric sensors
                    return float(sensor["value"])
                except (ValueError, TypeError):
                    # Return as string if not numeric
                    return sensor["value"]
        
        return None

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._device.host)},
            "name": f"Allnet Device {self._device.host}",
            "manufacturer": "Allnet",
            "model": "ALL3500",
        }

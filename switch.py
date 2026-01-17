"""Support for Allnet switches."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
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
    """Set up Allnet switches from a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    device = hass.data[DOMAIN][config_entry.entry_id]["device"]

    entities = []

    if coordinator.data and "actors" in coordinator.data:
        for actor_data in coordinator.data["actors"]:
            entities.append(AllnetSwitch(coordinator, device, actor_data))

    async_add_entities(entities)


class AllnetSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of an Allnet switch."""

    def __init__(self, coordinator, device, actor_data: dict[str, Any]) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._device = device
        self._actor_id = actor_data["id"]
        self._attr_name = f"Allnet {actor_data['name']}"
        self._attr_unique_id = f"{device.host}_actor_{self._actor_id}"

    @property
    def is_on(self) -> bool | None:
        """Return true if switch is on."""
        if not self.coordinator.data or "actors" not in self.coordinator.data:
            return None

        for actor in self.coordinator.data["actors"]:
            if actor["id"] == self._actor_id:
                # State can be "1" or "0" or boolean
                state = str(actor["state"]).lower()
                return state in ("1", "true", "on")

        return None

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self.hass.async_add_executor_job(
            self._device.set_actor, self._actor_id, True
        )
        # Wait for device to update state
        await asyncio.sleep(0.5)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self.hass.async_add_executor_job(
            self._device.set_actor, self._actor_id, False
        )
        # Wait for device to update state
        await asyncio.sleep(0.5)
        await self.coordinator.async_request_refresh()

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._device.host)},
            "name": f"Allnet Device {self._device.host}",
            "manufacturer": "Allnet",
            "model": "ALL3500",
        }

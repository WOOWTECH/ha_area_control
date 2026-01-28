"""The Area Control integration."""
from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.components import frontend
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PANEL_URL, PANEL_TITLE, PANEL_TITLE_ZH, PANEL_ICON, PANEL_VERSION
from .panel import async_register_websocket_commands

_LOGGER = logging.getLogger(__name__)


def _get_panel_title(hass: HomeAssistant) -> str:
    """Get panel title based on HA language setting."""
    language = hass.config.language or "en"
    if language.startswith("zh"):
        return PANEL_TITLE_ZH
    return PANEL_TITLE


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Area Control component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Area Control from a config entry."""
    _LOGGER.info("Setting up ha_area_control")

    # Register static path for frontend files
    frontend_path = Path(__file__).parent / "frontend"
    try:
        await hass.http.async_register_static_paths([
            StaticPathConfig(
                "/ha_area_control",
                str(frontend_path),
                cache_headers=False
            )
        ])
    except RuntimeError:
        _LOGGER.debug("Static path already registered, skipping")

    # Register sidebar panel
    if PANEL_URL not in hass.data.get("frontend_panels", {}):
        frontend.async_register_built_in_panel(
            hass,
            component_name="custom",
            sidebar_title=_get_panel_title(hass),
            sidebar_icon=PANEL_ICON,
            frontend_url_path=PANEL_URL,
            config={
                "_panel_custom": {
                    "name": "ha-area-control-panel",
                    "module_url": f"/ha_area_control/ha-area-control-panel.js?v={PANEL_VERSION}",
                }
            },
            require_admin=False,
        )

    # Register WebSocket commands
    await async_register_websocket_commands(hass)

    _LOGGER.info("ha_area_control setup complete")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Unloading ha_area_control")
    frontend.async_remove_panel(hass, PANEL_URL)
    return True

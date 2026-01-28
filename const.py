"""Constants for ha_area_control."""

DOMAIN = "ha_area_control"

# Permission Manager patterns
# Entity ID format: select.permission_manager_{user}_{resource_type}_{resource}
# We check for entities starting with this prefix
PERM_PREFIX = "select.permission_manager_"
PERM_AREA_TYPE = "area"

# Permission levels
PERM_CLOSED = 0
PERM_VIEW = 1
PERM_LIMITED = 2
PERM_EDIT = 3

# Panel configuration
PANEL_URL = "area-control"
PANEL_TITLE = "Area Control"
PANEL_TITLE_ZH = "分區控制"
PANEL_ICON = "mdi:floor-plan"
PANEL_VERSION = "1.2.1"

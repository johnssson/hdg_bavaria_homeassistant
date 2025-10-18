"""Entity Definitions for the HDG Bavaria Boiler integration.

This module serves as the central repository for defining the structure and
properties of all entities (sensors, numbers, etc.) that the HDG Bavaria Boiler
integration can create. The core of this module is the `SENSOR_DEFINITIONS`
dictionary, which maps specific HDG API node IDs and their characteristics to
corresponding Home Assistant entity configurations.
"""

from __future__ import annotations

__version__ = "0.1.15"

from typing import Final, cast

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    PERCENTAGE,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfPressure,
    UnitOfTemperature,
    UnitOfTime,
    UnitOfVolume,
)
from homeassistant.helpers.entity import EntityCategory

from .const import (
    POLLING_GROUP_DEFINITIONS,  # We will derive the keys from here
)
from .models import SensorDefinition  # Import from new models.py


#
# Entity Definition Factory Functions
#
# This section contains a set of "factory" functions designed to simplify the
# creation of entity definitions in the `SENSOR_DEFINITIONS` dictionary below.
# Instead of manually specifying every single parameter for each entity, you can
# use these helpers to create standardized entities with fewer lines of code.
#
# How to add a new entity:
# 1.  Identify the type of entity you want to add (e.g., a temperature sensor,
#     a percentage, a duration, an enum, a writable number, etc.).
# 2.  Choose the corresponding factory function (e.g., `create_temp_sensor`,
#     `create_percentage_sensor`, `create_number_entity`).
# 3.  Find the `SENSOR_DEFINITIONS` dictionary at the bottom of this file.
# 4.  Add a new entry. The key should be a unique identifier, which MUST match
#     the key you will add in the translation files (e.g., `en.json`).
# 5.  Call the chosen factory function as the value for your new key.
# 6.  Provide the required arguments, such as `key`, `node_id`, `polling_group`,
#     and `icon`. The factory function will handle the rest of the boilerplate.
#
# Example: Adding a new temperature sensor
#
#    "my_new_temp_sensor": create_temp_sensor(
#        key="my_new_temp_sensor",
#        node_id="12345T",  # The API node ID from the HDG documentation
#        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
#        icon="mdi:thermometer-plus",
#    ),
#
# If no specific factory function fits your needs, you can use the flexible
# `create_general_sensor` function, which allows you to specify all parameters
# manually. For highly unusual cases, you can fall back to the base
# `_create_sensor_definition` function.
#


def _create_sensor_definition(
    hdg_node_id: str,
    translation_key: str,
    polling_group: str,
    hdg_data_type: str,
    parse_as_type: str,
    ha_platform: str = "sensor",
    hdg_formatter: str | None = None,
    ha_device_class: SensorDeviceClass | None = None,
    ha_native_unit_of_measurement: str | None = None,
    ha_state_class: SensorStateClass | None = None,
    icon: str | None = None,
    writable: bool = False,  # Default to False
    entity_category: EntityCategory | None = None,
    setter_type: str | None = None,
    setter_min_val: float | None = None,
    setter_max_val: float | None = None,
    setter_step: float | None = None,
    options: list[str] | None = None,
    uppercase_value: bool | None = None,
) -> SensorDefinition:
    """Create a SensorDefinition dictionary. Avoid using directly."""
    definition: dict[str, object | None] = {
        "hdg_node_id": hdg_node_id,
        "translation_key": translation_key,
        "polling_group": polling_group,
        "hdg_data_type": hdg_data_type,
        "parse_as_type": parse_as_type,
        "ha_platform": ha_platform,
        "writable": writable,
    }
    # Add optional fields only if they are not None
    if hdg_formatter is not None:
        definition["hdg_formatter"] = hdg_formatter
    if ha_device_class is not None:
        definition["ha_device_class"] = ha_device_class
    if ha_native_unit_of_measurement is not None:
        definition["ha_native_unit_of_measurement"] = ha_native_unit_of_measurement
    if ha_state_class is not None:
        definition["ha_state_class"] = ha_state_class
    if icon is not None:
        definition["icon"] = icon
    if entity_category is not None:
        definition["entity_category"] = entity_category
    if setter_type is not None:
        definition["setter_type"] = setter_type
    if setter_min_val is not None:
        definition["setter_min_val"] = setter_min_val
    if setter_max_val is not None:
        definition["setter_max_val"] = setter_max_val
    if setter_step is not None:
        definition["setter_step"] = setter_step
    if options is not None:
        definition["options"] = options
    if uppercase_value is not None:
        definition["uppercase_value"] = uppercase_value
    return cast(SensorDefinition, definition)


def create_temp_sensor(
    key: str,
    node_id: str,
    polling_group: str,
    icon: str,
    entity_category: EntityCategory | None = None,
) -> SensorDefinition:
    """Create a standard temperature sensor in °C."""
    return _create_sensor_definition(
        hdg_node_id=node_id,
        translation_key=key,
        polling_group=polling_group,
        hdg_data_type="2",
        hdg_formatter="iTEMP",
        parse_as_type="float",
        ha_device_class=SensorDeviceClass.TEMPERATURE,
        ha_native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        ha_state_class=SensorStateClass.MEASUREMENT,
        icon=icon,
        entity_category=entity_category,
    )


def create_enum_sensor(
    key: str,
    node_id: str,
    polling_group: str,
    icon: str,
    entity_category: EntityCategory | None = None,
    ha_state_class: SensorStateClass | None = None,
) -> SensorDefinition:
    """Create a sensor for text values based on an ENUM type."""
    return _create_sensor_definition(
        hdg_node_id=node_id,
        translation_key=key,
        polling_group=polling_group,
        hdg_data_type="10",
        parse_as_type="enum_text",
        ha_device_class=SensorDeviceClass.ENUM,
        ha_state_class=ha_state_class,
        icon=icon,
        entity_category=entity_category,
    )


def create_diagnostic_enum_sensor(
    key: str,
    node_id: str,
    polling_group: str,
    icon: str,
) -> SensorDefinition:
    """Create a diagnostic sensor for text values based on an ENUM type."""
    return _create_sensor_definition(
        hdg_node_id=node_id,
        translation_key=key,
        polling_group=polling_group,
        hdg_data_type="10",
        parse_as_type="enum_text",
        ha_device_class=SensorDeviceClass.ENUM,
        ha_native_unit_of_measurement=None,
        ha_state_class=None,
        icon=icon,
        entity_category=EntityCategory.DIAGNOSTIC,
    )


def create_number_entity(
    key: str,
    node_id: str,
    polling_group: str,
    icon: str,
    setter_type: str,
    setter_min_val: float,
    setter_max_val: float,
    setter_step: float,
    ha_native_unit_of_measurement: str | None = None,
    ha_device_class: SensorDeviceClass | None = None,
    hdg_formatter: str | None = None,
    ha_state_class: SensorStateClass | None = SensorStateClass.MEASUREMENT,
) -> SensorDefinition:
    """Create a writable number entity."""
    return _create_sensor_definition(
        hdg_node_id=node_id,
        translation_key=key,
        polling_group=polling_group,
        hdg_data_type="2",
        parse_as_type="float",
        ha_platform="number",
        writable=True,
        entity_category=EntityCategory.CONFIG,
        icon=icon,
        setter_type=setter_type,
        setter_min_val=setter_min_val,
        setter_max_val=setter_max_val,
        setter_step=setter_step,
        ha_native_unit_of_measurement=ha_native_unit_of_measurement,
        ha_device_class=ha_device_class,
        hdg_formatter=hdg_formatter,
        ha_state_class=ha_state_class,
    )


def create_percentage_sensor(
    key: str,
    node_id: str,
    polling_group: str,
    icon: str,
    ha_state_class: SensorStateClass | None = SensorStateClass.MEASUREMENT,
    entity_category: EntityCategory | None = None,
    ha_device_class: SensorDeviceClass | None = None,
) -> SensorDefinition:
    """Create a standard percentage sensor."""
    return _create_sensor_definition(
        hdg_node_id=node_id,
        translation_key=key,
        polling_group=polling_group,
        hdg_data_type="2",
        parse_as_type="float",
        hdg_formatter="iPERC",
        ha_native_unit_of_measurement=PERCENTAGE,
        ha_state_class=ha_state_class,
        icon=icon,
        entity_category=entity_category,
        ha_device_class=ha_device_class,
    )


def create_duration_sensor(
    key: str,
    node_id: str,
    polling_group: str,
    icon: str,
    hdg_formatter: str,
    unit: str,
    ha_state_class: SensorStateClass | None = SensorStateClass.MEASUREMENT,
    entity_category: EntityCategory | None = None,
) -> SensorDefinition:
    """Create a sensor for time duration."""
    return _create_sensor_definition(
        hdg_node_id=node_id,
        translation_key=key,
        polling_group=polling_group,
        hdg_data_type="2",
        parse_as_type="float",
        hdg_formatter=hdg_formatter,
        ha_device_class=SensorDeviceClass.DURATION,
        ha_native_unit_of_measurement=unit,
        ha_state_class=ha_state_class,
        icon=icon,
        entity_category=entity_category,
    )


def create_energy_sensor(
    key: str,
    node_id: str,
    polling_group: str,
    icon: str,
    hdg_formatter: str,
    unit: str,
    ha_state_class: SensorStateClass | None = SensorStateClass.MEASUREMENT,
    entity_category: EntityCategory | None = None,
    ha_device_class: SensorDeviceClass | None = SensorDeviceClass.ENERGY,
) -> SensorDefinition:
    """Create a sensor for energy consumption."""
    return _create_sensor_definition(
        hdg_node_id=node_id,
        translation_key=key,
        polling_group=polling_group,
        hdg_data_type="2",
        parse_as_type="float",
        hdg_formatter=hdg_formatter,
        ha_device_class=ha_device_class,
        ha_native_unit_of_measurement=unit,
        ha_state_class=ha_state_class,
        icon=icon,
        entity_category=entity_category,
    )


def create_text_sensor(
    key: str,
    node_id: str,
    polling_group: str,
    icon: str,
    parse_as_type: str = "text",
    entity_category: EntityCategory | None = None,
    ha_state_class: SensorStateClass | None = None,
) -> SensorDefinition:
    """Create a sensor for plain text values."""
    return _create_sensor_definition(
        hdg_node_id=node_id,
        translation_key=key,
        polling_group=polling_group,
        hdg_data_type="4",
        parse_as_type=parse_as_type,
        icon=icon,
        entity_category=entity_category,
        ha_state_class=ha_state_class,
    )


def create_diagnostic_text_sensor(
    key: str,
    node_id: str,
    polling_group: str,
    icon: str,
    parse_as_type: str = "text",
) -> SensorDefinition:
    """Create a diagnostic sensor for plain text values."""
    return _create_sensor_definition(
        hdg_node_id=node_id,
        translation_key=key,
        polling_group=polling_group,
        hdg_data_type="4",
        parse_as_type=parse_as_type,
        ha_device_class=None,
        ha_native_unit_of_measurement=None,
        icon=icon,
        entity_category=EntityCategory.DIAGNOSTIC,
    )


def create_pressure_sensor(
    key: str,
    node_id: str,
    polling_group: str,
    icon: str,
    entity_category: EntityCategory | None = None,
) -> SensorDefinition:
    """Create a pressure sensor in Pascals."""
    return _create_sensor_definition(
        hdg_node_id=node_id,
        translation_key=key,
        polling_group=polling_group,
        hdg_data_type="2",
        parse_as_type="float",
        hdg_formatter="iPASCAL",
        ha_device_class=SensorDeviceClass.PRESSURE,
        ha_native_unit_of_measurement=UnitOfPressure.PA,
        ha_state_class=SensorStateClass.MEASUREMENT,
        icon=icon,
        entity_category=entity_category,
    )


def create_kelvin_sensor(
    key: str,
    node_id: str,
    polling_group: str,
    icon: str,
    entity_category: EntityCategory | None = None,
) -> SensorDefinition:
    """Create a sensor for temperature difference in Kelvin."""
    return _create_sensor_definition(
        hdg_node_id=node_id,
        translation_key=key,
        polling_group=polling_group,
        hdg_data_type="2",
        parse_as_type="float",
        hdg_formatter="iKELV",
        ha_native_unit_of_measurement=UnitOfTemperature.KELVIN,
        ha_state_class=SensorStateClass.MEASUREMENT,
        icon=icon,
        entity_category=entity_category,
    )


def create_general_sensor(
    key: str,
    node_id: str,
    polling_group: str,
    hdg_data_type: str,
    parse_as_type: str,
    icon: str,
    hdg_formatter: str | None = None,
    ha_device_class: SensorDeviceClass | None = None,
    ha_native_unit_of_measurement: str | None = None,
    ha_state_class: SensorStateClass | None = None,
    entity_category: EntityCategory | None = None,
) -> SensorDefinition:
    """Create a general-purpose sensor for cases not covered by other factories."""
    return _create_sensor_definition(
        hdg_node_id=node_id,
        translation_key=key,
        polling_group=polling_group,
        hdg_data_type=hdg_data_type,
        parse_as_type=parse_as_type,
        hdg_formatter=hdg_formatter,
        ha_device_class=ha_device_class,
        ha_native_unit_of_measurement=ha_native_unit_of_measurement,
        ha_state_class=ha_state_class,
        icon=icon,
        entity_category=entity_category,
    )


def create_version_sensor(
    key: str,
    node_id: str,
    polling_group: str,
    icon: str,
) -> SensorDefinition:
    """Create a sensor for software/firmware version information."""
    return _create_sensor_definition(
        hdg_node_id=node_id,
        translation_key=key,
        polling_group=polling_group,
        hdg_data_type="2",
        parse_as_type="text",
        hdg_formatter="iVERSION",
        ha_device_class=None,
        ha_native_unit_of_measurement=None,
        ha_state_class=None,
        icon=icon,
        entity_category=EntityCategory.DIAGNOSTIC,
    )


def create_select_entity(
    key: str,
    node_id: str,
    polling_group: str,
    icon: str,
    options: list[str],
    entity_category: EntityCategory | None = None,
    uppercase_value: bool | None = None,
) -> SensorDefinition:
    """Create a writable select entity."""
    return _create_sensor_definition(
        hdg_node_id=node_id,
        translation_key=key,
        polling_group=polling_group,
        hdg_data_type="10",  # Assuming ENUM type for select
        parse_as_type="enum_text",
        ha_platform="select",
        writable=True,
        entity_category=entity_category,
        icon=icon,
        options=options,
        uppercase_value=uppercase_value,
        ha_device_class=SensorDeviceClass.ENUM,
    )


POLLING_GROUP_KEYS: dict[str, str] = {
    f"POLLING_GROUP_{i + 1}": group["key"]  # type: ignore[misc]
    for i, group in enumerate(POLLING_GROUP_DEFINITIONS)
}

# Master dictionary defining all sensors and entities for the integration.
# Each key is a unique string identifier for the entity, typically matching its `translation_key`.
# The value is a `SensorDefinition` TypedDict (defined in `models.py`) which specifies:
#   - `hdg_node_id`: The raw ID used by the HDG API (e.g., "22003T").
#   - `translation_key`: Used for localization of names and other UI elements.
#   - `hdg_data_type`, `hdg_formatter`, `hdg_enum_type`: Info from HDG API about the node.
#   - `ha_platform`: The Home Assistant platform (e.g., "sensor", "number").
#   - `ha_device_class`, `ha_native_unit_of_measurement`, `ha_state_class`, `icon`, `entity_category`: HA entity properties.
#   - `writable`: Boolean, true if the node's value can be set.
#   - `parse_as_type`: Hint for how to parse the raw string value from the API.
# Each key is a unique identifier (often matching the translation_key) for the entity.
SENSOR_DEFINITIONS: Final[dict[str, SensorDefinition]] = {
    "sprache": create_enum_sensor(
        key="sprache",
        node_id="1T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:translate",
    ),
    "bauart": create_enum_sensor(
        key="bauart",
        node_id="2T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:tools",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "kesseltyp_kennung": create_enum_sensor(
        key="kesseltyp_kennung",
        node_id="3T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:tag-text-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "stromnetz": create_enum_sensor(
        key="stromnetz",
        node_id="4T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:power-plug-outline",
    ),
    "brennstoff": create_enum_sensor(
        key="brennstoff",
        node_id="6T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:pine-tree-fire",
    ),
    "automatische_zeitumstellung": create_enum_sensor(
        key="automatische_zeitumstellung",
        node_id="9T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:clock-time-eleven-outline",
    ),
    "einstiegsbild": create_enum_sensor(
        key="einstiegsbild",
        node_id="11T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:television-guide",
    ),
    "holzart": create_enum_sensor(
        key="holzart",
        node_id="13T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:tree-outline",
    ),
    "holzfeuchte": create_enum_sensor(
        key="holzfeuchte",
        node_id="14T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:water-percent",
    ),
    "automatische_zundung_aktivieren": create_enum_sensor(
        key="automatische_zundung_aktivieren",
        node_id="15T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:auto-fix",
    ),
    "auto_zundung_webcontrol_erlauben": create_enum_sensor(
        key="auto_zundung_webcontrol_erlauben",
        node_id="16T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:web-check",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "objektwarmebedarf": create_general_sensor(
        key="objektwarmebedarf",
        node_id="17T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        hdg_data_type="2",
        parse_as_type="float",
        hdg_formatter="iKW",
        ha_device_class=SensorDeviceClass.POWER,
        ha_native_unit_of_measurement=UnitOfPower.KILO_WATT,
        ha_state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:radiator",
    ),
    "minimale_nachlegemenge": create_percentage_sensor(
        key="minimale_nachlegemenge",
        node_id="18T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:basket-minus-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "nachlegeschritt_text": create_text_sensor(
        key="nachlegeschritt_text",
        node_id="19T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:stairs-up",
    ),
    "nachlegeschritt": create_percentage_sensor(
        key="nachlegeschritt",
        node_id="19T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:stairs",
    ),
    "nachlege_benachrichtigung": create_enum_sensor(
        key="nachlege_benachrichtigung",
        node_id="20T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:basket-clock",
    ),
    "offset_aussenfuhler": create_temp_sensor(
        key="offset_aussenfuhler",
        node_id="36T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:thermometer-offset",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "kesseltemperatur_sollwert_param": create_temp_sensor(
        key="kesseltemperatur_sollwert_param",
        node_id="2113T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:thermometer-lines",
    ),
    "frostschutzprogramm_aktivieren": create_enum_sensor(
        key="frostschutzprogramm_aktivieren",
        node_id="2114T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:snowflake-thermometer",
    ),
    "frostschutz_zirkulation_at_kleiner": create_temp_sensor(
        key="frostschutz_zirkulation_at_kleiner",
        node_id="2115T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:snowflake-alert",
    ),
    "frostschutz_rlt_kleiner": create_temp_sensor(
        key="frostschutz_rlt_kleiner",
        node_id="2116T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:snowflake-alert",
    ),
    "frostschutz_rlt_groesser": create_temp_sensor(
        key="frostschutz_rlt_groesser",
        node_id="2117T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:snowflake-check",
    ),
    "offset_kesseltemperatur_soll_maximum": create_kelvin_sensor(
        key="offset_kesseltemperatur_soll_maximum",
        node_id="2123T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:thermometer-plus",
    ),
    "anzunden_zeitdauer": create_duration_sensor(
        key="anzunden_zeitdauer",
        node_id="2302T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:timer-fire",
        hdg_formatter="iMIN",
        unit=UnitOfTime.MINUTES,
    ),
    "anzunden_primarluft": create_percentage_sensor(
        key="anzunden_primarluft",
        node_id="2303T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:weather-windy",
    ),
    "anzunden_sekundarluft": create_percentage_sensor(
        key="anzunden_sekundarluft",
        node_id="2304T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:weather-windy-variant",
    ),
    "anheizen_zeitdauer": create_duration_sensor(
        key="anheizen_zeitdauer",
        node_id="2306T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:fire-clock",
        hdg_formatter="iMIN",
        unit=UnitOfTime.MINUTES,
    ),
    "auto_zundung_einschaltverzogerung": create_duration_sensor(
        key="auto_zundung_einschaltverzogerung",
        node_id="2320T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:timer-cog-outline",
        hdg_formatter="iMIN",
        unit=UnitOfTime.MINUTES,
    ),
    "ausbrennen_primarluft": create_percentage_sensor(
        key="ausbrennen_primarluft",
        node_id="2402T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:air-filter",
    ),
    "ausbrennen_sekundarluft": create_percentage_sensor(
        key="ausbrennen_sekundarluft",
        node_id="2403T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:air-filter",
    ),
    "ausbrennen_bezugsgrosse": create_enum_sensor(
        key="ausbrennen_bezugsgrosse",
        node_id="2407T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:axis-arrow",
    ),
    "festwertvorgabe_primarluft": create_percentage_sensor(
        key="festwertvorgabe_primarluft",
        node_id="2603T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:tune-variant",
    ),
    "festwertvorgabe_sekundarluft": create_percentage_sensor(
        key="festwertvorgabe_sekundarluft",
        node_id="2604T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_3"],
        icon="mdi:tune-variant",
    ),
    "pid3_o2_sekundarluft_minimum": create_percentage_sensor(
        key="pid3_o2_sekundarluft_minimum",
        node_id="2623T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:arrow-collapse-down",
    ),
    "pid3_o2_sekundarluft_maximum": create_percentage_sensor(
        key="pid3_o2_sekundarluft_maximum",
        node_id="2624T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:arrow-collapse-up",
    ),
    "rucklaufmischer_laufzeit_gesamt": create_duration_sensor(
        key="rucklaufmischer_laufzeit_gesamt",
        node_id="2805T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:timer-sync-outline",
        hdg_formatter="iSEK",
        unit=UnitOfTime.SECONDS,
        ha_state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "pid_sollwert_rucklauf_spreizung_minimum": create_kelvin_sensor(
        key="pid_sollwert_rucklauf_spreizung_minimum",
        node_id="2813T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:thermometer-minus",
    ),
    "restwarmenutzung_puffer_bezug": create_enum_sensor(
        key="restwarmenutzung_puffer_bezug",
        node_id="2816T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:heat-wave",
    ),
    "freigabe_kesseltemperatur": create_temp_sensor(
        key="freigabe_kesseltemperatur",
        node_id="2901T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:thermometer-check",
    ),
    "freigabe_abgastemperatur": create_temp_sensor(
        key="freigabe_abgastemperatur",
        node_id="2904T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:thermometer-high",
    ),
    "puffer_1_bezeichnung": create_diagnostic_text_sensor(
        key="puffer_1_bezeichnung",
        node_id="4020T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:information-outline",
    ),
    "puffer_1_ladung_abbruch_temperatur_oben": create_temp_sensor(
        key="puffer_1_ladung_abbruch_temperatur_oben",
        node_id="4033T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:thermometer-off",
    ),
    "puffer_1_fuhler_quelle": create_enum_sensor(
        key="puffer_1_fuhler_quelle",
        node_id="4036T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:thermometer-lines",
    ),
    "puffer_1_energieberechnung_aktivieren": create_enum_sensor(
        key="puffer_1_energieberechnung_aktivieren",
        node_id="4060T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:calculator-variant-outline",
    ),
    "puffer_1_temperatur_kalt": create_temp_sensor(
        key="puffer_1_temperatur_kalt",
        node_id="4061T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:thermometer-low",
    ),
    "puffer_1_temperatur_warm": create_temp_sensor(
        key="puffer_1_temperatur_warm",
        node_id="4062T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:thermometer-high",
    ),
    "puffer_1_nachlegemenge_optimieren": create_enum_sensor(
        key="puffer_1_nachlegemenge_optimieren",
        node_id="4064T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:basket-check-outline",
    ),
    "puffer_1_grosse": create_general_sensor(
        key="puffer_1_grosse",
        node_id="4065T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        hdg_data_type="1",
        parse_as_type="float",
        hdg_formatter="iLITER",
        ha_device_class=SensorDeviceClass.VOLUME,
        ha_native_unit_of_measurement=UnitOfVolume.LITERS,
        ha_state_class=None,
        icon="mdi:propane-tank",
    ),
    "puffer_1_umladesystem_aktivieren": create_enum_sensor(
        key="puffer_1_umladesystem_aktivieren",
        node_id="4070T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:sync-circle",
    ),
    "puffer_1_beladeventil_aktivieren": create_enum_sensor(
        key="puffer_1_beladeventil_aktivieren",
        node_id="4090T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:valve-check",
    ),
    "puffer_1_zonenventil_aktivieren": create_enum_sensor(
        key="puffer_1_zonenventil_aktivieren",
        node_id="4091T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:valve-check",
    ),
    "puffer_1_y2_ventil_aktivieren": create_enum_sensor(
        key="puffer_1_y2_ventil_aktivieren",
        node_id="4095T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:valve-check",
    ),
    "puffer_art": create_enum_sensor(
        key="puffer_art",
        node_id="4099T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:propane-tank-outline",
    ),
    "hk1_system": create_enum_sensor(
        key="hk1_system",
        node_id="6020T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:radiator-disabled",
    ),
    "hk1_bezeichnung": create_diagnostic_text_sensor(
        key="hk1_bezeichnung",
        node_id="6021T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:label-outline",
    ),
    "hk1_soll_normal": create_number_entity(
        key="hk1_soll_normal",
        node_id="6022T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:home-thermometer",
        setter_type="int",
        setter_min_val=0.0,
        setter_max_val=90.0,
        setter_step=1.0,
        ha_device_class=SensorDeviceClass.TEMPERATURE,
        ha_native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        hdg_formatter="iTEMP",
        ha_state_class=SensorStateClass.MEASUREMENT,
    ),
    "hk1_soll_absenk": create_number_entity(
        key="hk1_soll_absenk",
        node_id="6023T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:home-thermometer-outline",
        setter_type="int",
        setter_min_val=0.0,
        setter_max_val=90.0,
        setter_step=1.0,
        ha_device_class=SensorDeviceClass.TEMPERATURE,
        ha_native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        hdg_formatter="iTEMP",
        ha_state_class=SensorStateClass.MEASUREMENT,
    ),
    "hk1_parallelverschiebung": create_number_entity(
        key="hk1_parallelverschiebung",
        node_id="6024T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_2"],
        icon="mdi:arrow-up-down",
        setter_type="int",
        setter_min_val=-20.0,
        setter_max_val=20.0,
        setter_step=1.0,
        ha_native_unit_of_measurement=UnitOfTemperature.KELVIN,
        hdg_formatter="iKELV",
        ha_state_class=SensorStateClass.MEASUREMENT,
    ),
    "hk1_raumeinflussfaktor": create_general_sensor(
        key="hk1_raumeinflussfaktor",
        node_id="6025T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_2"],
        hdg_data_type="2",
        parse_as_type="float",
        ha_state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:home-import-outline",
    ),
    "hk1_steilheit": create_number_entity(
        key="hk1_steilheit",
        node_id="6026T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_2"],
        icon="mdi:chart-line-variant",
        setter_type="float1",
        setter_min_val=0.1,
        setter_max_val=3.5,
        setter_step=0.1,
        ha_native_unit_of_measurement=None,
        ha_state_class=SensorStateClass.MEASUREMENT,
    ),
    "hk1_vorlauftemperatur_minimum": create_temp_sensor(
        key="hk1_vorlauftemperatur_minimum",
        node_id="6027T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:thermometer-minus",
    ),
    "hk1_vorlauftemperatur_maximum": create_temp_sensor(
        key="hk1_vorlauftemperatur_maximum",
        node_id="6028T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:thermometer-plus",
    ),
    "hk1_raumeinheit_status": create_enum_sensor(
        key="hk1_raumeinheit_status",
        node_id="6029T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:remote",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "hk1_offset_raumfuhler": create_kelvin_sensor(
        key="hk1_offset_raumfuhler",
        node_id="6030T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:thermometer-offset",
    ),
    "hk1_warmequelle": create_enum_sensor(
        key="hk1_warmequelle",
        node_id="6039T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:radiator-outline",
    ),
    "hk1_mischerlaufzeit_maximum": create_duration_sensor(
        key="hk1_mischerlaufzeit_maximum",
        node_id="6041T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:timer-settings-outline",
        hdg_formatter="iSEK",
        unit=UnitOfTime.SECONDS,
    ),
    "hk1_pumpe_ein_freigabetemperatur": create_temp_sensor(
        key="hk1_pumpe_ein_freigabetemperatur",
        node_id="6046T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:pump-outline",
    ),
    "hk1_pumpe_aus_aussentemperatur": create_number_entity(
        key="hk1_pumpe_aus_aussentemperatur",
        node_id="6047T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:pump-off-outline",
        setter_type="int",
        setter_min_val=0.0,
        setter_max_val=50.0,
        setter_step=1.0,
        ha_device_class=SensorDeviceClass.TEMPERATURE,
        ha_native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        hdg_formatter="iTEMP",
        ha_state_class=SensorStateClass.MEASUREMENT,
    ),
    "hk1_frostschutz_temp": create_temp_sensor(
        key="hk1_frostschutz_temp",
        node_id="6048T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:snowflake-thermometer",
    ),
    "hk1_eco_absenken_aus_aussentemperatur": create_number_entity(
        key="hk1_eco_absenken_aus_aussentemperatur",
        node_id="6049T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:leaf-thermometer",
        setter_type="int",
        setter_min_val=0.0,
        setter_max_val=50.0,
        setter_step=1.0,
        ha_device_class=SensorDeviceClass.TEMPERATURE,
        ha_native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        hdg_formatter="iTEMP",
        ha_state_class=SensorStateClass.MEASUREMENT,
    ),
    "hk1_heizgrenze_sommer": create_temp_sensor(
        key="hk1_heizgrenze_sommer",
        node_id="6050T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:weather-sunny-alert",
    ),
    "hk1_heizgrenze_winter": create_temp_sensor(
        key="hk1_heizgrenze_winter",
        node_id="6051T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:weather-snowy-heavy",
    ),
    "hk1_restwarme_aufnehmen": create_enum_sensor(
        key="hk1_restwarme_aufnehmen",
        node_id="6067T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:heat-wave",
    ),
    "aussentemperatur": create_temp_sensor(
        key="aussentemperatur",
        node_id="20000T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:thermometer",
    ),
    "software_version_touch": create_version_sensor(
        key="software_version_touch",
        node_id="20003T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:chip",
    ),
    "anlagenbezeichnung_sn": create_diagnostic_text_sensor(
        key="anlagenbezeichnung_sn",
        node_id="20026T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:tag",
    ),
    "mac_adresse": create_diagnostic_text_sensor(
        key="mac_adresse",
        node_id="20031T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:network-outline",
    ),
    "anlage_betriebsart": create_enum_sensor(
        key="anlage_betriebsart",
        node_id="20032T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:home-automation",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "anlage_status_text": create_enum_sensor(
        key="anlage_status_text",
        node_id="20033T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:power-settings",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "software_version_fa": create_version_sensor(
        key="software_version_fa",
        node_id="20036T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:chip",
    ),
    "extra_version_info": create_diagnostic_text_sensor(
        key="extra_version_info",
        node_id="20037T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:information-outline",
        parse_as_type="allow_empty_string",
    ),
    "hydraulikschema_nummer": create_diagnostic_text_sensor(
        key="hydraulikschema_nummer",
        node_id="20039T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:hydraulic-oil-level",
    ),
    "brennraumtemperatur_soll": create_temp_sensor(
        key="brennraumtemperatur_soll",
        node_id="22000T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:thermometer-lines",
    ),
    "kessel_abgastemperatur_ist": create_temp_sensor(
        key="kessel_abgastemperatur_ist",
        node_id="22001T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:thermometer-high",
    ),
    "kessel_restsauerstoff_ist": create_percentage_sensor(
        key="kessel_restsauerstoff_ist",
        node_id="22002T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:molecule-co2",
    ),
    "kesseltemperatur_ist": create_temp_sensor(
        key="kesseltemperatur_ist",
        node_id="22003T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:thermometer",
    ),
    "kessel_rucklauftemperatur_ist": create_temp_sensor(
        key="kessel_rucklauftemperatur_ist",
        node_id="22004T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:thermometer-water",
    ),
    "materialmenge_aktuell": create_percentage_sensor(
        key="materialmenge_aktuell",
        node_id="22005T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:gauge",
    ),
    "primarluftklappe_ist": create_percentage_sensor(
        key="primarluftklappe_ist",
        node_id="22008T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:valve",
    ),
    "sekundarluftklappe_ist": create_percentage_sensor(
        key="sekundarluftklappe_ist",
        node_id="22009T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:valve",
    ),
    "kessel_status": create_enum_sensor(
        key="kessel_status",
        node_id="22010T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:fire",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "kessel_betriebsstunden": create_duration_sensor(
        key="kessel_betriebsstunden",
        node_id="22011T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:timer-outline",
        hdg_formatter="iSTD",
        unit=UnitOfTime.HOURS,
        ha_state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "laufzeit_wt_reinigung": create_duration_sensor(
        key="laufzeit_wt_reinigung",
        node_id="22012T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:broom",
        hdg_formatter="iSTD",
        unit=UnitOfTime.HOURS,
        ha_state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "laufzeit_entaschung": create_duration_sensor(
        key="laufzeit_entaschung",
        node_id="22013T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:delete-sweep-outline",
        hdg_formatter="iSTD",
        unit=UnitOfTime.HOURS,
        ha_state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "laufzeit_hauptgeblase": create_duration_sensor(
        key="laufzeit_hauptgeblase",
        node_id="22014T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:fan-clock",
        hdg_formatter="iSTD",
        unit=UnitOfTime.HOURS,
        ha_state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "laufzeit_zundgeblase": create_duration_sensor(
        key="laufzeit_zundgeblase",
        node_id="22015T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:fan-plus",
        hdg_formatter="iSTD",
        unit=UnitOfTime.HOURS,
        ha_state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "anzahl_rostkippungen": create_general_sensor(
        key="anzahl_rostkippungen",
        node_id="22016T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        hdg_data_type="2",
        parse_as_type="float",
        ha_state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:recycle-variant",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "primarluftklappe_soll": create_percentage_sensor(
        key="primarluftklappe_soll",
        node_id="22019T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:valve-closed",
    ),
    "kessel_haupt_betriebsart": create_enum_sensor(
        key="kessel_haupt_betriebsart",
        node_id="22020T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_2"],
        icon="mdi:cogs",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "kessel_externe_anforderung": create_percentage_sensor(
        key="kessel_externe_anforderung",
        node_id="22021T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:call-made",
    ),
    "kesselvorlauf_solltemperatur": create_temp_sensor(
        key="kesselvorlauf_solltemperatur",
        node_id="22022T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:thermometer-chevron-up",
    ),
    "kesselrucklauf_solltemperatur": create_temp_sensor(
        key="kesselrucklauf_solltemperatur",
        node_id="22023T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:thermometer-water",
    ),
    "kesselleistung_ist": create_percentage_sensor(
        key="kesselleistung_ist",
        node_id="22024T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:fire-circle",
    ),
    "kessel_restlaufzeit_wartung": create_duration_sensor(
        key="kessel_restlaufzeit_wartung",
        node_id="22025T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:wrench-clock",
        hdg_formatter="iSTD",
        unit=UnitOfTime.HOURS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "kessel_betriebsphase_text": create_enum_sensor(
        key="kessel_betriebsphase_text",
        node_id="22026T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_2"],
        icon="mdi:state-machine",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "kessel_wirkungsgrad": create_percentage_sensor(
        key="kessel_wirkungsgrad",
        node_id="22028T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:chart-bell-curve-cumulative",
    ),
    "kessel_ausbrandgrund": create_enum_sensor(
        key="kessel_ausbrandgrund",
        node_id="22029T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_2"],
        icon="mdi:fire-alert",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "kessel_saugzuggeblase_ist": create_percentage_sensor(
        key="kessel_saugzuggeblase_ist",
        node_id="22030T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:fan",
    ),
    "kessel_unterdruck_ist": create_pressure_sensor(
        key="kessel_unterdruck_ist",
        node_id="22031T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:gauge-low",
    ),
    "sekundarluftklappe_soll": create_percentage_sensor(
        key="sekundarluftklappe_soll",
        node_id="22033T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:valve-closed",
    ),
    "betriebsstunden_rostmotor": create_duration_sensor(
        key="betriebsstunden_rostmotor",
        node_id="22037T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:cog-counterclockwise",
        hdg_formatter="iSTD",
        unit=UnitOfTime.HOURS,
        ha_state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "betriebsstunden_stokerschnecke": create_duration_sensor(
        key="betriebsstunden_stokerschnecke",
        node_id="22038T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:screw-lag",
        hdg_formatter="iSTD",
        unit=UnitOfTime.HOURS,
        ha_state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "betriebsstunden_ascheschnecke": create_duration_sensor(
        key="betriebsstunden_ascheschnecke",
        node_id="22039T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:screw-lag",
        hdg_formatter="iSTD",
        unit=UnitOfTime.HOURS,
        ha_state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "restlaufzeit_schornsteinfeger": create_duration_sensor(
        key="restlaufzeit_schornsteinfeger",
        node_id="22040T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:account-hard-hat-outline",
        hdg_formatter="iMIN",
        unit=UnitOfTime.MINUTES,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "kessel_typ_info_leer": create_diagnostic_text_sensor(
        key="kessel_typ_info_leer",
        node_id="22041T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:information-off-outline",
        parse_as_type="allow_empty_string",
    ),
    "kessel_rucklaufmischer": create_percentage_sensor(
        key="kessel_rucklaufmischer",
        node_id="22043T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:valve-open",
    ),
    "abgasleitwert_ist": create_kelvin_sensor(
        key="abgasleitwert_ist",
        node_id="22044T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:delta",
    ),
    "kessel_restsauerstoff_korr": create_percentage_sensor(
        key="kessel_restsauerstoff_korr",
        node_id="22045T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:molecule-co2",
    ),
    "primarluft_korrektur_o2": create_enum_sensor(
        key="primarluft_korrektur_o2",
        node_id="22046T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:air-filter",
    ),
    "abgasleitwert_soll": create_kelvin_sensor(
        key="abgasleitwert_soll",
        node_id="22049T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:delta",
    ),
    "kessel_o2_sollwert": create_percentage_sensor(
        key="kessel_o2_sollwert",
        node_id="22050T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:target-variant",
    ),
    "kessel_nachlegemenge": create_percentage_sensor(
        key="kessel_nachlegemenge",
        node_id="22052T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:basket-fill",
    ),
    "kessel_nachlegezeitpunkt_2": create_general_sensor(
        key="kessel_nachlegezeitpunkt_2",
        node_id="22053T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        hdg_data_type="2",
        parse_as_type="hdg_datetime_or_text",
        hdg_formatter="iRSINLM",
        ha_device_class=SensorDeviceClass.TIMESTAMP,
        icon="mdi:clock-alert-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "kessel_energieverbrauch_tag_gesamt": create_energy_sensor(
        key="kessel_energieverbrauch_tag_gesamt",
        node_id="22054T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:lightning-bolt",
        hdg_formatter="iKWH",
        unit=UnitOfEnergy.KILO_WATT_HOUR,
        ha_state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "kessel_nachlegebedarf": create_percentage_sensor(
        key="kessel_nachlegebedarf",
        node_id="22057T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:basket-unfill",
    ),
    "kessel_nachlegen_anzeige_text": create_diagnostic_enum_sensor(
        key="kessel_nachlegen_anzeige_text",
        node_id="22062T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:basket-alert-outline",
    ),
    "zeit_kesseluberhitzung_10_abbrande_std": create_duration_sensor(
        key="zeit_kesseluberhitzung_10_abbrande_std",
        node_id="22064T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:timer-alert-outline",
        hdg_formatter="iSTD",
        unit=UnitOfTime.HOURS,
        ha_state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "zeit_kesseluberhitzung_10_abbrande_prozent": create_percentage_sensor(
        key="zeit_kesseluberhitzung_10_abbrande_prozent",
        node_id="22065T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:alert-circle-check-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "zeit_kesseluberhitzung_gesamt_std": create_duration_sensor(
        key="zeit_kesseluberhitzung_gesamt_std",
        node_id="22066T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:timer-alert",
        hdg_formatter="iSTD",
        unit=UnitOfTime.HOURS,
        ha_state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "zeit_kesseluberhitzung_gesamt_prozent": create_percentage_sensor(
        key="zeit_kesseluberhitzung_gesamt_prozent",
        node_id="22067T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:alert-circle-check",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "stillstandszeit_soll": create_duration_sensor(
        key="stillstandszeit_soll",
        node_id="22068T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:timer-sand",
        hdg_formatter="iSTD",
        unit=UnitOfTime.HOURS,
    ),
    "kessel_warmemenge_gesamt": create_energy_sensor(
        key="kessel_warmemenge_gesamt",
        node_id="22069T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:lightning-bolt-circle",
        hdg_formatter="iMWH",
        unit=UnitOfEnergy.MEGA_WATT_HOUR,
        ha_state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "kessel_stillstandszeit": create_duration_sensor(
        key="kessel_stillstandszeit",
        node_id="22070T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:timer-sand-complete",
        hdg_formatter="iSTD",
        unit=UnitOfTime.HOURS,
        ha_state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "angeforderte_temperatur_abnehmer": create_temp_sensor(
        key="angeforderte_temperatur_abnehmer",
        node_id="22098T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:thermometer-alert",
    ),
    "puffer_temperatur_oben": create_temp_sensor(
        key="puffer_temperatur_oben",
        node_id="24000T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:coolant-temperature",
    ),
    "puffer_temperatur_mitte": create_temp_sensor(
        key="puffer_temperatur_mitte",
        node_id="24001T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:coolant-temperature",
    ),
    "puffer_temperatur_unten": create_temp_sensor(
        key="puffer_temperatur_unten",
        node_id="24002T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:coolant-temperature",
    ),
    "puffer_soll_oben": create_temp_sensor(
        key="puffer_soll_oben",
        node_id="24004T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:coolant-temperature",
    ),
    "puffer_rucklauf_soll": create_temp_sensor(
        key="puffer_rucklauf_soll",
        node_id="24006T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:coolant-temperature",
    ),
    "puffer_status": create_enum_sensor(
        key="puffer_status",
        node_id="24015T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_2"],
        icon="mdi:propane-tank-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "puffer_energie_max": create_energy_sensor(
        key="puffer_energie_max",
        node_id="24016T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:battery-arrow-up",
        hdg_formatter="iKWH",
        unit=UnitOfEnergy.KILO_WATT_HOUR,
        ha_state_class=None,
    ),
    "puffer_energie_aktuell": create_energy_sensor(
        key="puffer_energie_aktuell",
        node_id="24017T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_2"],
        icon="mdi:lightning-bolt",
        hdg_formatter="iKWH",
        unit=UnitOfEnergy.KILO_WATT_HOUR,
        ha_state_class=SensorStateClass.TOTAL,
    ),
    "puffer_ladezustand_alt": create_percentage_sensor(
        key="puffer_ladezustand_alt",
        node_id="24019T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:battery-70",
        ha_device_class=SensorDeviceClass.BATTERY,
    ),
    "puffer_energie_gesamt_zahler": create_energy_sensor(
        key="puffer_energie_gesamt_zahler",
        node_id="24020T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:counter",
        hdg_formatter="iKWH",
        unit=UnitOfEnergy.KILO_WATT_HOUR,
        ha_state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "puffer_energie_ist": create_energy_sensor(
        key="puffer_energie_ist",
        node_id="24021T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:battery-heart-variant",
        hdg_formatter="iKWH",
        unit=UnitOfEnergy.KILO_WATT_HOUR,
        ha_state_class=SensorStateClass.MEASUREMENT,
        ha_device_class=None,
    ),
    "puffer_energie_aufnehmbar": create_energy_sensor(
        key="puffer_energie_aufnehmbar",
        node_id="24022T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:battery-plus-variant",
        hdg_formatter="iKWH",
        unit=UnitOfEnergy.KILO_WATT_HOUR,
        ha_state_class=SensorStateClass.MEASUREMENT,
        ha_device_class=None,
    ),
    "puffer_ladezustand": create_percentage_sensor(
        key="puffer_ladezustand",
        node_id="24023T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:battery-charging-70",
        ha_device_class=SensorDeviceClass.BATTERY,
    ),
    "puffer_vorlauf_extern": create_temp_sensor(
        key="puffer_vorlauf_extern",
        node_id="24098T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:thermometer-chevron-up",
    ),
    "puffer_rucklauf_extern": create_temp_sensor(
        key="puffer_rucklauf_extern",
        node_id="24099T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        icon="mdi:thermometer-chevron-down",
    ),
    "hk1_vorlauftemperatur_ist": create_temp_sensor(
        key="hk1_vorlauftemperatur_ist",
        node_id="26000T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:radiator",
    ),
    "hk1_temp_quelle_status_wert": create_general_sensor(
        key="hk1_temp_quelle_status_wert",
        node_id="26004T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        hdg_data_type="2",
        parse_as_type="float",
        ha_state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer-lines",
    ),
    "hk1_mischer_status_text": create_enum_sensor(
        key="hk1_mischer_status_text",
        node_id="26007T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:valve",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "hk1_pumpe_status_text": create_enum_sensor(
        key="hk1_pumpe_status_text",
        node_id="26008T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:pump",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "hk1_aktuelle_betriebsart": create_diagnostic_enum_sensor(
        key="hk1_aktuelle_betriebsart",
        node_id="26011T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:home-thermometer-outline",
    ),
    "hk1_vorlauftemperatur_soll": create_temp_sensor(
        key="hk1_vorlauftemperatur_soll",
        node_id="26099T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:radiator",
    ),
    "hk1_betriebsart": create_select_entity(
        key="hk1_betriebsart",
        node_id="6008T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:thermostat",
        options=[
            "normal",
            "tag",
            "nacht",
            "party",
            "sommer",
        ],
        uppercase_value=True,
    ),
    "hk2_system": create_enum_sensor(
        key="hk2_system",
        node_id="6120T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:radiator-disabled",
    ),
    "hk2_bezeichnung": create_diagnostic_text_sensor(
        key="hk2_bezeichnung",
        node_id="6121T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:label-outline",
    ),
    "hk2_soll_normal": create_number_entity(
        key="hk2_soll_normal",
        node_id="6122T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:home-thermometer",
        setter_type="int",
        setter_min_val=0.0,
        setter_max_val=90.0,
        setter_step=1.0,
        ha_device_class=SensorDeviceClass.TEMPERATURE,
        ha_native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        hdg_formatter="iTEMP",
        ha_state_class=SensorStateClass.MEASUREMENT,
    ),
    "hk2_soll_absenk": create_number_entity(
        key="hk2_soll_absenk",
        node_id="6123T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:home-thermometer-outline",
        setter_type="int",
        setter_min_val=0.0,
        setter_max_val=90.0,
        setter_step=1.0,
        ha_device_class=SensorDeviceClass.TEMPERATURE,
        ha_native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        hdg_formatter="iTEMP",
        ha_state_class=SensorStateClass.MEASUREMENT,
    ),
    "hk2_parallelverschiebung": create_number_entity(
        key="hk2_parallelverschiebung",
        node_id="6124T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_2"],
        icon="mdi:arrow-up-down",
        setter_type="int",
        setter_min_val=-20.0,
        setter_max_val=20.0,
        setter_step=1.0,
        ha_native_unit_of_measurement=UnitOfTemperature.KELVIN,
        hdg_formatter="iKELV",
        ha_state_class=SensorStateClass.MEASUREMENT,
    ),
    "hk2_raumeinflussfaktor": create_general_sensor(
        key="hk2_raumeinflussfaktor",
        node_id="6125T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_2"],
        hdg_data_type="2",
        parse_as_type="float",
        ha_state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:home-import-outline",
    ),
    "hk2_steilheit": create_number_entity(
        key="hk2_steilheit",
        node_id="6126T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_2"],
        icon="mdi:chart-line-variant",
        setter_type="float1",
        setter_min_val=0.1,
        setter_max_val=3.5,
        setter_step=0.1,
        ha_native_unit_of_measurement=None,
        ha_state_class=SensorStateClass.MEASUREMENT,
    ),
    "hk2_vorlauftemperatur_minimum": create_temp_sensor(
        key="hk2_vorlauftemperatur_minimum",
        node_id="6127T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:thermometer-minus",
    ),
    "hk2_vorlauftemperatur_maximum": create_temp_sensor(
        key="hk2_vorlauftemperatur_maximum",
        node_id="6128T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:thermometer-plus",
    ),
    "hk2_raumeinheit_status": create_enum_sensor(
        key="hk2_raumeinheit_status",
        node_id="6129T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:remote",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "hk2_offset_raumfuhler": create_kelvin_sensor(
        key="hk2_offset_raumfuhler",
        node_id="6130T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:thermometer-offset",
    ),
    "hk2_warmequelle": create_enum_sensor(
        key="hk2_warmequelle",
        node_id="6139T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:radiator-outline",
    ),
    "hk2_mischerlaufzeit_maximum": create_duration_sensor(
        key="hk2_mischerlaufzeit_maximum",
        node_id="6141T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:timer-settings-outline",
        hdg_formatter="iSEK",
        unit=UnitOfTime.SECONDS,
    ),
    "hk2_pumpe_ein_freigabetemperatur": create_temp_sensor(
        key="hk2_pumpe_ein_freigabetemperatur",
        node_id="6146T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:pump-outline",
    ),
    "hk2_pumpe_aus_aussentemperatur": create_number_entity(
        key="hk2_pumpe_aus_aussentemperatur",
        node_id="6147T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:pump-off-outline",
        setter_type="int",
        setter_min_val=0.0,
        setter_max_val=50.0,
        setter_step=1.0,
        ha_device_class=SensorDeviceClass.TEMPERATURE,
        ha_native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        hdg_formatter="iTEMP",
        ha_state_class=SensorStateClass.MEASUREMENT,
    ),
    "hk2_frostschutz_temp": create_temp_sensor(
        key="hk2_frostschutz_temp",
        node_id="6148T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:snowflake-thermometer",
    ),
    "hk2_eco_absenken_aus_aussentemperatur": create_number_entity(
        key="hk2_eco_absenken_aus_aussentemperatur",
        node_id="6149T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:leaf-thermometer",
        setter_type="int",
        setter_min_val=0.0,
        setter_max_val=50.0,
        setter_step=1.0,
        ha_device_class=SensorDeviceClass.TEMPERATURE,
        ha_native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        hdg_formatter="iTEMP",
        ha_state_class=SensorStateClass.MEASUREMENT,
    ),
    "hk2_heizgrenze_sommer": create_temp_sensor(
        key="hk2_heizgrenze_sommer",
        node_id="6150T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:weather-sunny-alert",
    ),
    "hk2_heizgrenze_winter": create_temp_sensor(
        key="hk2_heizgrenze_winter",
        node_id="6151T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:weather-snowy-heavy",
    ),
    "hk2_restwarme_aufnehmen": create_enum_sensor(
        key="hk2_restwarme_aufnehmen",
        node_id="6167T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_4"],
        icon="mdi:heat-wave",
    ),
    "hk2_vorlauftemperatur_ist": create_temp_sensor(
        key="hk2_vorlauftemperatur_ist",
        node_id="26100T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:radiator",
    ),
    "hk2_temp_quelle_status_wert": create_general_sensor(
        key="hk2_temp_quelle_status_wert",
        node_id="26104T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_5"],
        hdg_data_type="2",
        parse_as_type="float",
        ha_state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer-lines",
    ),
    "hk2_mischer_status_text": create_enum_sensor(
        key="hk2_mischer_status_text",
        node_id="26107T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:valve",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "hk2_pumpe_status_text": create_enum_sensor(
        key="hk2_pumpe_status_text",
        node_id="26108T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:pump",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "hk2_aktuelle_betriebsart": create_diagnostic_enum_sensor(
        key="hk2_aktuelle_betriebsart",
        node_id="26111T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:home-thermometer-outline",
    ),
    "hk2_vorlauftemperatur_soll": create_temp_sensor(
        key="hk2_vorlauftemperatur_soll",
        node_id="26199T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:radiator",
    ),
    "hk2_betriebsart": create_select_entity(
        key="hk2_betriebsart",
        node_id="6108T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:thermostat",
        options=[
            "normal",
            "tag",
            "nacht",
            "party",
            "sommer",
        ],
        uppercase_value=True,
    ),
    "ww1_temperatur_ist": create_temp_sensor(
        key="ww1_temperatur_ist",
        node_id="28000T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:thermometer",
    ),
    "ww1_ladungspumpe_status_text": create_enum_sensor(
        key="ww1_ladungspumpe_status_text",
        node_id="28004T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:pump",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),    
    "ww1_erhitzen_an_schwelle": create_number_entity(
        key="ww1_erhitzen_an_schwelle",
        node_id="8021T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:thermometer-chevron-up",
        setter_type="int",
        setter_min_val=10.0,
        setter_max_val=60.0,
        setter_step=1.0,
        ha_device_class=SensorDeviceClass.TEMPERATURE,
        ha_native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        hdg_formatter="iTEMP",
        ha_state_class=SensorStateClass.MEASUREMENT,
    ),
    "ww1_erhitzen_aus_schwelle": create_number_entity(
        key="ww1_erhitzen_aus_schwelle",
        node_id="8022T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:thermometer-chevron-down",
        setter_type="int",
        setter_min_val=20.0,
        setter_max_val=70.0,
        setter_step=1.0,
        ha_device_class=SensorDeviceClass.TEMPERATURE,
        ha_native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        hdg_formatter="iTEMP",
        ha_state_class=SensorStateClass.MEASUREMENT,
    ),
    "ww1_temperatur_vorlauf_solar_ist": create_temp_sensor(
        key="ww1_temperatur_vorlauf_solar_ist",
        node_id="28003T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:solar-power-variant",
    ),
    "ww1_angeforderte_temperatur_status": create_enum_sensor(
        key="ww1_angeforderte_temperatur_status",
        node_id="28099T",
        polling_group=POLLING_GROUP_KEYS["POLLING_GROUP_1"],
        icon="mdi:thermometer-plus",
        entity_category=EntityCategory.DIAGNOSTIC,
    )
}

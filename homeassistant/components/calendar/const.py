"""Constants for calendar components."""

from __future__ import annotations

from enum import IntFlag
from typing import TYPE_CHECKING

from homeassistant.util.hass_dict import HassKey

if TYPE_CHECKING:
    from homeassistant.helpers.entity_component import EntityComponent

    from . import CalendarEntity

DOMAIN = "calendar"
DOMAIN_DATA: HassKey[EntityComponent[CalendarEntity]] = HassKey(DOMAIN)

CONF_EVENT = "event"
CALENDAR_TEMPLATE = "calendar_template"
TEMPLATE_EVENTS = "template_events"
TEMPLATE_NAME = "template_name"
TEMPLATE_ID = "template_id"
TEMPLATE_VIEW_EVENTS = "template_view_events"


class CalendarEntityFeature(IntFlag):
    """Supported features of the calendar entity."""

    CREATE_EVENT = 1
    DELETE_EVENT = 2
    UPDATE_EVENT = 4


EVENT_ATTENDEES = "attendees"
# rfc5545 fields
EVENT_UID = "uid"
EVENT_START = "dtstart"
EVENT_END = "dtend"
EVENT_SUMMARY = "summary"
EVENT_DESCRIPTION = "description"
EVENT_LOCATION = "location"
EVENT_RECURRENCE_ID = "recurrence_id"
EVENT_RECURRENCE_RANGE = "recurrence_range"
EVENT_RRULE = "rrule"

# Service call fields
EVENT_START_DATE = "start_date"
EVENT_END_DATE = "end_date"
EVENT_START_DATETIME = "start_date_time"
EVENT_END_DATETIME = "end_date_time"
EVENT_IN = "in"
EVENT_IN_DAYS = "days"
EVENT_IN_WEEKS = "weeks"
EVENT_TIME_FIELDS = {
    EVENT_START_DATE,
    EVENT_END_DATE,
    EVENT_START_DATETIME,
    EVENT_END_DATETIME,
    EVENT_IN,
}
EVENT_TYPES = "event_types"
EVENT_DURATION = "duration"

ENITITY_NOT_FOUND_ERROR = "Entity not found"

# Fields for the list events service
LIST_EVENT_FIELDS = {
    "start",
    "end",
    EVENT_SUMMARY,
    EVENT_DESCRIPTION,
    EVENT_LOCATION,
}

"""Support for Alexa skill service end point."""

import hmac
from http import HTTPStatus
import logging
import uuid

from aiohttp.web_response import StreamResponse

from homeassistant.components import http
from homeassistant.const import CONF_PASSWORD
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import template
from homeassistant.helpers.typing import ConfigType
import homeassistant.util.dt as dt_util

from .const import (
    API_PASSWORD,
    ATTR_MAIN_TEXT,
    ATTR_REDIRECTION_URL,
    ATTR_STREAM_URL,
    ATTR_TITLE_TEXT,
    ATTR_UID,
    ATTR_UPDATE_DATE,
    CONF_AUDIO,
    CONF_DISPLAY_URL,
    CONF_TEXT,
    CONF_TITLE,
    CONF_UID,
    DATE_FORMAT,
)

_LOGGER = logging.getLogger(__name__)

FLASH_BRIEFINGS_API_ENDPOINT = "/api/alexa/flash_briefings/{briefing_id}"


@callback
def async_setup(hass: HomeAssistant, flash_briefing_config: ConfigType) -> None:
    """Activate Alexa component."""
    hass.http.register_view(AlexaFlashBriefingView(hass, flash_briefing_config))


class AlexaFlashBriefingView(http.HomeAssistantView):
    """Handle Alexa Flash Briefing skill requests."""

    url = FLASH_BRIEFINGS_API_ENDPOINT
    requires_auth = False
    name = "api:alexa:flash_briefings"

    def __init__(self, hass: HomeAssistant, flash_briefings: ConfigType) -> None:
        """Initialize Alexa view."""
        super().__init__()
        self.flash_briefings = flash_briefings

    def _authorize_apipassword(
        self, request: http.HomeAssistantRequest, briefing_id: str
    ) -> tuple[bytes, HTTPStatus] | None:
        if request.query.get(API_PASSWORD) is None:
            err = "No password provided for Alexa flash briefing: %s"
            _LOGGER.error(err, briefing_id)
            return b"", HTTPStatus.UNAUTHORIZED

        if not hmac.compare_digest(
            request.query[API_PASSWORD].encode("utf-8"),
            self.flash_briefings[CONF_PASSWORD].encode("utf-8"),
        ):
            err = "Wrong password for Alexa flash briefing: %s"
            _LOGGER.error(err, briefing_id)
            return b"", HTTPStatus.UNAUTHORIZED

        if not isinstance(self.flash_briefings.get(briefing_id), list):
            err = "No configured Alexa flash briefing was found for: %s"
            _LOGGER.error(err, briefing_id)
            return b"", HTTPStatus.NOT_FOUND

        return None

    def _briefing_output(self, item: dict) -> dict:
        output = {}

        conf_title = item.get(CONF_TITLE)
        if conf_title is not None and isinstance(conf_title, template.Template):
            output[ATTR_TITLE_TEXT] = item[CONF_TITLE].async_render(parse_result=False)
        else:
            output[ATTR_TITLE_TEXT] = conf_title

        conf_text = item.get(CONF_TEXT)
        if isinstance(conf_text, template.Template):
            output[ATTR_MAIN_TEXT] = item[CONF_TEXT].async_render(parse_result=False)
        elif conf_text is not None:
            output[ATTR_MAIN_TEXT] = conf_text

        if (uid := item.get(CONF_UID)) is None:
            uid = str(uuid.uuid4())
        output[ATTR_UID] = uid

        conf_audio = item.get(CONF_AUDIO)
        if isinstance(conf_audio, template.Template):
            output[ATTR_STREAM_URL] = item[CONF_AUDIO].async_render(parse_result=False)
        elif conf_audio is not None:
            output[ATTR_STREAM_URL] = conf_audio

        conf_display_url = item.get(CONF_DISPLAY_URL)
        if isinstance(conf_display_url, template.Template):
            output[ATTR_REDIRECTION_URL] = item[CONF_DISPLAY_URL].async_render(
                parse_result=False
            )
        elif conf_display_url is not None:
            output[ATTR_REDIRECTION_URL] = conf_display_url

        output[ATTR_UPDATE_DATE] = dt_util.utcnow().strftime(DATE_FORMAT)
        return output

    @callback
    def get(
        self, request: http.HomeAssistantRequest, briefing_id: str
    ) -> StreamResponse | tuple[bytes, HTTPStatus]:
        """Handle Alexa Flash Briefing request."""
        _LOGGER.debug("Received Alexa flash briefing request for: %s", briefing_id)
        status = self._authorize_apipassword(request, briefing_id)
        if status is not None:
            return status

        briefing = []

        for item in self.flash_briefings.get(briefing_id, []):
            output = self._briefing_output(item)
            briefing.append(output)

        return self.json(briefing)

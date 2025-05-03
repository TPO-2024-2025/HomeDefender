from typing import List, Optional  # noqa: D100, UP035

from homeassistant.core import HomeAssistant


class EmailNotifier:
    """A dedicated Python class to send email notifications via Home Assistant's notify SMTP integration."""

    def __init__(self, hass: HomeAssistant, service_name: str = "email_alerts"):
        """Initialize the EmailNotifier.

        :param hass: The Home Assistant instance
        :param service_name: The name of the notify service (SMTP) to call
        """
        self.hass = hass
        self.service_name = service_name

    def send(
        self, subject: str, message: str, targets: Optional[List[str]] = None
    ) -> None:
        """Send an email notification using the configured Home Assistant notify service.

        :param subject: The email subject line
        :param message: The email body text
        :param targets: Optional list of recipient email addresses (overrides default)
        """
        data: dict = {"title": subject, "message": message}
        # If specific recipients are provided, include them
        if targets:
            data["target"] = targets

        # Call the Home Assistant notify service
        self.hass.services.call("notify", self.service_name, data)


# Example usage in your integration's async_setup_entry:
#
# from .notifications import EmailNotifier
#
# async def async_setup_entry(hass, entry):
#     email_service = entry.options.get("email_service", "notify.email_alerts")
#     notifier = EmailNotifier(hass, service_name=email_service)
#
#     # When an event triggers, call:
#     notifier.send(
#         subject="Home Security Alert",
#         message="A person was detected by your camera",
#         targets=entry.options.get("email_recipients")
#     )
#
#     return True

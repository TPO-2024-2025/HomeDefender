"""Event listeners for the tpo_home_security integration, refactored using the Observer pattern and a Facade structural pattern."""

import logging
from pathlib import Path
from typing import Any, List, Optional

import cv2
import torch

from homeassistant.core import Event, HomeAssistant, callback
from .notifications import EmailNotifier
from .const import DOMAIN


from ultralytics import YOLO  # noqa: E402

_LOGGER = logging.getLogger(__name__)

# ── Configuration ─────────────────────────────────────────────────────────────
VIDEO_FILE = Path(__file__).parent / "GoldenDoodleCam.mp4"
MODEL_FILE = Path(__file__).parent / "yolov8n.pt"
PERSON_CLASS = 0
ANIMAL_CLASS_IDS = [
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
]
CONFIDENCE = 0.5
# ─────────────────────────────────────────────────────────────────────────────


# Load the model **once** at import time
try:
    MODEL = YOLO(str(MODEL_FILE))
    MODEL.export(format="torchscript", imgsz=640)
    _LOGGER.info("Loaded YOLO model from %s", MODEL_FILE)
except Exception as e:
    MODEL = None
    _LOGGER.error("Failed loading YOLO model: %s", e)


class YoloModelSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # direct‐load raw weights; ultralytics will call torch.load internally
            cls._instance.model = YOLO(str(MODEL_FILE))
            _LOGGER.info("Loaded YOLO model from %s", MODEL_FILE)
        return cls._instance

    def detect_person(self, image_path: str) -> bool:
        if not self.model:
            return False
        try:
            results = self.model(image_path)[0]
            return any(
                int(box.cls) == PERSON_CLASS and box.conf.cpu().item() >= CONFIDENCE
                for box in results.boxes
            )
        except Exception as e:
            _LOGGER.error("YOLO error: %s", e)
            return False

    def detect_animals(self, image_path: str) -> List[str]:
        """Return list of animal class names detected in the image."""
        if not self.model:
            return []
        try:
            results = self.model.predict(source=image_path, classes=ANIMAL_CLASS_IDS)[0]
            animals = [self.model.names[int(box.cls)] for box in results.boxes]
            return list(dict.fromkeys(animals))
        except Exception as e:
            _LOGGER.error("YOLO error during animal detection: %s", e)
            return []


# ── Observer Pattern ───────────────────────────────────────────────────────────
class Sensor:
    def __init__(self):
        self.subscribers = []

    def register(self, subscriber):
        self.subscribers.append(subscriber)

    def notify(self, state):
        for sub in self.subscribers:
            sub.update(state)


class Alarm:
    def __init__(self, hass: HomeAssistant):
        self.hass = hass

    def update(self, state):
        svc = "turn_on" if state == "DETECTED" else "turn_off"
        self.hass.services.call(
            "input_boolean",
            svc,
            {"entity_id": "input_boolean.alarm_toggle"},
        )
        _LOGGER.info("Alarm turned %s", "ON" if state == "DETECTED" else "OFF")


class Notifier:
    def update(self, state):
        if state == "DETECTED":
            _LOGGER.info("Notifier: Person detected alert triggered")


# ── Structural Pattern: Facade Pattern ─────────────────────────────────────────
class SecurityFacade:
    """Facade to simplify detection, state decision, and notification flow."""

    def __init__(self, hass: HomeAssistant):
        # initialize subject and observers
        self.sensor = Sensor()
        self.sensor.register(Alarm(hass))
        self.sensor.register(Notifier())
        # reuse singleton for detection
        self.yolo = YoloModelSingleton()

    def process_frame(self, image_path: str) -> bool:
        # detect person and notify subscribers via Sensor
        detected = self.yolo.detect_person(image_path)
        state = "DETECTED" if detected else "CLEAR"
        self.sensor.notify(state)
        return detected


# Global facade instance (to be created in register_listeners)
security_facade: SecurityFacade | None = None


@callback
def handle_sensor_toggle_update(hass: HomeAssistant, event: Event) -> None:
    entity_id = event.data.get("entity_id")
    if entity_id not in ("input_boolean.sensor_toggle", "input_select.home_mode"):
        return

    sensor_state = hass.states.get("input_boolean.sensor_toggle")
    if sensor_state:
        hass.states.set(
            "home_sec.sensor_toggle_state",
            sensor_state.state,
            {
                "friendly_name": "Sensor Toggle State",
                "original_entity": "input_boolean.sensor_toggle",
            },
        )

    mode_state = hass.states.get("input_select.home_mode")
    if not sensor_state or not mode_state:
        _LOGGER.debug("Missing entities, skipping detection")
        return

    if sensor_state.state != "on" or mode_state.state != "AWAY":
        _LOGGER.debug(
            "Conditions not met (sensor=%s, mode=%s)",
            sensor_state.state,
            mode_state.state,
        )
        return

    cap = cv2.VideoCapture(str(VIDEO_FILE))
    success, frame = cap.read()
    cap.release()
    if not success:
        _LOGGER.error("Failed to read frame from %s", VIDEO_FILE)
        return

    tmp = VIDEO_FILE.parent / "_snapshot.jpg"
    cv2.imwrite(str(tmp), frame)

    email_notifier = hass.data[DOMAIN]["email_notifier"]
    push_notifier = hass.data[DOMAIN]["push_notifier"]
    recipients = hass.data[DOMAIN]["email_recipients"]
    # Delegate detection & notification to the Facade
    if security_facade:
        detected = security_facade.process_frame(str(tmp))
        if detected:
            # Send the email
            email_notifier.send(
                subject="🏠 Home Security Alert",
                message="A person was detected by your camera.",
                targets=recipients,
            )
            # send the push notification
            push_notifier.send(
                title="🏠 Home Security Alert",
                message="A person was detected by your camera.",
            )
        animals = security_facade.yolo.detect_animals(str(tmp))
        for animal in animals:
            _LOGGER.info("Detected animal: %s", animal)
            # Here you can add logic to handle animal detection if needed
            push_notifier.send(
                title="Animal Detected",
                message=f"Detected animal: {animal}",
            )


def register_listeners(hass: HomeAssistant) -> None:
    global security_facade
    # create and configure the SecurityFacade
    security_facade = SecurityFacade(hass)

    # register Home Assistant event listener
    hass.bus.async_listen(
        "state_changed", lambda event: handle_sensor_toggle_update(hass, event)
    )

    # initialize UI toggle state
    initial = hass.states.get("input_boolean.sensor_toggle")
    init_state = initial.state if initial else "unknown"
    hass.states.set(
        "home_sec.sensor_toggle_state",
        init_state,
        {
            "friendly_name": "Sensor Toggle State",
            "original_entity": "input_boolean.sensor_toggle",
        },
    )

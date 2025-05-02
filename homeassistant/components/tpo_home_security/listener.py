"""Event listeners for the tpo_home_security integration."""

import logging
from pathlib import Path
from typing import Any

import cv2
import torch

from homeassistant.core import Event, HomeAssistant, callback

# Force full weights load so ultralytics can load YOLOv5
_orig_torch_load = torch.load


def _torch_load_force_full(*args: Any, **kwargs: Any) -> Any:
    """Override torch.load to enforce weights_only=False."""
    kwargs.setdefault("weights_only", False)
    return _orig_torch_load(*args, **kwargs)


torch.load = _torch_load_force_full

from ultralytics import YOLO  # noqa: E402

_LOGGER = logging.getLogger(__name__)

# ── Configuration ─────────────────────────────────────────────────────────────
VIDEO_FILE = Path(__file__).parent / "SecurityCam.mp4"
MODEL_FILE = Path(__file__).parent / "yolov5s.pt"
PERSON_CLASS = 0
CONFIDENCE = 0.5
# ────────────────────────────────────────────────────────────────────────────────

# Load the model **once** at import time
try:
    MODEL = YOLO(str(MODEL_FILE))
    _LOGGER.info("Loaded YOLO model from %s", MODEL_FILE)
except Exception as e:  # noqa: BLE001
    MODEL = None
    _LOGGER.error("Failed loading YOLO model: %s", e)


@callback
def handle_sensor_toggle_update(hass: HomeAssistant, event: Event) -> None:
    """Re-run detection whenever sensor_toggle or home_mode changes."""
    entity_id = event.data.get("entity_id")
    if entity_id not in ("input_boolean.sensor_toggle", "input_select.home_mode"):
        return

    # 1) Mirror the sensor state in our helper entity
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

    # 2) Only proceed if sensor=on AND mode=AWAY
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

    # 3) Grab a single frame
    cap = cv2.VideoCapture(str(VIDEO_FILE))
    success, frame = cap.read()
    cap.release()
    if not success:
        _LOGGER.error("Failed to read frame from %s", VIDEO_FILE)
        return

    # 4) Save snapshot for YOLO
    tmp = VIDEO_FILE.parent / "_snapshot.jpg"
    cv2.imwrite(str(tmp), frame)

    # 5) Run YOLO person detection
    if MODEL is None:
        _LOGGER.error("No model loaded, cannot detect person")
        return

    try:
        results = MODEL(str(tmp))[0]
        person = any(
            int(box.cls) == PERSON_CLASS and box.conf.cpu().item() >= CONFIDENCE
            for box in results.boxes
        )
        _LOGGER.info("Person detected: %s", person)
    except Exception as e:  # noqa: BLE001
        _LOGGER.error("YOLO error: %s", e)
        person = False

    # 6) Toggle the alarm
    svc = "turn_on" if person else "turn_off"
    hass.services.call(
        "input_boolean",
        svc,
        {"entity_id": "input_boolean.alarm_toggle"},
    )
    _LOGGER.info("Alarm turned %s", "ON" if person else "OFF")


def register_listeners(hass: HomeAssistant) -> None:
    """Wire up listener and set the initial sensor state mirror."""
    hass.bus.async_listen(
        "state_changed", lambda event: handle_sensor_toggle_update(hass, event)
    )

    # Initial mirror of sensor_toggle
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

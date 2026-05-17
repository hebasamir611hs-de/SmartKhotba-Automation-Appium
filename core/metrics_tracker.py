"""
Healing Metrics Tracker.
Thread-safe, append-only, absolute-path JSON logger.
"""
import json
import os
import threading
from datetime import datetime
from pathlib import Path
from utils.logger import get_logger

logger = get_logger(__name__)

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_METRICS = _PROJECT_ROOT / "data" / "healing_metrics.json"
_LOCK = threading.Lock()


class MetricsTracker:
    def __init__(self, metrics_file: Path = None):
        self.metrics_file = Path(metrics_file) if metrics_file else _DEFAULT_METRICS
        self._ensure_file()

    def _ensure_file(self):
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.metrics_file.exists():
            self.metrics_file.write_text("[]", encoding="utf-8")

    def log_healing_event(self, page, element, primary_locator, successful_locator):
        self._append_event({
            "timestamp": datetime.now().isoformat(),
            "status": "HEALED",
            "page": page,
            "element": element,
            "primary_locator": str(primary_locator),
            "healed_with": str(successful_locator),
        })
        logger.info(f"📈 HEALED: {page}.{element} via {successful_locator}")

    def log_failure_event(self, page, element, primary_locator):
        self._append_event({
            "timestamp": datetime.now().isoformat(),
            "status": "FAILED",
            "page": page,
            "element": element,
            "primary_locator": str(primary_locator),
        })
        logger.error(f"📈 FAILED: {page}.{element}")

    def _append_event(self, event):
        with _LOCK:
            try:
                data = json.loads(self.metrics_file.read_text(encoding="utf-8") or "[]")
                if not isinstance(data, list):
                    data = []
                data.append(event)
                tmp = self.metrics_file.with_suffix(".json.tmp")
                tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
                os.replace(tmp, self.metrics_file)
            except Exception as e:
                logger.error(f"Metrics write failed: {e}")
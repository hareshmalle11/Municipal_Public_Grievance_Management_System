from __future__ import annotations

import json
import re
import threading
from pathlib import Path

import numpy as np

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "ml_model"
MODEL_PATH = MODEL_DIR / "grievance_bilstm_multi_task.keras"
TOKENIZER_PATH = MODEL_DIR / "tokenizer.json"
CONFIG_PATH = MODEL_DIR / "training_config.json"


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


class GrievancePredictor:
    def __init__(self) -> None:
        self._validate_artifacts()

        # Import tensorflow and keras dynamically inside init to keep startup instant
        import tensorflow as tf
        from tensorflow.keras.preprocessing.sequence import pad_sequences
        from tensorflow.keras.preprocessing.text import tokenizer_from_json

        self._pad_sequences = pad_sequences
        self.model = tf.keras.models.load_model(MODEL_PATH)
        self.tokenizer = tokenizer_from_json(TOKENIZER_PATH.read_text(encoding="utf-8"))
        self.config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        self.max_length = int(self.config.get("max_length", 100))
        self.category_classes = self.config["category_classes"]
        self.priority_classes = self.config["priority_classes"]

    def _validate_artifacts(self) -> None:
        missing_paths = [
            path for path in [MODEL_PATH, TOKENIZER_PATH, CONFIG_PATH] if not path.exists()
        ]
        if missing_paths:
            missing = ", ".join(str(path) for path in missing_paths)
            raise FileNotFoundError(
                f"Missing ML artifact(s): {missing}. Run ml-service/train.py first."
            )

    def predict(self, complaint_text: str) -> dict[str, float | str]:
        cleaned_text = clean_text(complaint_text)
        sequence = self.tokenizer.texts_to_sequences([cleaned_text])
        padded_sequence = self._pad_sequences(
            sequence,
            maxlen=self.max_length,
            padding="post",
            truncating="post",
        )

        raw_prediction = self.model.predict(padded_sequence, verbose=0)
        category_probs, priority_probs = self._split_outputs(raw_prediction)

        category_index = int(np.argmax(category_probs))
        priority_index = int(np.argmax(priority_probs))

        return {
            "category": self.category_classes[category_index],
            "priority": self.priority_classes[priority_index],
            "category_confidence": float(category_probs[category_index]),
            "priority_confidence": float(priority_probs[priority_index]),
        }

    def _split_outputs(self, prediction: object) -> tuple[np.ndarray, np.ndarray]:
        if isinstance(prediction, dict):
            category_probs = prediction["category_output"][0]
            priority_probs = prediction["priority_output"][0]
            return category_probs, priority_probs

        if isinstance(prediction, (list, tuple)) and len(prediction) == 2:
            first = np.asarray(prediction[0][0])
            second = np.asarray(prediction[1][0])

            if len(first) == len(self.category_classes):
                return first, second
            return second, first

        raise ValueError("Unexpected model prediction output format.")


# Thread-safe background loader
_predictor: GrievancePredictor | None = None
_predictor_lock = threading.Lock()
_loading_thread: threading.Thread | None = None
_loading_error: str | None = None


def _load_model_task() -> None:
    global _predictor, _loading_error
    try:
        print("[ML Service] Starting background ML model initialization...")
        p = GrievancePredictor()
        with _predictor_lock:
            _predictor = p
            _loading_error = None
        print("[ML Service] Background ML model initialization completed successfully!")
    except Exception as e:
        error_msg = f"Error loading ML model in background: {e}"
        print(f"[ML Service] {error_msg}")
        with _predictor_lock:
            _loading_error = error_msg


def start_background_loading() -> None:
    global _loading_thread
    with _predictor_lock:
        if _predictor is not None or _loading_thread is not None:
            return  # Already loaded or loading in progress
    _loading_thread = threading.Thread(target=_load_model_task, daemon=True)
    _loading_thread.start()


def get_predictor() -> GrievancePredictor | None:
    with _predictor_lock:
        if _loading_error is not None:
            raise RuntimeError(_loading_error)
        return _predictor

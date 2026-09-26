"""
inference.py

Clean prediction wrapper around the trained brain tumor classifier
(brain_tumor_transfer.keras from Step 2). Preprocessing (EfficientNet's
preprocess_input) is already baked into the saved model, so this file
only needs to resize images before calling model.predict() — nothing
here needs to duplicate what's inside the model graph.

This is what the Streamlit app (Step 4) will import directly.
"""

import io
import numpy as np
import tensorflow as tf
from PIL import Image

IMG_SIZE = (224, 224)

# Alphabetical order of the training folder names — matches what
# image_dataset_from_directory printed as class_names in Steps 1 & 2.
# Double-check against that printed output before using this in the app.
CLASS_NAMES = ["glioma", "meningioma", "notumor", "pituitary"]


def load_model(model_path: str = "brain_tumor_transfer.keras") -> tf.keras.Model:
    """Load the saved Keras model from disk."""
    return tf.keras.models.load_model(model_path)


def preprocess_image(image) -> np.ndarray:
    """
    Accepts a file path (str), raw bytes, or a PIL.Image, and returns
    a (1, 224, 224, 3) float32 array ready for model.predict().

    Does NOT rescale or normalize — the model already has that built in.
    """
    if isinstance(image, str):
        img = Image.open(image)
    elif isinstance(image, (bytes, bytearray)):
        img = Image.open(io.BytesIO(image))
    elif isinstance(image, Image.Image):
        img = image
    else:
        raise TypeError(f"Unsupported image input type: {type(image)}")

    img = img.convert("RGB").resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32)
    return np.expand_dims(arr, axis=0)


def predict(model: tf.keras.Model, image) -> dict:
    """
    Runs inference and returns:
    {
        "label": "glioma",
        "confidence": 0.94,
        "probabilities": {"glioma": 0.94, "meningioma": 0.03, ...}
    }
    """
    batch = preprocess_image(image)
    probs = model.predict(batch, verbose=0)[0]

    predicted_idx = int(np.argmax(probs))
    return {
        "label": CLASS_NAMES[predicted_idx],
        "confidence": float(probs[predicted_idx]),
        "probabilities": {
            name: float(p) for name, p in zip(CLASS_NAMES, probs)
        },
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python inference.py <path_to_mri_image> [model_path]")
        sys.exit(1)

    image_path = sys.argv[1]
    model_path = sys.argv[2] if len(sys.argv) > 2 else "brain_tumor_transfer.keras"

    model = load_model(model_path)
    result = predict(model, image_path)

    print(f"Prediction: {result['label']} ({result['confidence']:.2%} confidence)")
    print("Full probabilities:")
    for label, p in sorted(result["probabilities"].items(), key=lambda x: -x[1]):
        print(f"  {label}: {p:.2%}")

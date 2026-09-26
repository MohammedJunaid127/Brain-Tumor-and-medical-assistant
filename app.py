"""
app.py

Streamlit interface for the brain tumor MRI classifier. Uses inference.py
for the model/prediction logic and medical_info.py for the reference
content — this file only handles layout and display.

Run locally:   streamlit run app.py
Requires "brain_tumor_transfer.keras" in the same folder.
"""

import io

import streamlit as st
from PIL import Image

from inference import load_model, predict
from medical_info import get_medical_info

DISPLAY_NAMES = {
    "glioma": "Glioma",
    "meningioma": "Meningioma",
    "notumor": "No Tumor",
    "pituitary": "Pituitary",
}

st.set_page_config(page_title="Brain Tumor MRI Classifier", page_icon="🧠", layout="centered")

st.title("🧠 Brain Tumor MRI Classifier")
st.caption("Upload a brain MRI scan to classify tumor type and view general reference information.")


@st.cache_resource
def get_model():
    return load_model("brain_tumor_transfer.keras")


try:
    model = get_model()
except Exception as e:
    st.error(
        "Couldn't load 'brain_tumor_transfer.keras'. Make sure the model file "
        f"is in the same folder as this app.\n\n{e}"
    )
    st.stop()

uploaded_file = st.file_uploader("Upload an MRI scan", type=["jpg", "jpeg", "png"])

if uploaded_file is None:
    st.info("Upload an MRI image above to get started.")
    st.stop()

image_bytes = uploaded_file.getvalue()
image = Image.open(io.BytesIO(image_bytes))

col_img, col_result = st.columns([1, 1.2])

with col_img:
    st.image(image, caption="Uploaded scan", use_container_width=True)

with st.spinner("Analyzing scan..."):
    result = predict(model, image_bytes)

label = result["label"]
confidence = result["confidence"]
probabilities = result["probabilities"]

with col_result:
    st.subheader(f"Prediction: {DISPLAY_NAMES.get(label, label.title())}")
    st.metric("Confidence", f"{confidence:.1%}")

    st.write("**Class probabilities**")
    for cls, p in sorted(probabilities.items(), key=lambda item: -item[1]):
        st.write(f"{DISPLAY_NAMES.get(cls, cls.title())} — {p:.1%}")
        st.progress(p)

st.divider()

info = get_medical_info(label)

st.subheader("About this result")
st.write(info["definition"])

if info["symptoms"]:
    with st.expander("Common symptoms"):
        for symptom in info["symptoms"]:
            st.write(f"- {symptom}")

st.write(f"**Typical management:** {info['common_treatments']}")

st.warning(
    "This tool provides general educational information only and is not a medical "
    "diagnosis. Always consult a qualified healthcare professional for interpretation "
    "of medical imaging and treatment decisions."
)

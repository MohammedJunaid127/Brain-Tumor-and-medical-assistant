"""
medical_info.py

Static reference information for each predicted tumor class. This is
general educational content, not a diagnosis — app.py pairs this with
a clear disclaimer to that effect.
"""

INFO_DB = {
    "glioma": {
        "definition": (
            "A glioma is a type of tumor that occurs in the brain and spinal cord. "
            "Gliomas begin in the glial cells that surround nerve cells and help them function."
        ),
        "symptoms": [
            "Headaches (especially in the morning)",
            "Nausea or vomiting",
            "Confusion or a decline in brain function",
            "Memory loss",
            "Difficulty with balance or speech",
        ],
        "common_treatments": (
            "Treatment depends on the grade and location, usually involving a combination "
            "of surgery, radiation therapy, and chemotherapy."
        ),
    },
    "meningioma": {
        "definition": (
            "A meningioma is a tumor that arises from the meninges — the membranes that "
            "surround your brain and spinal cord. Most are noncancerous (benign) and slow-growing."
        ),
        "symptoms": [
            "Changes in vision (double vision or blurriness)",
            "Headaches that worsen with time",
            "Hearing loss or ringing in ears",
            "Loss of smell",
            "Seizures or weakness in limbs",
        ],
        "common_treatments": (
            "Active monitoring (watchful waiting) for small slow tumors, surgical removal, "
            "or targeted radiation therapy (stereotactic radiosurgery)."
        ),
    },
    "pituitary": {
        "definition": (
            "A pituitary tumor is an abnormal growth in the pituitary gland, located at the "
            "base of the brain. Most are benign adenomas that do not spread to other parts of the body."
        ),
        "symptoms": [
            "Hormonal imbalances (unexplained weight gain, fatigue)",
            "Vision loss (particularly peripheral vision loss)",
            "Headaches",
            "Nausea and vomiting",
        ],
        "common_treatments": (
            "Surgery to remove the tumor, medication to manage hormone levels, or radiation "
            "therapy to shrink the tumor."
        ),
    },
    "notumor": {
        "definition": (
            "No tumor detected. The MRI scan does not indicate abnormal structural growths "
            "consistent with glioma, meningioma, or pituitary adenomas."
        ),
        "symptoms": [],
        "common_treatments": (
            "No oncological intervention required. Continue routine preventative checkups "
            "or follow up with your primary physician regarding any symptoms."
        ),
    },
}

_UNKNOWN = {
    "definition": "Unknown category. Please consult a neurological specialist.",
    "symptoms": [],
    "common_treatments": "Consult a physician.",
}


def get_medical_info(tumor_type: str) -> dict:
    """Look up general reference info for a predicted class (case-insensitive)."""
    return INFO_DB.get(tumor_type.lower().strip(), _UNKNOWN)

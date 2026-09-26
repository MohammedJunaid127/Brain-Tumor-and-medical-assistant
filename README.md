# Brain Tumor Detection — MRI Classifier + Medical Info Assistant

Classifies brain MRI scans into four categories — glioma, meningioma, pituitary
tumor, or no tumor — using a fine-tuned EfficientNetB0, and pairs each
prediction with general reference information via a Streamlit interface.

## Results

Trained on the Kaggle [Brain Tumor MRI Dataset](https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset)
(5,600 training images, 1,600 test images, balanced across 4 classes).

| Model | Test accuracy | Test loss |
|---|---|---|
| Baseline CNN (from scratch) | 89.6% | 1.14 |
| EfficientNetB0 (transfer learning + fine-tuning) | 85.6% | 0.47 |

Per-class performance (EfficientNetB0):

| Class | Precision | Recall | F1 |
|---|---|---|---|
| Glioma | 0.92 | 0.69 | 0.79 |
| Meningioma | 0.82 | 0.76 | 0.79 |
| No Tumor | 0.89 | 0.98 | 0.93 |
| Pituitary | 0.81 | 0.99 | 0.89 |

Glioma is the hardest class to separate from the others — a known
characteristic of this dataset, not specific to this model.

## Repo structure

```
.
├── README.md
├── requirements.txt
├── .gitignore
├── notebooks/
│   ├── 01_baseline_cnn.ipynb
│   └── 02_transfer_learning.ipynb
├── inference.py        # model loading + predict()
├── medical_info.py      # reference content per tumor class
└── app.py                # Streamlit interface
```

## Setup

```bash
pip install -r requirements.txt
```

Place a trained `brain_tumor_transfer.keras` (produced by
`02_transfer_learning.ipynb`) in the project root — it's not committed to
this repo since model files are large; see `.gitignore`.

## Running the notebooks

Open either notebook in Google Colab (recommended, for free GPU access) or
locally with Jupyter. Each notebook downloads the dataset itself via
`kagglehub`.

## Running the app

```bash
streamlit run app.py
```

Upload an MRI image (JPG/PNG) to get a predicted class, confidence
breakdown, and general reference information.

## Disclaimer

This project is for educational purposes. Predictions and reference
information are not a medical diagnosis — consult a qualified healthcare
professional for interpretation of medical imaging.

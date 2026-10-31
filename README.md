# WildSight: AI-Powered Wildlife Monitoring & Camera-Trap Analytics

**CBIT Hacktoberfest '26** | **Team Helix (HFT26-TEAM-11)**

## Team Members

| Name                      | Role                                     |
| ------------------------- | ---------------------------------------- |
| Sudiksha Gopisetty (Lead) | Integration, deployment, README and demo |
| Sahasra Bandari           | Data pipeline                            |
| Dwayitha Reddy            | Species classifier                       |
| Ria Reddy                 | Dashboard                                |

## 1. Problem Statement

Researchers manually review thousands of camera-trap images to identify wildlife activity. This process is time-consuming, especially when datasets contain empty frames, repeated captures, and images with unclear animal visibility.

WildSight automates animal detection, species classification, and wildlife activity analysis using computer vision and machine learning.

**Dataset:** [Caltech Camera Traps – LILA](https://lila.science/datasets/caltech-camera-traps)

## 2. Solution Overview

WildSight provides an end-to-end camera-trap analytics workflow:

1. **Animal Detection:** MegaDetector identifies animals, people, and vehicles while filtering empty frames.
2. **Species Classification:** A fine-tuned MobileNetV3-Small classifier predicts supported animal classes.
3. **Uncertainty Handling:** Low-confidence predictions are marked as unidentified rather than presenting uncertain predictions as facts.
4. **Sightings Generation:** Related camera frames are grouped into sightings using sequence information or timestamp proximity.
5. **Analytics Dashboard:** Detection results and wildlife activity summaries are presented through an interactive dashboard.
6. **AI Insights:** Featherless-powered natural-language summaries are intended to help interpret aggregated wildlife statistics.

## 3. Technology Stack

* **Detection:** MegaDetector V6, PyTorch-Wildlife
* **Classification:** MobileNetV3-Small, PyTorch
* **Data Processing:** Python, OpenCV
* **Dashboard:** Next.js, React, TypeScript
* **UI:** Tailwind CSS, shadcn/ui
* **AI Integration:** Featherless API

## 4. Architecture

The system follows this workflow:

```text
Camera-Trap Images
        |
        v
   MegaDetector
        |
        v
 Animal Detection
        |
        v
 Species Classifier
        |
        v
 Confidence Filtering
        |
        v
 Sightings Generation
        |
        v
 Structured Analytics
        |
        v
 WildSight Dashboard
        |
        v
 AI-Generated Insights
```

Additional documentation:

* `docs/architecture.md`
* `docs/data_contract.md`

## 5. Experimental Results

The following results were obtained from the implemented pipeline:

| Metric                                            | Result |
| ------------------------------------------------- | -----: |
| Images selected                                   |  5,000 |
| Images successfully downloaded                    |  3,914 |
| Camera locations                                  |    140 |
| Animal detections                                 |  6,305 |
| Species classifier validation accuracy            | 64.61% |
| Macro F1-score                                    |   0.56 |
| Weighted F1-score                                 |   0.64 |
| Predictions marked unidentified at 0.60 threshold |  2,098 |

The classifier was trained for 5 epochs using MobileNetV3-Small across 13 classes.

**Evaluation note:** The reported classifier accuracy is from a random validation split of 243 samples. It is not a held-out-camera evaluation. Performance may vary across camera locations and environmental conditions.

## 6. Uncertainty and Limitations

* Classification is limited to the supported training classes.
* Low-confidence predictions are marked as unidentified.
* Class imbalance can affect predictions for less frequent species.
* Night-time, infrared, and unclear images may reduce accuracy.
* Only a subset of the available camera-trap dataset was processed.
* Camera timestamps and sequence information may not always be reliable.
* Detection counts should not be interpreted as actual wildlife population estimates.

## 7. Live Demo

**Deployed Dashboard:** https://wildsight-eta.vercel.app/

**Demo Video:** To be added.

## 8. Setup Instructions

### Clone the repository

```bash
git clone https://github.com/Sudiksha2507/HFT26-TEAM-11.git
cd HFT26-TEAM-11
```

### Set up the Python environment

```bash
python -m venv .venv
```

Activate the environment:

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file using `.env.example` and add the required API configuration if using the Featherless integration.

### Run the dashboard

```bash
cd wildlife-dashboard
npm install
npm run dev
```

Open `http://localhost:3000` in your browser.

**Note:** Dataset files and trained model weights are not included in the repository. Download the required dataset subset and model weights separately.

## 9. Credits and Licenses

We acknowledge the open-source tools and resources used in this project:

* MegaDetector
* PyTorch-Wildlife
* PyTorch
* timm
* OpenCV
* Next.js
* React
* shadcn/ui
* Featherless

**Dataset:** Caltech Camera Traps, accessed through LILA. Please refer to the dataset documentation for licensing and attribution requirements.

**Project:** Developed by Team Helix for CBIT Hacktoberfest '26.

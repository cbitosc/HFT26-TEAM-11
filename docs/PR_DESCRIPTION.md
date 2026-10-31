**PR title:** `[SUBMISSION] TEAM-11 - Helix - Track Selection in Progress`
(confirm with organisers whether to swap in the track name)

## 📌 Solution Overview & Approach
Two-tier pipeline: MegaDetector filters empty frames, a fine-tuned classifier
identifies species on crops, bursts are merged into sightings, and a dashboard
plus insight agent report results with explicit uncertainty.

## 🏗️ Architecture & Tech Stack
See `docs/architecture.md`. Python (PyTorch-Wildlife, timm, OpenCV), SQLite/Supabase,
Next.js, shadcn/ui, Tailwind, Leaflet, Featherless API.

## 🚀 Local Setup
See README.md "Setup".

## 🎥 Demo Video / Live URL
<add link>

## 📸 Key Screenshots
<add screenshots from docs/>

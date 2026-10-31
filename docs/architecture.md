# Architecture

```
1 INGEST      Caltech Camera Traps subset + metadata (camera, timestamp, seq id)
      v
2 PERCEPTION  Tier 1: MegaDetector on every image (animal/person/vehicle/empty)
              Tier 2: species classifier on animal crops
              below threshold -> "Unidentified animal"
      v
3 STATE       SQLite (dev) / Supabase Postgres (deploy), or exported JSON
              images, detections, sightings (burst-merged), cameras, species
      v                         v
4 ANALYTICS API (Next.js)    5 INSIGHT AGENT (Featherless, aggregates only,
                                 template fallback)
      v                         v
6 DASHBOARD (Next.js + shadcn/ui + Tailwind + Leaflet)
```

Design rules: everything is precomputed; no model runs during the demo;
the LLM never sees raw images, only aggregates; every summary states its limits.

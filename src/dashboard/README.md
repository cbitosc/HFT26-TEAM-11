# Dashboard (Ria)
Next.js + shadcn/ui + Tailwind + Recharts + Leaflet.

```bash
cd src/dashboard
npx create-next-app@latest . --ts --tailwind --app
npx shadcn@latest init
npm i recharts leaflet react-leaflet
npm run dev
```
Reads `data/sightings.json` and `data/aggregates.json` (see docs/data_contract.md).
Required panels: overview cards, species chart, activity by hour, location map,
representative image + box + confidence, summary panel, "uncertainty and limits"
card, confidence slider that filters everything.

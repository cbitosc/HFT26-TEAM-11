# Data contract (pipeline -> dashboard)

Pipeline writes `src/dashboard/data/sightings.json` (array) and `aggregates.json`.

## Sighting
| field | type | notes |
|---|---|---|
| sighting_id | string | unique |
| camera_id | string | location id |
| start_time / end_time | ISO 8601 string | |
| species | string | `"unidentified"` if below threshold |
| confidence | float 0-1 | max confidence in burst |
| n_frames | int | frames merged |
| rep_image | string | relative path to crop |
| rep_box | [x,y,w,h] | normalised |

## Aggregates
`species_counts`, `hourly_counts[species][0..23]`, `location_counts`,
`pct_empty`, `pct_unidentified`, `mean_confidence`, `per_class_accuracy`,
`clock_flagged_cameras`.

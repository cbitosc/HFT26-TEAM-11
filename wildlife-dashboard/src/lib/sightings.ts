
import rawSightings from "@/data/sightings.json";
import aggregates from "@/data/aggregates.json";

export type Sighting = {
  id: string;
  species: string;
  location: string;
  time: string;
  confidence: number;
  status: string;
  image: string;
};

type PipelineSighting = {
  sighting_id: string;
  species: string;
  camera_id: string;
  start_time: string;
  confidence: number;
  rep_image: string;
  n_frames: number;
};

export const sightings: Sighting[] = (
  rawSightings as PipelineSighting[]
).map((s) => ({
  id: s.sighting_id,
  species: s.species,
  location: `Camera ${s.camera_id}`,
  time: s.start_time.replace("T", " "),
  confidence: Number((s.confidence * 100).toFixed(2)),
  status: "Not provided",
  image: s.rep_image,
}));

export const wildlifeAggregates = aggregates;

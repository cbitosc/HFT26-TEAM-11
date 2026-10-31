
import { sightings, wildlifeAggregates } from "@/lib/sightings";

const cameraActivity = Object.entries(
  sightings.reduce<Record<string, typeof sightings>>((acc, sighting) => {
    if (!acc[sighting.location]) {
      acc[sighting.location] = [];
    }

    acc[sighting.location].push(sighting);
    return acc;
  }, {})
)
  .map(([camera, records]) => ({
    camera,
    count: records.length,
    species: [...new Set(records.map((s) => s.species))],
    latest: records[records.length - 1],
  }))
  .sort((a, b) => b.count - a.count);

const identifiedSpecies = Object.keys(
  wildlifeAggregates.species_counts
).filter((species) => species !== "unidentified").length;

export default function MapPage() {
  return (
    <main className="min-h-screen bg-[#07130f] text-white p-8">
      <div className="max-w-7xl mx-auto">
        <a href="/" className="text-emerald-400 text-sm">
          ← Back to dashboard
        </a>

        <p className="text-emerald-400 text-sm tracking-widest mt-8">
          CAMERA INTELLIGENCE
        </p>

        <h1 className="text-4xl font-bold mt-2">
          Wildlife Camera Activity
        </h1>

        <p className="text-gray-400 mt-3 mb-8">
          Explore actual wildlife detections recorded by individual camera IDs.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-[#11251c] border border-emerald-900 rounded-xl p-5">
            <p className="text-gray-400 text-sm">Camera IDs</p>
            <p className="text-3xl font-bold mt-2">
              {cameraActivity.length}
            </p>
          </div>

          <div className="bg-[#11251c] border border-emerald-900 rounded-xl p-5">
            <p className="text-gray-400 text-sm">Total Sightings</p>
            <p className="text-3xl font-bold mt-2">
              {sightings.length.toLocaleString()}
            </p>
          </div>

          <div className="bg-[#11251c] border border-emerald-900 rounded-xl p-5">
            <p className="text-gray-400 text-sm">Species Identified</p>
            <p className="text-3xl font-bold mt-2">
              {identifiedSpecies}
            </p>
          </div>
        </div>

        <div className="flex items-center justify-between mb-5">
          <h2 className="text-xl font-semibold">Camera-wise Activity</h2>
          <span className="text-xs text-gray-400">
            {cameraActivity.length} cameras
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {cameraActivity.map((item) => (
            <article
              key={item.camera}
              className="bg-[#11251c] border border-emerald-900 rounded-xl overflow-hidden"
            >
              <img
                src={item.latest.image}
                alt={`Wildlife detected by ${item.camera}`}
                className="w-full h-56 object-cover"
              />

              <div className="p-5">
                <div className="flex justify-between items-center gap-3">
                  <h3 className="text-lg font-semibold">
                    {item.camera}
                  </h3>

                  <span className="text-emerald-300 text-sm">
                    {item.count} sightings
                  </span>
                </div>

                <p className="text-gray-400 text-sm mt-2">
                  Species detected: {item.species.length}
                </p>

                <div className="flex flex-wrap gap-2 mt-3">
                  {item.species.slice(0, 6).map((species) => (
                    <span
                      key={species}
                      className="bg-emerald-900/50 text-emerald-300 text-xs px-3 py-1 rounded-full capitalize"
                    >
                      {species}
                    </span>
                  ))}
                </div>

                <p className="text-gray-500 text-xs mt-4">
                  Latest recorded time: {item.latest.time}
                </p>
              </div>
            </article>
          ))}
        </div>

        <p className="text-gray-500 text-xs mt-8">
          Camera IDs are identifiers, not GPS coordinates. Geographic
          positions are not available in the current pipeline data.
        </p>
      </div>
    </main>
  );
}

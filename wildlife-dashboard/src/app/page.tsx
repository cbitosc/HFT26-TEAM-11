
import { sightings, wildlifeAggregates } from "@/lib/sightings";

const identifiedSpecies = Object.keys(
  wildlifeAggregates.species_counts
).filter((species) => species !== "unidentified").length;

const detections = sightings
  .filter((s, index, arr) =>
    arr.findIndex((item) => item.species === s.species) === index
  )
  .slice(0, 4);

const stats = [
  {
    label: "Camera traps deployed",
    value: Object.keys(wildlifeAggregates.location_counts).length.toString(),
    note: "Unique camera IDs",
  },
  {
    label: "Wildlife sightings",
    value: sightings.length.toLocaleString(),
    note: "Actual pipeline records",
  },
  {
    label: "Species identified",
    value: identifiedSpecies.toString(),
    note: "Excluding unidentified",
  },
  {
    label: "Unidentified detections",
    value: `${wildlifeAggregates.pct_unidentified}%`,
    note: "Pipeline statistics",
  },
];

export default function Home() {
  return (
    <main className="min-h-screen bg-[#101a16] text-[#edf2eb]">
      <aside className="border-b border-white/10 px-6 py-5 md:px-10">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">
              WILD<span className="text-[#a6c88a]">SIGHT</span>
            </h1>
            <p className="mt-1 text-xs tracking-[0.2em] text-gray-400">
              AI-POWERED WILDLIFE INTELLIGENCE
            </p>
          </div>
          <div className="flex items-center gap-2 rounded-full border border-green-400/20 bg-green-400/10 px-4 py-2 text-sm text-green-300">
            <span className="h-2 w-2 rounded-full bg-green-400" />
            Monitoring workspace
          </div>
        </div>
      </aside>

      <div className="mx-auto max-w-7xl px-6 py-9 md:px-10">
        <nav className="flex flex-wrap gap-3 mb-8">
          <a href="/" className="px-4 py-2 rounded-lg bg-emerald-800 text-white hover:bg-emerald-700">
            Dashboard
          </a>
          <a href="/sightings" className="px-4 py-2 rounded-lg bg-[#11251c] border border-emerald-900 text-white hover:bg-emerald-900">
            Wildlife Sightings
          </a>
          <a href="/map" className="px-4 py-2 rounded-lg bg-[#11251c] border border-emerald-900 text-white hover:bg-emerald-900">
            Monitoring Map
          </a>
          <a href="/insights" className="px-4 py-2 rounded-lg bg-[#11251c] border border-emerald-900 text-white hover:bg-emerald-900">
            Insight Agent
          </a>
        </nav>

        <section className="mb-8">
          <p className="text-sm text-[#a6c88a]">CONSERVATION INTELLIGENCE</p>
          <h2 className="mt-2 text-3xl font-bold md:text-4xl">
            Wildlife Monitoring
          </h2>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-gray-400">
            Observe wildlife activity, review camera-trap detections and
            explore AI-generated conservation insights.
          </p>
        </section>

        <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {stats.map((stat) => (
            <div
              key={stat.label}
              className="rounded-2xl border border-white/10 bg-[#192720] p-5"
            >
              <p className="text-sm text-gray-400">{stat.label}</p>
              <p className="mt-4 text-3xl font-bold">{stat.value}</p>
              <p className="mt-2 text-xs text-[#a6c88a]">{stat.note}</p>
            </div>
          ))}
        </section>

        <section className="mt-10">
          <div className="mb-5">
            <h3 className="text-xl font-semibold">Camera-trap activity</h3>
            <p className="mt-1 text-sm text-gray-400">
              Actual representative images from wildlife detections
            </p>
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            {detections.map((item) => (
              <article
                key={item.id}
                className="overflow-hidden rounded-2xl border border-white/10 bg-[#192720]"
              >
                <div className="relative h-64 bg-[#25372d]">
                  <img
                    src={item.image}
                    alt={item.species}
                    className="h-full w-full object-cover"
                  />
                  <span className="absolute left-4 top-4 rounded-full bg-black/70 px-3 py-1 text-xs text-green-300">
                    CAMERA TRAP IMAGE
                  </span>
                </div>
                <div className="p-5">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div>
                      <h4 className="text-lg font-semibold capitalize">
                        {item.species}
                      </h4>
                      <p className="mt-1 text-sm text-gray-400">
                        {item.location}
                      </p>
                    </div>
                    <span className="rounded-lg bg-green-400/10 px-3 py-2 text-sm text-green-300">
                      {item.confidence.toFixed(2)}%
                    </span>
                  </div>
                  <p className="mt-4 text-xs text-gray-500">
                    Capture time: {item.time}
                  </p>
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className="mt-10 rounded-2xl border border-[#718d65]/30 bg-[#1b2d23] p-6">
          <p className="text-sm font-semibold text-[#b5d39d]">
            CONSERVATION INSIGHT
          </p>
          <h3 className="mt-3 text-xl font-semibold">
            From camera traps to actionable intelligence
          </h3>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-gray-300">
            The platform processes camera-trap images, identifies wildlife
            species, analyses detection patterns and supports conservation
            monitoring through AI-powered insights.
          </p>
          <p className="mt-4 text-xs text-gray-500">
            Wildlife statistics sourced from the detection pipeline.
          </p>
        </section>

        <footer className="mt-12 border-t border-white/10 py-6 text-center text-xs text-gray-500">
          WILDSIGHT · Wildlife Conservation Intelligence Platform
        </footer>
      </div>
    </main>
  );
}

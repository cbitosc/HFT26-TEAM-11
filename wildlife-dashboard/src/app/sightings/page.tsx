
"use client";

import { useState } from "react";
import { sightings, wildlifeAggregates } from "@/lib/sightings";

const PAGE_SIZE = 25;

export default function SightingsPage() {
  const [search, setSearch] = useState("");
  const [speciesFilter, setSpeciesFilter] = useState("All");
  const [page, setPage] = useState(1);

  const speciesList = [
    "All",
    ...Array.from(new Set(sightings.map((s) => s.species))).sort(),
  ];

  const filteredSightings = sightings.filter((s) => {
    const matchesSearch =
      s.species.toLowerCase().includes(search.toLowerCase()) ||
      s.location.toLowerCase().includes(search.toLowerCase());

    const matchesSpecies =
      speciesFilter === "All" || s.species === speciesFilter;

    return matchesSearch && matchesSpecies;
  });

  const totalPages = Math.ceil(filteredSightings.length / PAGE_SIZE);
  const startIndex = (page - 1) * PAGE_SIZE;
  const currentSightings = filteredSightings.slice(
    startIndex,
    startIndex + PAGE_SIZE
  );

  const avgConfidence =
    sightings.reduce((sum, s) => sum + s.confidence, 0) /
    sightings.length;

  const identifiedSpecies = Object.keys(
    wildlifeAggregates.species_counts
  ).filter((species) => species !== "unidentified").length;

  return (
    <main className="min-h-screen bg-[#071812] text-white p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-emerald-400">
          Wildlife Sightings
        </h1>

        <p className="text-gray-400 mt-2">
          Explore and filter recorded wildlife detections.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5 my-8">
          <div className="bg-[#10291e] p-6 rounded-xl">
            <p className="text-gray-400">Total Sightings</p>
            <h2 className="text-3xl font-bold mt-2">
              {sightings.length.toLocaleString()}
            </h2>
          </div>

          <div className="bg-[#10291e] p-6 rounded-xl">
            <p className="text-gray-400">Identified Species</p>
            <h2 className="text-3xl font-bold mt-2">
              {identifiedSpecies}
            </h2>
          </div>

          <div className="bg-[#10291e] p-6 rounded-xl">
            <p className="text-gray-400">Average Confidence</p>
            <h2 className="text-3xl font-bold mt-2">
              {avgConfidence.toFixed(1)}%
            </h2>
          </div>
        </div>

        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <input
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            placeholder="Search species or camera..."
            className="flex-1 bg-[#10291e] border border-gray-700 rounded-lg p-3 outline-none focus:border-emerald-500"
          />

          <select
            value={speciesFilter}
            onChange={(e) => {
              setSpeciesFilter(e.target.value);
              setPage(1);
            }}
            className="bg-[#10291e] border border-gray-700 rounded-lg p-3"
          >
            {speciesList.map((species) => (
              <option key={species} value={species}>
                {species}
              </option>
            ))}
          </select>
        </div>

        <div className="bg-[#10291e] rounded-xl overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-[#183a2a] text-emerald-300">
              <tr>
                <th className="p-4">Species</th>
                <th className="p-4">Camera</th>
                <th className="p-4">Detection Time</th>
                <th className="p-4">Confidence</th>
                <th className="p-4">Representative Image</th>
              </tr>
            </thead>

            <tbody>
              {currentSightings.map((s) => (
                <tr key={s.id} className="border-t border-gray-700">
                  <td className="p-4 font-medium capitalize">
                    {s.species}
                  </td>

                  <td className="p-4 text-gray-300">{s.location}</td>

                  <td className="p-4 text-gray-300">{s.time}</td>

                  <td className="p-4">
                    <span className="text-emerald-400">
                      {s.confidence.toFixed(2)}%
                    </span>
                  </td>

                  <td className="p-4">
                    <img
                      src={s.image}
                      alt={s.species}
                      className="w-20 h-14 object-cover rounded-lg"
                    />
                  </td>
                </tr>
              ))}

              {filteredSightings.length === 0 && (
                <tr>
                  <td colSpan={5} className="p-8 text-center text-gray-400">
                    No sightings found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        <div className="flex flex-col sm:flex-row justify-between items-center gap-4 mt-5">
          <p className="text-sm text-gray-400">
            Showing {filteredSightings.length === 0 ? 0 : startIndex + 1}–
            {Math.min(startIndex + PAGE_SIZE, filteredSightings.length)} of{" "}
            {filteredSightings.length.toLocaleString()} sightings
          </p>

          <div className="flex gap-3 items-center">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
              className="px-4 py-2 rounded-lg bg-[#183a2a] disabled:opacity-40 hover:bg-emerald-900"
            >
              Previous
            </button>

            <span className="text-sm text-gray-300">
              Page {page} of {Math.max(totalPages, 1)}
            </span>

            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page >= totalPages}
              className="px-4 py-2 rounded-lg bg-[#183a2a] disabled:opacity-40 hover:bg-emerald-900"
            >
              Next
            </button>
          </div>
        </div>

        <p className="text-xs text-gray-500 mt-5">
          Data sourced from the wildlife detection pipeline. Camera IDs are
          identifiers, not geographic coordinates.
        </p>
      </div>
    </main>
  );
}

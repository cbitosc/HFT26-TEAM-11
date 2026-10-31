
import { sightings, wildlifeAggregates } from "@/lib/sightings";

export async function POST(req: Request) {
  try {
    const { question } = await req.json();

    if (typeof question !== "string" || !question.trim()) {
      return Response.json(
        { error: "Please enter a question." },
        { status: 400 }
      );
    }

    const apiKey = process.env.FEATHERLESS_API_KEY;

    if (!apiKey) {
      return Response.json(
        { error: "Featherless API key is missing." },
        { status: 500 }
      );
    }

    const speciesCounts = wildlifeAggregates.species_counts;
    const cameraCounts = wildlifeAggregates.location_counts;

    const topSpecies = Object.entries(speciesCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 14);

    const topCameras = Object.entries(cameraCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 15);

    const sampleRecords = [...sightings]
      .sort((a, b) => b.confidence - a.confidence)
      .slice(0, 10)
      .map((s) => ({
        species: s.species,
        camera: s.location,
        time: s.time,
        confidence: `${s.confidence}%`,
      }));

    const wildlifeContext = {
      totalSightings: sightings.length,
      identifiedSpecies: topSpecies.filter(
        ([species]) => species !== "unidentified"
      ).length,
      averageConfidence: `${(wildlifeAggregates.mean_confidence * 100).toFixed(2)}%`,
      unidentifiedPercentage: wildlifeAggregates.pct_unidentified,
      emptyDetectionPercentage: wildlifeAggregates.pct_empty,
      speciesCounts: topSpecies,
      topCameraActivity: topCameras,
      hourlyActivity: wildlifeAggregates.hourly_counts,
      sampleHighConfidenceRecords: sampleRecords,
      dataNote:
        "Historical camera-trap pipeline output. This is not live monitoring data. Camera IDs are identifiers, not GPS locations. Verification status and forest-zone coordinates are not provided.",
    };

    const response = await fetch(
      "https://api.featherless.ai/v1/chat/completions",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${apiKey}`,
          "X-Title": "WildSight",
        },
        body: JSON.stringify({
          model: "Qwen/Qwen2.5-7B-Instruct",
          messages: [
            {
              role: "system",
              content: `You are WildSight, an AI wildlife conservation intelligence assistant.

Answer questions using only the supplied wildlife dataset.
Be clear, professional, and concise.

Rules:
1. Use the supplied statistics when answering numerical questions.
2. Never invent species, sightings, locations, coordinates, or camera details.
3. Camera IDs identify cameras; they do not provide geographic locations.
4. Do not claim that records are verified or pending. Verification status is unavailable.
5. The dataset is historical pipeline output, not live monitoring.
6. If the dataset does not contain enough information, clearly say so.
7. You may suggest conservation actions based on observed patterns, but distinguish suggestions from proven conclusions.
8. Format answers with short paragraphs or bullet points when useful.

WILDLIFE DATA:
${JSON.stringify(wildlifeContext, null, 2)}`,
            },
            {
              role: "user",
              content: question.trim(),
            },
          ],
          temperature: 0.3,
          max_tokens: 600,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      return Response.json(
        {
          error:
            data.error?.message || "Featherless request failed.",
        },
        { status: response.status }
      );
    }

    return Response.json({
      answer:
        data.choices?.[0]?.message?.content ||
        "No response generated.",
    });
  } catch {
    return Response.json(
      { error: "Unable to connect to the AI service." },
      { status: 500 }
    );
  }
}

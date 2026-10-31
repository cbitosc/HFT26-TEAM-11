"""Insight agent. Sends AGGREGATES ONLY to the LLM; template fallback if it fails."""
import json, os

SYSTEM_PROMPT = (
    "You summarise wildlife camera-trap statistics for researchers. "
    "Use ONLY the numbers provided. Do not invent species, places or causes. "
    "Reply with two sections: 'Summary' (plain language) and "
    "'What we cannot conclude' (uncertainty, unidentified share, data limits)."
)


def fallback_summary(agg: dict) -> str:
    counts = agg.get("species_counts", {})
    known = {k: v for k, v in counts.items() if k != "unidentified"}
    top = max(known, key=known.get) if known else "none"
    return (
        "Summary\n"
        f"{agg.get('n_sightings', 0)} sightings recorded; {agg.get('pct_empty', 0)}% of images "
        f"were empty and filtered out. Most frequent identified species: {top}.\n\n"
        "What we cannot conclude\n"
        f"{agg.get('pct_unidentified', 0)}% of sightings are unidentified and mean confidence is "
        f"{agg.get('mean_confidence', 0)}. Results come from a subset of cameras and are not "
        "population estimates."
    )


def llm_summary(agg: dict) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(base_url="https://api.featherless.ai/v1",
                        api_key=os.environ["FEATHERLESS_API_KEY"])
        r = client.chat.completions.create(
            model=os.environ["FEATHERLESS_MODEL"],
            messages=[{"role": "system", "content": SYSTEM_PROMPT},
                      {"role": "user", "content": json.dumps(agg)}],
            timeout=20,
        )
        return r.choices[0].message.content
    except Exception:
        return fallback_summary(agg)

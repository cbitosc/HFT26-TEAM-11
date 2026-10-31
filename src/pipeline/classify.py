"""Tier 2: species classification on animal crops with threshold -> unidentified."""
from .config import SPECIES_THRESHOLD, UNIDENTIFIED


def apply_threshold(species: str, confidence: float, threshold: float = SPECIES_THRESHOLD):
    """Return (label, confidence); below threshold becomes 'unidentified'."""
    return (species, confidence) if confidence >= threshold else (UNIDENTIFIED, confidence)

"""Approved binary-posterior uncertainty representation for shared autonomy."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


class UncertaintyError(ValueError):
    """Raised when a binary Bayesian posterior is invalid."""


@dataclass(frozen=True)
class BinaryUncertainty:
    """Shannon entropy in bits for one validated binary Bayesian posterior."""

    posterior: tuple[float, float]
    entropy_bits: float

    def validate(self) -> None:
        validated = validate_binary_posterior(self.posterior)
        expected_entropy = shannon_entropy_bits(validated)
        if not np.isclose(self.entropy_bits, expected_entropy, rtol=0.0, atol=1e-12):
            raise UncertaintyError("Entropy must match the supplied binary Bayesian posterior.")


def estimate_binary_uncertainty(
    posterior: tuple[float, float] | list[float] | np.ndarray,
) -> BinaryUncertainty:
    """Compute the approved Shannon entropy of a binary posterior in bits."""
    validated = validate_binary_posterior(posterior)
    return BinaryUncertainty(
        posterior=(float(validated[0]), float(validated[1])),
        entropy_bits=shannon_entropy_bits(validated),
    )


def shannon_entropy_bits(posterior: tuple[float, float] | list[float] | np.ndarray) -> float:
    """Return binary Shannon entropy in base-2 units, treating 0 log2(0) as zero."""
    validated = validate_binary_posterior(posterior)
    positive = validated[validated > 0.0]
    return float(-np.sum(positive * np.log2(positive)))


def validate_binary_posterior(
    posterior: tuple[float, float] | list[float] | np.ndarray,
) -> np.ndarray:
    """Validate the binary posterior contract without silently normalizing it."""
    values = np.asarray(posterior, dtype=np.float64)
    if values.ndim != 1 or values.shape != (2,):
        raise UncertaintyError("Binary posterior must contain exactly two values.")
    if not np.isfinite(values).all():
        raise UncertaintyError("Binary posterior must be finite.")
    if (values < 0.0).any():
        raise UncertaintyError("Binary posterior must be non-negative.")
    if not np.isclose(values.sum(), 1.0, rtol=0.0, atol=1e-8):
        raise UncertaintyError("Binary posterior must sum to 1.0.")
    return values

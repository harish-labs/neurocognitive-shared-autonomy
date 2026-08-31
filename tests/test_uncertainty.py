from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.cognitive import uncertainty


def test_uniform_binary_posterior_has_one_bit_of_entropy() -> None:
    assert uncertainty.shannon_entropy_bits([0.5, 0.5]) == pytest.approx(1.0)


def test_ninety_ten_binary_posterior_has_approved_entropy_equivalent() -> None:
    assert uncertainty.shannon_entropy_bits([0.9, 0.1]) == pytest.approx(0.4689955936, abs=1e-10)


def test_uncertainty_estimate_preserves_the_validated_binary_posterior() -> None:
    estimate = uncertainty.estimate_binary_uncertainty([0.75, 0.25])

    assert estimate.posterior == (0.75, 0.25)
    assert estimate.entropy_bits == pytest.approx(0.8112781245, abs=1e-10)


@pytest.mark.parametrize(
    "posterior",
    ([0.5], [0.2, 0.3, 0.5], [[0.5, 0.5]], [np.nan, 1.0], [np.inf, 0.0], [-0.1, 1.1], [0.4, 0.4]),
)
def test_invalid_binary_posterior_shape_or_probability_contract_is_rejected(posterior: object) -> None:
    with pytest.raises(uncertainty.UncertaintyError):
        uncertainty.estimate_binary_uncertainty(posterior)  # type: ignore[arg-type]


def test_uncertainty_rejects_a_stored_entropy_that_does_not_match_the_posterior() -> None:
    estimate = uncertainty.BinaryUncertainty(posterior=(0.9, 0.1), entropy_bits=1.0)

    with pytest.raises(uncertainty.UncertaintyError, match="must match"):
        estimate.validate()

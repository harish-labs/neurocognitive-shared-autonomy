from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.models import calibration, csp_lda, eegnet
from tests.test_csp_lda import make_partitioned_epochs as make_csp_partitioned_epochs
from tests.test_eegnet import make_partitioned_epochs as make_eegnet_partitioned_epochs


def test_fit_model_specific_calibrator_uses_approved_method_per_decoder(monkeypatch) -> None:
    csp_epochs = make_csp_partitioned_epochs()
    eeg_epochs = make_eegnet_partitioned_epochs()
    monkeypatch.setattr(eegnet, "MAX_EPOCHS", 1)
    monkeypatch.setattr(eegnet, "EARLY_STOPPING_PATIENCE", 1)

    csp_result = csp_lda.fit_csp_lda(csp_epochs)
    eeg_result = eegnet.fit_eegnet(eeg_epochs)

    csp_calibrator = calibration.fit_model_specific_calibrator(
        model_family=calibration.CSP_LDA_MODEL_FAMILY,
        decoder=csp_result.decoder,
        epochs=csp_epochs,
    )
    eeg_calibrator = calibration.fit_model_specific_calibrator(
        model_family=calibration.EEGNET_MODEL_FAMILY,
        decoder=eeg_result.decoder,
        epochs=eeg_epochs,
    )

    assert csp_calibrator.method == calibration.PLATT_SCALING_METHOD
    assert eeg_calibrator.method == calibration.TEMPERATURE_SCALING_METHOD


def test_fit_eegnet_temperature_scaler_uses_validation_partition_only(monkeypatch) -> None:
    epochs = make_eegnet_partitioned_epochs()
    validation_count = int((epochs.metadata["partition"] == "validation").sum())
    monkeypatch.setattr(eegnet, "MAX_EPOCHS", 1)
    monkeypatch.setattr(eegnet, "EARLY_STOPPING_PATIENCE", 1)
    training_result = eegnet.fit_eegnet(epochs)
    seen_sizes: list[int] = []
    original_predict_logits = training_result.decoder.predict_logits

    def spy_predict_logits(epoch_subset):
        seen_sizes.append(len(epoch_subset))
        return original_predict_logits(epoch_subset)

    monkeypatch.setattr(training_result.decoder, "predict_logits", spy_predict_logits)

    calibration.fit_eegnet_temperature_scaler(training_result.decoder, epochs)

    assert seen_sizes == [validation_count]


def test_fit_csp_lda_platt_scaler_uses_validation_partition_only(monkeypatch) -> None:
    epochs = make_csp_partitioned_epochs()
    validation_count = int((epochs.metadata["partition"] == "validation").sum())
    training_result = csp_lda.fit_csp_lda(epochs)
    seen_sizes: list[int] = []
    original_predict_proba = training_result.decoder.predict_proba

    def spy_predict_proba(epoch_subset):
        seen_sizes.append(len(epoch_subset))
        return original_predict_proba(epoch_subset)

    monkeypatch.setattr(training_result.decoder, "predict_proba", spy_predict_proba)

    calibration.fit_csp_lda_platt_scaler(training_result.decoder, epochs)

    assert seen_sizes == [validation_count]


def test_protected_test_and_final_test_do_not_influence_calibrator_fitting(monkeypatch) -> None:
    csp_epochs = make_csp_partitioned_epochs()
    eeg_epochs = make_eegnet_partitioned_epochs()
    poisoned_csp = csp_epochs.copy()
    poisoned_eeg = eeg_epochs.copy()

    poisoned_csp_data = poisoned_csp.get_data(copy=True)
    poisoned_eeg_data = poisoned_eeg.get_data(copy=True)
    protected_mask_csp = poisoned_csp.metadata["partition"].isin(("test", "final_test")).to_numpy()
    protected_mask_eeg = poisoned_eeg.metadata["partition"].isin(("test", "final_test")).to_numpy()
    poisoned_csp_data[protected_mask_csp, :, :] *= -30.0
    poisoned_eeg_data[protected_mask_eeg, :, :] *= 40.0

    poisoned_csp._data = poisoned_csp_data  # noqa: SLF001
    poisoned_eeg._data = poisoned_eeg_data  # noqa: SLF001

    monkeypatch.setattr(eegnet, "MAX_EPOCHS", 1)
    monkeypatch.setattr(eegnet, "EARLY_STOPPING_PATIENCE", 1)

    base_csp_result = csp_lda.fit_csp_lda(csp_epochs)
    poisoned_csp_result = csp_lda.fit_csp_lda(poisoned_csp)
    base_csp_calibrator = calibration.fit_csp_lda_platt_scaler(base_csp_result.decoder, csp_epochs)
    poisoned_csp_calibrator = calibration.fit_csp_lda_platt_scaler(poisoned_csp_result.decoder, poisoned_csp)

    base_eeg_result = eegnet.fit_eegnet(eeg_epochs)
    poisoned_eeg_result = eegnet.fit_eegnet(poisoned_eeg)
    base_eeg_calibrator = calibration.fit_eegnet_temperature_scaler(base_eeg_result.decoder, eeg_epochs)
    poisoned_eeg_calibrator = calibration.fit_eegnet_temperature_scaler(poisoned_eeg_result.decoder, poisoned_eeg)

    assert base_csp_calibrator == poisoned_csp_calibrator
    assert base_eeg_calibrator == poisoned_eeg_calibrator


def test_identity_calibration_preserves_probabilities_and_model_family() -> None:
    calibrator = calibration.build_identity_calibrator(model_family=calibration.CSP_LDA_MODEL_FAMILY)
    probabilities = np.asarray([[0.25, 0.75], [0.8, 0.2]], dtype=np.float64)

    calibrated = calibrator.predict_proba(probabilities)

    assert calibrator.method == calibration.IDENTITY_METHOD
    assert calibrator.model_family == calibration.CSP_LDA_MODEL_FAMILY
    np.testing.assert_allclose(calibrated, probabilities, atol=1e-8)


def test_calibrators_preserve_probability_normalization_and_class_order(monkeypatch) -> None:
    csp_epochs = make_csp_partitioned_epochs()
    eeg_epochs = make_eegnet_partitioned_epochs()
    monkeypatch.setattr(eegnet, "MAX_EPOCHS", 1)
    monkeypatch.setattr(eegnet, "EARLY_STOPPING_PATIENCE", 1)

    csp_result = csp_lda.fit_csp_lda(csp_epochs)
    eeg_result = eegnet.fit_eegnet(eeg_epochs)
    csp_calibrator = calibration.fit_csp_lda_platt_scaler(csp_result.decoder, csp_epochs)
    eeg_calibrator = calibration.fit_eegnet_temperature_scaler(eeg_result.decoder, eeg_epochs)

    csp_probabilities = csp_calibrator.predict_proba(
        csp_result.decoder.predict_proba(csp_epochs[csp_epochs.metadata["partition"] == "test"])
    )
    eeg_probabilities = eeg_calibrator.predict_proba(
        eeg_result.decoder.predict_logits(eeg_epochs[eeg_epochs.metadata["partition"] == "test"])
    )

    assert csp_calibrator.class_labels == ("left", "right")
    assert eeg_calibrator.class_labels == ("left", "right")
    np.testing.assert_allclose(csp_probabilities.sum(axis=1), np.ones(len(csp_probabilities)), atol=1e-6)
    np.testing.assert_allclose(eeg_probabilities.sum(axis=1), np.ones(len(eeg_probabilities)), atol=1e-6)


def test_temperature_scaling_changes_logits_but_keeps_shape() -> None:
    calibrator = calibration.TemperatureScalingCalibrator(temperature=2.0)
    logits = np.asarray([[2.0, 0.0], [0.0, 2.0]], dtype=np.float64)

    calibrated = calibrator.predict_proba(logits)

    assert calibrated.shape == (2, 2)
    assert calibrated[0, 0] < 0.88079708
    assert calibrated[1, 1] < 0.88079708


def test_platt_scaling_changes_positive_class_probability_but_keeps_normalization() -> None:
    calibrator = calibration.PlattScalingCalibrator(slope=0.5, intercept=-0.25)
    probabilities = np.asarray([[0.9, 0.1], [0.4, 0.6]], dtype=np.float64)

    calibrated = calibrator.predict_proba(probabilities)

    assert calibrated.shape == (2, 2)
    assert calibrated[0, 1] != pytest.approx(probabilities[0, 1])
    np.testing.assert_allclose(calibrated.sum(axis=1), np.ones(2), atol=1e-6)


def test_ece_uses_exactly_ten_equal_width_bins_over_zero_to_one() -> None:
    probabilities = np.asarray(
        [
            [1.0, 0.0],
            [0.95, 0.05],
            [0.85, 0.15],
            [0.75, 0.25],
            [0.65, 0.35],
            [0.55, 0.45],
            [0.45, 0.55],
            [0.35, 0.65],
            [0.25, 0.75],
            [0.15, 0.85],
            [0.05, 0.95],
        ],
        dtype=np.float64,
    )
    true_labels = np.asarray(
        ["left", "left", "left", "left", "left", "left", "right", "right", "right", "right", "right"]
    )

    metrics = calibration.evaluate_calibration(probabilities, true_labels)

    assert metrics.bin_count == 10
    assert len(metrics.reliability_bins) == 10
    assert metrics.reliability_bins[0].lower_bound == 0.0
    assert metrics.reliability_bins[0].upper_bound == 0.1
    assert metrics.reliability_bins[-1].lower_bound == 0.9
    assert metrics.reliability_bins[-1].upper_bound == 1.0
    assert sum(reliability_bin.sample_count for reliability_bin in metrics.reliability_bins) == len(probabilities)


def test_brier_score_matches_binary_right_class_definition() -> None:
    probabilities = np.asarray([[0.8, 0.2], [0.1, 0.9], [0.6, 0.4]], dtype=np.float64)
    true_indices = np.asarray([0, 1, 1], dtype=np.int64)

    brier = calibration.brier_score(probabilities, true_indices)

    expected = ((0.2 - 0.0) ** 2 + (0.9 - 1.0) ** 2 + (0.4 - 1.0) ** 2) / 3.0
    assert brier == pytest.approx(expected)


def test_calibration_module_is_compatible_with_accepted_decoder_paths(monkeypatch) -> None:
    csp_epochs = make_csp_partitioned_epochs()
    eeg_epochs = make_eegnet_partitioned_epochs()
    monkeypatch.setattr(eegnet, "MAX_EPOCHS", 1)
    monkeypatch.setattr(eegnet, "EARLY_STOPPING_PATIENCE", 1)

    csp_result = csp_lda.fit_csp_lda(csp_epochs)
    eeg_result = eegnet.fit_eegnet(eeg_epochs)
    csp_calibrator = calibration.fit_model_specific_calibrator(
        model_family=calibration.CSP_LDA_MODEL_FAMILY,
        decoder=csp_result.decoder,
        epochs=csp_epochs,
    )
    eeg_calibrator = calibration.fit_model_specific_calibrator(
        model_family=calibration.EEGNET_MODEL_FAMILY,
        decoder=eeg_result.decoder,
        epochs=eeg_epochs,
    )

    test_csp_epochs = csp_epochs[csp_epochs.metadata["partition"] == "test"]
    test_eeg_epochs = eeg_epochs[eeg_epochs.metadata["partition"] == "test"]
    csp_metrics = calibration.evaluate_calibration(
        csp_calibrator.predict_proba(csp_result.decoder.predict_proba(test_csp_epochs)),
        test_csp_epochs.metadata["semantic_label"].astype(str).to_numpy(),
    )
    eeg_metrics = calibration.evaluate_calibration(
        eeg_calibrator.predict_proba(eeg_result.decoder.predict_logits(test_eeg_epochs)),
        test_eeg_epochs.metadata["semantic_label"].astype(str).to_numpy(),
    )

    assert csp_metrics.class_labels == ("left", "right")
    assert eeg_metrics.class_labels == ("left", "right")
    assert np.isfinite(csp_metrics.expected_calibration_error)
    assert np.isfinite(eeg_metrics.expected_calibration_error)
    assert np.isfinite(csp_metrics.brier_score)
    assert np.isfinite(eeg_metrics.brier_score)

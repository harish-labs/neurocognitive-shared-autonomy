"""Read-only presentation and demonstration layer for accepted project results."""

from src.app.result_loader import PresentationData, ResultIntegrityError, load_presentation_data

__all__ = ["PresentationData", "ResultIntegrityError", "load_presentation_data"]

# Final Demonstration

The dashboard combines accepted M7 result inspection with a deterministic explanatory end-to-end fixture. The fixture calls the accepted production Bayes, entropy, shared-autonomy, and A* interfaces, but uses fixed probabilities; it is not a new experiment and does not access protected EEG.

## Run

```powershell
python -m src.app.dashboard --smoke
python -m streamlit run src/app/dashboard.py
```

Open the local Streamlit URL, use the sidebar in order, and finish on **Interactive Demo**.

## Presenter boundary

Say “public prerecorded EEG,” “Offline EEG Replay / Simulated Real-Time BCI,” “deterministic simulated-human policy,” and “2D simulated Search & Rescue.” Never imply live acquisition, a real participant study, a physical robot, clinical benefit, deployment, or certified safety.

The exact narration is in `DEMO_SCRIPT.md`; shot order is in `DEMO_STORYBOARD.md`.

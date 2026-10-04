# Eye-tracking and pupillometry review

Use this reference for gaze, fixation, AOI, pupil, blink, calibration, or validation questions.

- Identify the current device, SDK or export format, coordinate frames, timestamps, synchronization path, and units from live project authority.
- Distinguish calibration accuracy, validation accuracy, precision, tracking ratio, data loss, and drift. Validation measures performance; recalibration is only one possible response.
- Relate AOI geometry and gaze-event definitions to the spatial and temporal resolution required by the construct.
- For pupil data, consider illumination, gaze angle, foreshortening, accommodation, blink and eyelid artifacts, device confidence, and task-evoked timing.

Inspect raw traces and missingness before setting artifact rules. Define how invalid samples are flagged, when gaps can be reconstructed, how smoothing or resampling changes temporal information, and how baselines or windows answer the scientific question. Preserve raw samples and emit explicit quality flags. Coordinate with `statistics` on sensitivity analyses before `coding` implements an approved pipeline.

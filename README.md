# Permit Duration Estimator

A small, local web app that estimates historical permit processing time based on the permit's
work type. It uses the results already recorded in `data_test.ipynb`; the original CSV files are
not required to run the app.

## Run it

Open `index.html` in a web browser. No installation or server is required. Alternatively, from this
directory, run `python3 -m http.server 8000` and visit <http://localhost:8000>.

## How estimates are calculated

The notebook measures calendar days between permit submission and issuance, keeps one row per
permit number, and groups the results by `Work_Type`. The app displays the median as the typical
time and the 90th percentile as a planning estimate.

| Work type | Historical permits | Median | 90th percentile |
| --- | ---: | ---: | ---: |
| Addition | 1,575 | 42 days | 168.6 days |
| New Building | 8,730 | 21 days | 103.1 days |
| Renovation | 4,571 | 25 days | 100 days |

Other entered details are shown alongside the estimate but do not change it: the notebook's
calculation only tested work type. These are historical estimates, not guaranteed permit timelines.
The form runs in the browser and does not upload permit details.

## Clean the source CSVs

The original CSVs in `~/Desktop/side_quest` are left unchanged. To create analysis-ready copies
inside `cleaned_data/`, run:

```sh
python3 clean_data.py
```

The script trims whitespace and standardizes common null markers to blank cells. It keeps optional
blank values rather than discarding otherwise useful rows. In `PLC_permit.csv`, it excludes rows
without a permit number, work type, valid submission date, or valid issuance date; those fields are
needed for the submission-to-issuance estimate. The two dates are written in `YYYY-MM-DD` format.
In `PLC_permit_time.csv`, it excludes rows without a permit number, issuance stage, or finite,
non-negative duration. Repeated permit numbers and timeline stages are retained.

The cleaned permit file is a subset of issued permits suitable for duration analysis, not a
replacement for the full source data. Review the printed kept/excluded row counts when rerunning
the script.

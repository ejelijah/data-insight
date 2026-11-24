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

# Track 1: Instrument Validation

## Overview

The HamSCI ionosonde at W2NAF (Spring Brook Twp, PA) is a new instrument that has not been fully validated. Before its measurements can be used for scientific analysis or fed into propagation prediction systems, we need rigorous quantitative validation against professional Digisonde instruments.

The ionosonde is currently sounding every 5 minutes at 3.5 MHz and 7 MHz, producing virtual height measurements. The research engineer has begun creating overlay plots comparing these against Digisonde data from Alpena, MI (via the UMass Lowell GIRO database). This track formalizes and extends that work into a complete validation study.

### Objectives

1. Build reusable data infrastructure for retrieving and comparing ionosonde data
2. Quantitatively validate HamSCI virtual height measurements against professional Digisonde data
3. Characterize the instrument's detection limits and observational coverage
4. Produce publication-quality validation results

### Validation Station

- **Primary:** Alpena, MI Digisonde (currently used for comparison)
- **Stretch:** Wallops Island, VA; Millstone Hill, MA (for distance-dependence analysis)

---

## Requirements

### R1 — GIRO Data Retrieval Module

**Goal:** Automated, repeatable retrieval of Digisonde data from the GIRO DIDBase for any station and time range.

**Functional Requirements:**

- R1.1: Retrieve data from the GIRO DIDBase API (`https://giro.uml.edu/didbase/`) using HTTP requests.
- R1.2: Support retrieval for any GIRO station by URSI code (e.g., Alpena = `AL945`).
- R1.3: Retrieve the following parameters at minimum:
  - `foF2` — F2 layer critical frequency (MHz)
  - `hmF2` — F2 layer peak height (km)
  - `foE` — E layer critical frequency (MHz)
  - `MUF(3000)F2` — Maximum usable frequency for 3000 km path (MHz)
  - `h'F2` — Minimum virtual height of F2 layer (km)
  - Virtual heights at specific frequencies if available (h'(3.5 MHz), h'(7.0 MHz))
- R1.4: Accept start/end datetime range as input parameters.
- R1.5: Return data as a pandas DataFrame with consistent column names and UTC timestamps.
- R1.6: Handle missing data gracefully (GIRO uses value `9999` or empty fields for missing data).
- R1.7: Cache retrieved data locally to avoid redundant API calls during development and analysis.
- R1.8: Include basic error handling for network failures, invalid station codes, and empty responses.

**Non-Functional Requirements:**

- R1.9: Design as a reusable Python module (not a one-off script) importable by other modules.
- R1.10: Follow project code style (PEP 8, Google-style docstrings).
- R1.11: Include unit tests with sample/mock data.

**Acceptance Criteria:**

- [ ] Can retrieve foF2 and hmF2 time series from Alpena for a specified date range
- [ ] Returns a clean DataFrame with no `9999` sentinel values (replaced with NaN)
- [ ] Works for at least 3 different GIRO stations
- [ ] Handles network errors without crashing
- [ ] Unit tests pass

**Open Questions:**

- What is the exact GIRO DIDBase API format? Research needed to determine URL structure, available parameters, and response format.
- Does GIRO provide h'(f) at arbitrary frequencies, or only standard parameters? If only standard, we may need to retrieve full ionogram trace data.
- Are there rate limits or usage policies for the GIRO API?

---

### R2 — HamSCI Data Loader Module

**Goal:** Standardized loading of HamSCI ionosonde measurements into a consistent internal format.

**Functional Requirements:**

- R2.1: Read the current raw output format of the HamSCI ionosonde system.
- R2.2: Parse timestamps and convert to UTC datetime objects.
- R2.3: Extract virtual height measurements for each sounding frequency.
- R2.4: Return data as a pandas DataFrame with columns including at minimum:
  - `timestamp` (UTC datetime)
  - `frequency_mhz` (sounding frequency)
  - `virtual_height_km` (measured virtual height)
  - `echo_detected` (boolean — was an echo detected at this frequency?)
- R2.5: Handle edge cases: missing data, corrupted records, no-echo soundings.
- R2.6: Support loading data from a date range or a specific data file/directory.

**Non-Functional Requirements:**

- R2.7: Design as a reusable Python module.
- R2.8: Document the expected input data format (file structure, columns, units).
- R2.9: Follow project code style.
- R2.10: Include unit tests with sample data files.

**Acceptance Criteria:**

- [ ] Can load HamSCI data for a specified date range
- [ ] Output DataFrame has consistent column names and types
- [ ] Handles files with missing or corrupted records without crashing
- [ ] Unit tests pass with sample data

**Open Questions:**

- What is the current raw data format? (File type, column layout, directory structure.) The research engineer needs to document this.
- Is there metadata stored with the data (e.g., transmit power, antenna configuration, GPS time sync status)?
- Where is the data stored? Local filesystem, remote server, or both?

---

### R3 — Time-Aligned Comparison Dataset

**Goal:** Produce a paired dataset aligning HamSCI and Digisonde measurements in time for direct comparison.

**Functional Requirements:**

- R3.1: Accept a HamSCI DataFrame (from R2) and a GIRO DataFrame (from R1) as inputs.
- R3.2: Align measurements in time. HamSCI sounds every 5 minutes; GIRO Digisondes typically every 15 minutes. Support at least:
  - Nearest-neighbor matching (pair each GIRO measurement with the closest HamSCI measurement in time)
  - Optional: interpolation of HamSCI data to GIRO timestamps
- R3.3: Allow a configurable maximum time gap for pairing (e.g., reject pairs where timestamps differ by more than 5 minutes).
- R3.4: Output a single DataFrame where each row contains both HamSCI and GIRO measurements for the same time, clearly labeled (e.g., `hamsci_vh_3p5`, `giro_vh_3p5`, `giro_fof2`, etc.).
- R3.5: Include a column indicating the time difference between the paired measurements.
- R3.6: Flag or exclude rows where one side has missing data.

**Non-Functional Requirements:**

- R3.7: Design as a reusable function/module.
- R3.8: Include unit tests.

**Acceptance Criteria:**

- [ ] Produces a paired DataFrame from sample HamSCI and GIRO data
- [ ] Time alignment is correct (verified by inspection)
- [ ] Missing data is handled (NaN or excluded)
- [ ] Unit tests pass

---

### R4 — Statistical Validation of Virtual Heights

**Goal:** Quantitative assessment of how well HamSCI virtual height measurements agree with Digisonde values.

**Functional Requirements:**

- R4.1: Compute the following metrics for each sounding frequency (3.5 MHz, 7.0 MHz):
  - Bias (mean difference: HamSCI minus Digisonde)
  - RMSE (root mean square error)
  - MAE (mean absolute error)
  - Pearson correlation coefficient (r) and p-value
  - Number of valid paired measurements (N)
- R4.2: Generate the following plots:
  - Time series overlay: HamSCI and Digisonde virtual heights on the same axes
  - Scatter plot: HamSCI vs. Digisonde with 1:1 reference line and regression fit
  - Residual plot: difference vs. time, to identify systematic patterns
  - Histogram of residuals
- R4.3: Segment all metrics and plots by:
  - Day vs. night (use solar zenith angle or simple local time threshold)
  - Month or season (if sufficient data)
- R4.4: Identify and tabulate periods of disagreement:
  - HamSCI detects echo but Digisonde does not at comparable frequency
  - Digisonde detects echo but HamSCI does not
  - Large residuals (> 2 sigma from mean)
- R4.5: Output a summary statistics table suitable for inclusion in a report or paper.

**Non-Functional Requirements:**

- R4.6: All plots should be publication-quality (labeled axes with units, legends, titles, reasonable figure size).
- R4.7: Produce plots using Matplotlib; save as both PNG and PDF.
- R4.8: Analysis should be runnable as a script or notebook that regenerates all figures from the paired dataset.

**Acceptance Criteria:**

- [ ] Summary statistics table is produced for both frequencies
- [ ] All plots generate without error and are publication-quality
- [ ] Day/night segmentation is implemented
- [ ] Disagreement periods are identified and tabulated

---

### R5 — Detection Boundary Characterization

**Goal:** Understand when the HamSCI ionosonde can and cannot detect echoes, and how this relates to ionospheric conditions.

**Functional Requirements:**

- R5.1: For each sounding frequency (3.5 MHz, 7.0 MHz), compute:
  - Fraction of time echoes are detected (overall, day, night)
  - Detection rate as a function of GIRO foF2 (e.g., bin by foF2 in 0.5 MHz increments)
- R5.2: Generate the following plots:
  - Detection probability vs. foF2 (for each sounding frequency) — this should show a transition near the sounding frequency
  - Time-of-day heatmap showing detection rate by hour and frequency
  - Timeline showing echo presence/absence overlaid with GIRO foF2
- R5.3: Characterize the foF2 threshold below which echoes are lost for each frequency:
  - Empirical threshold (e.g., 50% detection probability)
  - Compare to the theoretical expectation (echo lost when foF2 < sounding frequency)
  - If discrepancy exists, discuss possible causes (noise floor, antenna pattern, D-region absorption)
- R5.4: Quantify the nighttime data gap: what fraction of nighttime hours have no echoes on each frequency?

**Acceptance Criteria:**

- [ ] Detection rate statistics are computed for both frequencies
- [ ] Detection probability vs. foF2 plots clearly show the transition
- [ ] Empirical detection thresholds are reported and compared to theory
- [ ] Nighttime gap is quantified

---

### R6 — Multi-Station Validation (Stretch)

**Goal:** Assess whether validation results hold across different reference stations and distances.

**Functional Requirements:**

- R6.1: Repeat the validation analysis (R4) using at least two additional GIRO stations at different distances from W2NAF.
- R6.2: Compute validation metrics as a function of distance between HamSCI and the reference Digisonde.
- R6.3: Discuss how ionospheric spatial variability limits the usefulness of distant reference stations.

**Candidate Stations:**

| Station | URSI Code | Distance from W2NAF | Notes |
|---------|-----------|---------------------|-------|
| Alpena, MI | AL945 | ~900 km | Current reference |
| Wallops Island, VA | WP937 | ~350 km | Closer, used in poster |
| Millstone Hill, MA | MHJ45 | ~350 km | MIT Haystack, co-author institution |

**Acceptance Criteria:**

- [ ] Validation metrics computed for at least 2 additional stations
- [ ] Comparison table across stations is produced
- [ ] Discussion of distance effects is written

---

## Deliverables

1. **Python modules:** `giro_data.py`, `hamsci_data.py`, `comparison.py`, `validation.py` (or similar)
2. **Validation report:** Summary statistics, all plots, and interpretation (as a Jupyter notebook or Markdown document)
3. **Unit tests** for all modules
4. **Sample data** in `data/` directory for testing and reproducibility

## Dependencies

- Python 3.8+
- pandas, numpy, scipy, matplotlib
- requests (for GIRO API)
- pytest (for testing)

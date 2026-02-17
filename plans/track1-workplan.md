# Track 1 Validation Work Plan

## Team

| Role | Name | GitHub | Label |
|------|------|--------|-------|
| Research Engineer | Gerard Piccini | `gerardpiccini` | RE |
| Physics Professor | (Prof) | `ras305` | Prof |

## Milestone Conferences

| Conference | Dates | Poster/Slides Due | Working Days |
|------------|-------|-------------------|--------------|
| **HamSCI Workshop 2026** | March 14-15 | ~March 10 | **~15 working days** |
| **Dayton Hamvention** | May 15-17 | ~May 10 | **~60 working days** |
| **NSF CEDAR Workshop** | Week of June 21 | ~June 16 | **~25 more working days** |

All dates measured from February 17, 2026.

---

## Phase 1: HamSCI Workshop 2026 (by March 10)

**Goal:** Updated poster showing quantitative validation results beyond the 2024 eclipse poster. Demonstrate the instrument is producing reliable virtual height measurements by comparison to a professional Digisonde.

This phase builds on the overlay plots the research engineer is already creating and formalizes them with statistical rigor.

### Tasks

#### T1.1 — Document Current Data Format (RE)

**Due: Feb 21 (Fri)**

Document the current HamSCI ionosonde raw data format: file type, column layout, units, directory structure, timestamp format, and any metadata. This is a prerequisite for writing a proper data loader.

**Deliverable:** A short document in `docs/data-format.md` describing the raw data.

**Acceptance criteria:**

- [ ] File format, column names, and units are documented
- [ ] Example data file is placed in `data/` directory
- [ ] Any quirks or known issues are noted

---

#### T1.2 — HamSCI Data Loader Module (RE)

**Due: Feb 25 (Tue)**

Write a Python module (`hamsci_data.py`) that loads raw HamSCI ionosonde data into a pandas DataFrame with standardized columns:

- `timestamp` (UTC datetime)
- `frequency_mhz` (sounding frequency)
- `virtual_height_km` (measured virtual height, NaN if no echo)
- `echo_detected` (boolean)

**Acceptance criteria:**

- [ ] Loads data for a specified date range
- [ ] Handles missing data and no-echo soundings
- [ ] Returns a clean DataFrame with consistent types
- [ ] Basic smoke test included

---

#### T1.3 — GIRO Data Retrieval Module (RE)

**Due: Feb 28 (Fri)**

Write a Python module (`giro_data.py`) that retrieves Digisonde data from the GIRO DIDBase for a given station and date range. Retrieve at minimum: foF2, hmF2, h'F2, and virtual heights at standard frequencies if available. Start with Alpena, MI.

Research the GIRO DIDBase API to determine the correct URL structure, available parameters, and response format.

**Acceptance criteria:**

- [ ] Retrieves foF2 and hmF2 time series for Alpena over a specified date range
- [ ] Returns a clean DataFrame with NaN for missing values (not 9999 sentinels)
- [ ] Caches data locally to avoid redundant API calls
- [ ] Basic smoke test included

---

#### T1.4 — Time-Aligned Comparison Dataset (RE)

**Due: Mar 3 (Tue)**

Write a function that takes a HamSCI DataFrame and a GIRO DataFrame and produces a paired dataset aligned in time. Use nearest-neighbor matching with a configurable maximum time gap.

**Acceptance criteria:**

- [ ] Produces a paired DataFrame with both HamSCI and GIRO values per row
- [ ] Includes time difference column
- [ ] Handles missing data appropriately

---

#### T1.5 — Statistical Validation Analysis (Prof)

**Due: Mar 7 (Fri)**

Using the paired dataset from T1.4, compute quantitative validation metrics and generate publication-quality figures. This is the core scientific contribution for the poster.

**Metrics (for each sounding frequency: 3.5 MHz, 7.0 MHz):**

- Bias (mean difference, HamSCI minus Digisonde)
- RMSE
- Pearson correlation coefficient (r) with p-value
- N (number of valid paired measurements)

**Figures:**

- Time series overlay (HamSCI vs. Digisonde virtual heights)
- Scatter plot with 1:1 line and linear regression fit
- Residual histogram

Segment by day vs. night (use local time cutoff or solar zenith angle).

**Acceptance criteria:**

- [ ] Summary statistics table produced for both frequencies
- [ ] At least 3 publication-quality figures generated
- [ ] Day/night segmentation included
- [ ] Results are interpretable and ready for poster

---

#### T1.6 — Updated Poster (RE + Prof)

**Due: Mar 10 (Mon)**

Update the 2025 poster for the 2026 HamSCI Workshop. Key additions beyond the 2025 poster:

- Quantitative validation metrics (from T1.5)
- Updated figures with statistical analysis
- Description of the ongoing sounding campaign (5-min cadence, 3.5 + 7 MHz)
- Comparison station identified (Alpena, MI)
- Brief mention of future directions (multi-frequency sounding, prop integration)

**Acceptance criteria:**

- [ ] Poster includes quantitative metrics (bias, RMSE, r)
- [ ] At least 2 new figures beyond what was in the 2025 poster
- [ ] Poster reviewed by both team members before submission

---

### Phase 1 Timeline

```
Week of Feb 17:  T1.1 (RE) .............. Document data format
                 T1.2 (RE) .............. HamSCI data loader
Week of Feb 24:  T1.3 (RE) .............. GIRO retrieval module
                 T1.4 (RE) .............. Time-aligned comparison
                 T1.5 (Prof) ............ Begin statistical analysis
Week of Mar 2:   T1.5 (Prof) ............ Complete statistical analysis
                 T1.6 (RE + Prof) ....... Draft poster
Week of Mar 9:   T1.6 (RE + Prof) ....... Finalize poster
                 ---- Mar 14-15: HamSCI Workshop ----
```

---

## Phase 2: Dayton Hamvention (by May 10)

**Goal:** Comprehensive validation study with detection boundary analysis, extended dataset, and initial multi-station comparison. Begin exploring multi-frequency sounding (Track 2 overlap). Poster or presentation for Hamvention audience (more operator-focused than HamSCI Workshop).

### Tasks

#### T2.1 — Extend Validation Dataset (RE)

**Due: Mar 28**

Accumulate and process a longer validation dataset — at least 2-3 months of continuous HamSCI data compared against GIRO. Rerun the validation analysis from T1.5 on the extended dataset.

**Acceptance criteria:**

- [ ] At least 2 months of paired HamSCI/GIRO data processed
- [ ] Validation metrics updated with larger dataset
- [ ] Any data gaps documented

---

#### T2.2 — Detection Boundary Analysis (Prof)

**Due: Apr 10**

Characterize when the ionosonde can and cannot detect echoes, and relate this to ionospheric conditions. This is a scientifically interesting result on its own.

**Analysis:**

- Detection probability vs. GIRO foF2 for each sounding frequency (3.5, 7.0 MHz)
- Empirical detection threshold (foF2 at which detection probability = 50%)
- Comparison to theoretical expectation (echo lost when foF2 < sounding frequency)
- If discrepancy exists, discuss possible causes (D-region absorption, noise floor, antenna pattern)
- Time-of-day heatmap showing detection rate by hour
- Quantify nighttime data gap

**Acceptance criteria:**

- [ ] Detection probability vs. foF2 curves produced
- [ ] Empirical thresholds reported and compared to theory
- [ ] Nighttime gap quantified
- [ ] Written interpretation (1 page)

---

#### T2.3 — Residual Pattern Analysis (Prof)

**Due: Apr 17**

Investigate systematic patterns in the validation residuals (HamSCI minus Digisonde).

- Do residuals correlate with time of day, season, geomagnetic activity (Kp)?
- Are there systematic biases (e.g., HamSCI consistently reading higher or lower)?
- Are there outlier events? If so, what was happening ionospherically?
- Is there a dependence on virtual height itself (e.g., larger errors at higher virtual heights)?

**Acceptance criteria:**

- [ ] Residual vs. time-of-day plot
- [ ] Residual vs. virtual height plot
- [ ] Assessment of whether systematic biases exist
- [ ] Outlier events identified and discussed

---

#### T2.4 — Multi-Station Comparison: Wallops Island (RE)

**Due: Apr 24**

Add Wallops Island, VA as a second validation reference (this was the reference used in the 2025 poster, so it provides continuity). Compute the same validation metrics as T1.5.

Compare results across Alpena and Wallops:

- Does agreement differ between stations?
- Is distance a factor? (Wallops is ~350 km from W2NAF; Alpena is ~900 km)

**Acceptance criteria:**

- [ ] Wallops Island GIRO data retrieved and processed
- [ ] Validation metrics computed for Wallops
- [ ] Comparison table: Alpena vs. Wallops metrics side by side

---

#### T2.5 — Add pytest Infrastructure (RE)

**Due: Apr 30**

Add formal pytest tests for the data modules created in Phase 1. Include sample data files in `data/test/` for reproducible testing.

**Test coverage:**

- `hamsci_data.py`: Load sample file, verify column types and values
- `giro_data.py`: Test with cached/mock GIRO response, verify parsing
- `comparison.py`: Test time alignment with known inputs
- Validation functions: Test metric calculations with known values

**Acceptance criteria:**

- [ ] `pytest` runs cleanly from the repo root
- [ ] At least one test per module
- [ ] Sample test data committed to `data/test/`
- [ ] Tests documented in README

---

#### T2.6 — Hamvention Poster/Presentation (RE + Prof)

**Due: May 10**

Prepare an updated poster or presentation for Dayton Hamvention. The Hamvention audience includes many amateur radio operators, so emphasis should be on:

- What this system does and why it matters for ham radio
- Validation results showing the system works
- Detection boundary results (when can you hear your signal bounce off the ionosphere?)
- Future directions: multi-frequency sounding, prop.kc2g.com integration

**Acceptance criteria:**

- [ ] Includes extended validation results (larger dataset than HamSCI Workshop)
- [ ] Includes detection boundary analysis
- [ ] Includes multi-station comparison (Alpena + Wallops)
- [ ] Accessible to amateur radio operator audience

---

### Phase 2 Timeline

```
Week of Mar 17:  T2.1 (RE) ... Begin extending validation dataset
Week of Mar 24:  T2.1 (RE) ... Continue data accumulation
Week of Mar 31:  T2.2 (Prof) . Begin detection boundary analysis
Week of Apr 6:   T2.2 (Prof) . Complete detection boundary analysis
Week of Apr 13:  T2.3 (Prof) . Residual pattern analysis
Week of Apr 20:  T2.4 (RE) ... Multi-station comparison (Wallops)
Week of Apr 27:  T2.5 (RE) ... pytest infrastructure
Week of May 4:   T2.6 (RE + Prof) ... Hamvention poster
                 ---- May 15-17: Dayton Hamvention ----
```

---

## Phase 3: NSF CEDAR Workshop (by June 16)

**Goal:** Publication-quality validation study suitable for an atmospheric science audience. CEDAR attendees are ionospheric scientists — this is the most technically demanding audience. The validation should be comprehensive enough to support a journal paper submission.

### Tasks

#### T3.1 — Multi-Station Validation: Millstone Hill (RE)

**Due: May 29**

Add Millstone Hill, MA (MIT Haystack Observatory) as a third validation reference. This is particularly relevant since Haystack is a co-author institution on the original poster.

Compute the same validation metrics and add to the multi-station comparison.

**Acceptance criteria:**

- [ ] Millstone Hill GIRO data retrieved and processed
- [ ] Validation metrics computed
- [ ] Three-station comparison table complete

---

#### T3.2 — Geophysical Context Analysis (Prof)

**Due: Jun 5**

Analyze how validation results vary with geophysical conditions. This is the kind of analysis CEDAR reviewers will expect.

- Segment validation metrics by:
  - Solar zenith angle (continuous, not just day/night binary)
  - Season (if sufficient data span)
  - Geomagnetic activity (Kp index — retrieve from NOAA or GFZ)
  - Solar flux (F10.7 index)
- Investigate whether there are ionospheric conditions under which the HamSCI system performs notably better or worse
- Discuss physical reasons for any dependencies found

**Acceptance criteria:**

- [ ] Validation metrics segmented by solar zenith angle
- [ ] Kp-dependent analysis included
- [ ] Physical interpretation provided
- [ ] Figures suitable for CEDAR presentation

---

#### T3.3 — Comprehensive Validation Report (Prof)

**Due: Jun 10**

Write up the complete validation study as a technical report or draft paper section. This should include:

- Description of the HamSCI ionosonde system and sounding parameters
- Description of the validation methodology
- All statistical results (full dataset, day/night, multi-station, geophysical dependence)
- Detection boundary characterization
- Discussion of systematic errors and their possible sources
- Comparison to the 2024 eclipse results from the original poster
- Conclusions on instrument reliability and measurement uncertainty

**Acceptance criteria:**

- [ ] Complete written report with all figures and tables
- [ ] Suitable for inclusion in a journal paper or conference proceedings
- [ ] Reviewed by both team members

---

#### T3.4 — CEDAR Poster/Presentation (RE + Prof)

**Due: Jun 16**

Prepare a poster or presentation for the NSF CEDAR Workshop. Emphasis for this audience:

- Rigorous validation methodology
- Multi-station comparison and distance dependence
- Geophysical context (SZA, Kp, F10.7 dependence)
- Measurement uncertainty characterization
- Scientific utility of a low-cost ionosonde network
- Connection to citizen science and distributed sensing

**Acceptance criteria:**

- [ ] Includes full multi-station validation
- [ ] Includes geophysical context analysis
- [ ] Technical depth appropriate for ionospheric science audience
- [ ] Clearly states measurement uncertainty bounds

---

### Phase 3 Timeline

```
Week of May 19:  T3.1 (RE) ... Multi-station: Millstone Hill
Week of May 25:  T3.1 (RE) ... Complete Millstone Hill analysis
Week of Jun 1:   T3.2 (Prof) . Geophysical context analysis
Week of Jun 8:   T3.3 (Prof) . Comprehensive validation report
                 T3.4 (RE + Prof) ... Begin CEDAR poster
Week of Jun 15:  T3.4 (RE + Prof) ... Finalize CEDAR poster
                 ---- Week of Jun 21: NSF CEDAR Workshop ----
```

---

## Full Timeline Summary

```
Feb 17 ─────────────────── PROJECT START ───────────────────
  │
  │  T1.1 (RE)  Document data format ............... Feb 21
  │  T1.2 (RE)  HamSCI data loader ................. Feb 25
  │  T1.3 (RE)  GIRO retrieval module .............. Feb 28
  │  T1.4 (RE)  Time-aligned comparison ............ Mar 3
  │  T1.5 (Prof) Statistical validation ............ Mar 7
  │  T1.6 (RE+Prof) HamSCI Workshop poster ......... Mar 10
  │
Mar 14-15 ──────── HAMSCI WORKSHOP 2026 ────────────────────
  │
  │  T2.1 (RE)  Extend validation dataset .......... Mar 28
  │  T2.2 (Prof) Detection boundary analysis ....... Apr 10
  │  T2.3 (Prof) Residual pattern analysis ......... Apr 17
  │  T2.4 (RE)  Multi-station: Wallops Island ...... Apr 24
  │  T2.5 (RE)  pytest infrastructure .............. Apr 30
  │  T2.6 (RE+Prof) Hamvention poster .............. May 10
  │
May 15-17 ──────── DAYTON HAMVENTION ───────────────────────
  │
  │  T3.1 (RE)  Multi-station: Millstone Hill ...... May 29
  │  T3.2 (Prof) Geophysical context analysis ...... Jun 5
  │  T3.3 (Prof) Comprehensive validation report ... Jun 10
  │  T3.4 (RE+Prof) CEDAR poster ................... Jun 16
  │
Week of Jun 21 ──── NSF CEDAR WORKSHOP ─────────────────────
```

## Task Assignment Summary

### Research Engineer (`gerardpiccini`)

| Task | Description | Due |
|------|-------------|-----|
| T1.1 | Document current data format | Feb 21 |
| T1.2 | HamSCI data loader module | Feb 25 |
| T1.3 | GIRO data retrieval module | Feb 28 |
| T1.4 | Time-aligned comparison dataset | Mar 3 |
| T1.6 | HamSCI Workshop poster (with Prof) | Mar 10 |
| T2.1 | Extend validation dataset | Mar 28 |
| T2.4 | Multi-station: Wallops Island | Apr 24 |
| T2.5 | pytest infrastructure | Apr 30 |
| T2.6 | Hamvention poster (with Prof) | May 10 |
| T3.1 | Multi-station: Millstone Hill | May 29 |
| T3.4 | CEDAR poster (with Prof) | Jun 16 |

### Physics Professor (`ras305`)

| Task | Description | Due |
|------|-------------|-----|
| T1.5 | Statistical validation analysis | Mar 7 |
| T1.6 | HamSCI Workshop poster (with RE) | Mar 10 |
| T2.2 | Detection boundary analysis | Apr 10 |
| T2.3 | Residual pattern analysis | Apr 17 |
| T2.6 | Hamvention poster (with RE) | May 10 |
| T3.2 | Geophysical context analysis | Jun 5 |
| T3.3 | Comprehensive validation report | Jun 10 |
| T3.4 | CEDAR poster (with RE) | Jun 16 |

## Dependencies

```
T1.1 → T1.2 → T1.4 → T1.5 → T1.6
T1.1 → T1.3 ↗        ↗
                T2.1 → T2.2 → T2.6
                       T2.3 ↗
                T2.4 ↗
                T2.5 (independent)
                       T3.1 → T3.2 → T3.3 → T3.4
```

- T1.5 (Prof) cannot start until T1.4 (RE) delivers the paired dataset
- T2.2 and T2.3 (Prof) depend on the extended dataset from T2.1 (RE)
- T2.4 (RE) depends on T1.3 (GIRO module) being generalizable to other stations
- Poster tasks are joint and depend on all preceding analysis tasks

# Track 2: Sounding Mode Design for prop.kc2g.com Integration

## Overview

prop.kc2g.com is an open-source ionospheric propagation prediction system that assimilates real ionosonde measurements into global ionospheric maps. It is the most widely used real-time HF propagation tool in the amateur radio community. Getting HamSCI ionosonde data into prop would be a significant contribution.

However, prop requires derived ionospheric parameters (**foF2, hmF2, mufd**) — not raw virtual heights at fixed frequencies. The current HamSCI sounding mode (3.5 and 7 MHz only) does not provide enough information to reliably derive these parameters.

This track focuses on designing an optimized sounding schedule that directly measures what prop needs, while minimizing total transmission time. The HamSCI system has the flexibility to sound additional frequencies within its 2-10 MHz license and potentially run sweep modes.

### Objectives

1. Understand what ionospheric parameters prop.kc2g.com requires and how they are derived from ionograms
2. Design candidate sounding schedules that can determine foF2 and hmF2
3. Evaluate candidates through simulation against existing Digisonde data (paper study)
4. Implement the chosen mode and validate it
5. Build a data pipeline from HamSCI measurements to prop-compatible output

### Constraints

- **Frequency range:** 2-10 MHz (FCC experimental license)
- **Power:** Up to 300 watts (not a concern for optimization right now)
- **Minimize transmission time:** Sound as few frequencies and for as short a duration as practical
- **5-minute cycle:** Current sounding cadence; new mode should fit within this or a similar cadence
- **Hardware:** Ettus N200 USRP (current) or Red Pitaya SDRlab 122-16 (in development); both controlled via GNU Radio

---

## Background: What prop.kc2g.com Needs

### Required Parameters (minimum viable measurement)

| Parameter | Description | Units | How Digisondes Measure It |
|-----------|-------------|-------|---------------------------|
| **foF2** | F2 layer critical frequency | MHz | Highest frequency at which a vertical echo returns from the F2 layer |
| **hmF2** | F2 layer peak height | km | Derived from the virtual height trace near foF2 via true-height inversion |
| **mufd** | MUF(3000)F2 factor | MHz | Can be derived from foF2 and hmF2 using the secant law |

Additionally, prop uses when available:

- **foE** — E layer critical frequency
- **foF1** — F1 layer critical frequency
- **h'F2** — Minimum virtual height of F2 layer
- **Confidence score** (0-100)

### How prop Ingests Data

prop currently ingests data via **SAO4 files** downloaded from three sources:

1. **GIRO** (UMass Lowell) — via FTP from `ftp://giro.uml.edu`
2. **NOAA** — ZIP files containing .SAO files
3. **Australian SWS** — ZIP files from `downloads.sws.bom.gov.au`

The SAO4 files are parsed by a Perl module (`loader/lib/Data/SAO4.pm`) and loaded into a PostgreSQL database. The assimilation engine then combines these measurements with IRI2016 model predictions using Gaussian Process regression to produce global ionospheric maps.

**Source code:** https://github.com/arodland/prop

**Key files in the prop repository:**

- `loader/lib/Data/SAO4.pm` — SAO4 file parser
- `loader/giro-loader/load.pl` — Measurement loader (extracts 21 parameters from SAO4)
- `assimilate/assimilate.py` — GP assimilation engine
- `pred/pred.py` — Station-level prediction from IRI baseline
- `essn/essn.py` — Back-derives space weather indices from measurements

### The Core Physics Problem

foF2 is the frequency at which the ionosphere becomes transparent — the plasma frequency at the F2 peak. At frequencies below foF2, the signal is refracted back to Earth. At frequencies above foF2, it passes through.

A traditional ionosonde sweeps from ~1-20 MHz and plots virtual height vs. frequency (an ionogram). foF2 is where the F2 trace goes to infinity (the "cusp") — meaning the signal barely reflects and takes a very long path. hmF2 is derived from the shape of the trace near this cusp using inversion algorithms.

**Key insight:** To determine foF2, we don't necessarily need a full ionogram sweep. We need to find the frequency boundary where echoes stop returning from the F2 layer. A few well-chosen frequency points can bracket this.

---

## Requirements

### R1 — Literature Review: foF2/hmF2 Determination Methods

**Goal:** Understand how foF2 and hmF2 are extracted from ionograms, and what minimum observations are needed.

**Requirements:**

- R1.1: Review how the Digisonde ARTIST autoscaling software determines foF2 from an ionogram.
- R1.2: Review how hmF2 is derived from the virtual height trace near foF2 (true-height inversion methods: POLAN, profile fitting).
- R1.3: Investigate whether simpler hmF2 estimation methods exist that don't require a full ionogram:
  - Empirical formulas relating h'F2 (minimum virtual height) to hmF2
  - Parabolic or Chapman layer approximations
  - IRI-constrained estimation (use IRI as prior, adjust with measurements)
- R1.4: Review literature on "sparse ionograms" or ionosonde systems that derive foF2 from a limited number of frequency points.
- R1.5: Investigate whether the virtual height behavior just below foF2 (heights increasing rapidly as frequency approaches foF2) can be exploited with a small number of frequencies.

**Deliverable:** Written summary (1-3 pages) of viable approaches with pros, cons, and references. Include assessment of how many frequency points are needed for each approach.

**Acceptance Criteria:**

- [ ] At least 3 methods for foF2 determination are described
- [ ] At least 2 methods for hmF2 estimation are described
- [ ] Minimum frequency count requirements are discussed for each method
- [ ] References to published work are included

---

### R2 — Design Candidate Sounding Schedules

**Goal:** Propose several concrete sounding schedules that could determine foF2 and hmF2 within the system's constraints.

**Requirements:**

- R2.1: Design at least 3 candidate sounding schedules from the following categories:

**Candidate A — Discrete Multi-Frequency Mode:**

- Sound at N fixed frequencies spanning the 2-10 MHz license range
- Suggested starting set: 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0 MHz (9 frequencies)
- foF2 is bracketed between the highest frequency that returns an echo and the lowest that does not
- hmF2 is estimated from the virtual height trend of the frequencies that return echoes
- **Pros:** Simple to implement, robust
- **Cons:** foF2 resolution limited to spacing between frequencies; more frequencies = more transmission time
- Evaluate: What frequency spacing gives acceptable foF2 accuracy for prop? (prop's GP assimilation can tolerate some measurement uncertainty)

**Candidate B — Adaptive Binary Search Mode:**

- Start at a middle frequency (e.g., 6 MHz)
- If echo detected: try higher; if no echo: try lower
- Converge on foF2 in ~log2(range/resolution) steps
- For 2-10 MHz range with 0.5 MHz resolution: ~4 steps
- **Pros:** Fewest transmissions; efficient
- **Cons:** More complex to implement; sequential (cannot parallelize); may be confused by sporadic E or multiple layers
- Evaluate: How robust is this to multi-layer ionosphere (E and F2 both reflecting)?

**Candidate C — Narrow Sweep Near Expected foF2:**

- Use IRI model prediction or recent measurements to estimate expected foF2
- Sweep a narrow band (e.g., +/- 2 MHz around expected foF2) using a chirp
- Directly images the ionogram cusp in a limited frequency range
- Sound a few monitoring frequencies outside the sweep for robustness
- **Pros:** Most accurate; directly measures the cusp shape needed for hmF2
- **Cons:** Requires IRI or recent data as prior; may miss foF2 if prior is wrong; sweep implementation may be more complex in GNU Radio

**Candidate D — Hybrid Fixed + Adaptive:**

- Always sound at fixed monitoring frequencies (e.g., 3.5 and 7 MHz) for continuity with existing data
- Additionally, run an adaptive or multi-frequency component to bracket foF2
- **Pros:** Maintains backward compatibility; provides both validation data and foF2
- **Cons:** More total transmission time than pure adaptive

- R2.2: For each candidate, estimate:
  - Number of transmissions per sounding cycle
  - Total on-air time per cycle (accounting for chirp duration, guard intervals, etc.)
  - Expected foF2 accuracy (MHz)
  - Expected hmF2 accuracy (km)
  - Implementation complexity (GNU Radio changes needed)
  - Robustness to edge cases (sporadic E, spread F, nighttime loss of F2)

- R2.3: Consider what happens when foF2 drops below 2 MHz (below license range) — this will happen at night. The system should detect this condition (no echoes at any frequency) and report it correctly rather than producing bad data.

- R2.4: Consider what happens with multiple layers (E and F2 both reflecting at the same frequency). Digisondes distinguish these by virtual height; our system may need to handle multiple echoes at the same frequency.

**Deliverable:** Written comparison document with a table summarizing the trade-offs across candidates.

**Acceptance Criteria:**

- [ ] At least 3 candidate sounding schedules are described in detail
- [ ] Transmission time and accuracy estimates are provided for each
- [ ] Edge cases (nighttime, sporadic E, multiple layers) are addressed
- [ ] A recommendation is made with rationale

---

### R3 — Simulate Sounding Schedules Against GIRO Data

**Goal:** Use existing Digisonde ionogram data to simulate what each sounding schedule would measure, and evaluate accuracy of derived foF2/hmF2.

This is a paper study — no hardware changes needed.

**Functional Requirements:**

- R3.1: Obtain GIRO Digisonde data for Alpena, MI (or another station with available trace data) including:
  - foF2 and hmF2 truth values
  - Virtual heights at multiple frequencies across the 2-10 MHz range (from ionogram trace data if available, or from the standard GIRO parameters)
- R3.2: For each candidate sounding schedule:
  - Extract the virtual heights at the candidate's sounding frequencies from the GIRO data
  - Apply the foF2/hmF2 extraction algorithm for that sounding mode
  - Compare derived foF2 against GIRO truth foF2
  - Compare derived hmF2 against GIRO truth hmF2
- R3.3: Compute validation metrics (bias, RMSE, correlation) for each candidate.
- R3.4: Plot the accuracy vs. number of frequencies sounded (the efficiency frontier).
- R3.5: Evaluate robustness: what fraction of soundings produce a valid foF2 estimate for each candidate?
- R3.6: Test sensitivity to noise: add realistic virtual height measurement noise (based on Track 1 validation results) and evaluate impact on foF2/hmF2 accuracy.

**Non-Functional Requirements:**

- R3.7: Analysis should be in a Jupyter notebook or script that can be rerun.
- R3.8: All plots publication-quality.

**Acceptance Criteria:**

- [ ] At least 3 sounding schedules simulated over at least 1 month of GIRO data
- [ ] Accuracy metrics (bias, RMSE, r) computed for foF2 and hmF2 for each schedule
- [ ] Efficiency frontier plot produced
- [ ] Robustness analysis completed
- [ ] Clear recommendation for preferred sounding schedule

**Open Questions:**

- Does GIRO provide virtual height at arbitrary frequencies, or only the standard scaled parameters? If only standard parameters, can we use the ionogram trace data directly? This determines the fidelity of the simulation.
- What is the realistic virtual height measurement noise for the HamSCI system? This comes from Track 1 validation and should feed into the noise sensitivity analysis.

---

### R4 — Implement Chosen Sounding Mode

**Goal:** Implement the selected sounding schedule on the HamSCI ionosonde hardware and validate it.

**Requirements:**

- R4.1: Work with the hardware/GNU Radio team to implement the selected sounding mode.
- R4.2: Maintain the existing 3.5/7 MHz fixed-frequency mode as a fallback or as part of a hybrid mode.
- R4.3: Implement the foF2/hmF2 extraction algorithm in Python:
  - Input: set of (frequency, virtual_height, echo_detected) tuples from one sounding cycle
  - Output: estimated foF2 (MHz), hmF2 (km), confidence score, and any flags
- R4.4: Validate the derived foF2/hmF2 against GIRO data using the Track 1 validation infrastructure:
  - Same metrics: bias, RMSE, correlation
  - Compare against the simulation predictions from R3 (did reality match the paper study?)
- R4.5: Run for at least 1 week in parallel with the existing mode to ensure stability.

**Acceptance Criteria:**

- [ ] New sounding mode runs stably for at least 1 week
- [ ] foF2 extraction algorithm produces reasonable values
- [ ] Validation against GIRO shows agreement consistent with simulation predictions
- [ ] Existing 3.5/7 MHz measurements are not disrupted

**Dependencies:** Track 1 validation infrastructure (Tasks 1.1-1.4); this task depends on having the paired comparison framework already working.

---

### R5 — Generate prop-Compatible Output

**Goal:** Produce HamSCI measurements in a format that prop.kc2g.com can ingest.

**Requirements:**

- R5.1: Coordinate with KC2G (prop maintainer) to determine the preferred integration method. Options:
  - **Option A — SAO4 file generation:** Write minimal SAO4 files containing foF2, hmF2, mufd, station metadata. prop already has SAO4 parsers and could pull these via FTP or filesystem.
  - **Option B — Direct database insertion:** Write a script that inserts measurements directly into prop's PostgreSQL database (schema: station_id, time, cs, fof2, hmf2, mufd, source).
  - **Option C — New API endpoint:** Propose a new REST endpoint on prop that accepts JSON measurement submissions.
  - **Option D — GIRO submission:** Submit HamSCI data to GIRO, which prop already ingests. This would be the most impactful long-term path but requires meeting GIRO quality standards.
- R5.2: Implement the chosen integration method.
- R5.3: Include station metadata:
  - Station code (to be assigned, e.g., `W2NAF` or a URSI-style code)
  - Latitude and longitude of the W2NAF site
  - Station name
- R5.4: Compute mufd from foF2 and hmF2 if not directly measured. Use the standard secant law: `M(3000)F2 = MUF(3000)F2 / foF2`, where `MUF(3000)F2` can be approximated from `hmF2` using the Shimazaki formula or similar.
- R5.5: Assign a confidence score (0-100) to each measurement based on:
  - Number of frequencies that returned echoes
  - Signal-to-noise ratio
  - Consistency of the virtual height profile
  - Whether foF2 was bracketed (both echo and no-echo frequencies observed) vs. extrapolated

**Acceptance Criteria:**

- [ ] Integration method agreed with KC2G
- [ ] Output module produces correctly formatted data
- [ ] Confidence scores are reasonable (validated against GIRO truth)
- [ ] mufd derivation is correct

---

### R6 — End-to-End Pipeline Test

**Goal:** Prove the full pipeline from HamSCI measurement to prop assimilation.

**Requirements:**

- R6.1: Stand up a local test instance of prop using Docker (the repo provides `docker-compose.yml`).
- R6.2: Feed HamSCI-derived measurements into the test instance via the chosen integration method (R5).
- R6.3: Verify the data appears correctly in prop's PostgreSQL database.
- R6.4: Run the prop assimilation pipeline and verify the HamSCI station appears in the output:
  - Station shows up in `stations.json` API endpoint
  - Station measurements influence the assimilated foF2/hmF2 maps
  - Station appears in the web interface
- R6.5: Document the end-to-end data flow with a block diagram.

**Acceptance Criteria:**

- [ ] Local prop instance runs successfully
- [ ] HamSCI measurements are visible in prop's database
- [ ] Assimilated maps reflect the HamSCI data
- [ ] Data flow is documented

**Dependencies:** R4 (working sounding mode), R5 (prop-compatible output).

---

## Suggested Priority and Sequencing

```
R1 (Literature Review)          ← Can start immediately, no code needed
  ↓
R2 (Design Sounding Schedules)  ← Informed by R1
  ↓
R3 (Simulate Against GIRO)      ← Depends on R2 and Track 1 GIRO retrieval (T1-R1)
  ↓
R4 (Implement on Hardware)      ← Depends on R3 recommendation + Track 1 validation infra
  ↓
R5 (prop-Compatible Output)     ← Can start once R4 is producing data; coordinate with KC2G early
  ↓
R6 (End-to-End Test)            ← Depends on R4 + R5
```

R1 and R2 are primarily research/design tasks and can begin in parallel with Track 1 implementation. R3 depends on Track 1's GIRO data retrieval module. R4-R6 depend on having a validated instrument (Track 1) and a chosen sounding mode (R3).

---

## Key References

- **prop source code:** https://github.com/arodland/prop
- **SAO4 format spec:** https://ulcar.uml.edu/~iag/SAO-4.htm
- **GIRO DIDBase:** https://giro.uml.edu/didbase/
- **IRI2016 model:** https://irimodel.org/
- **Digisonde ARTIST autoscaling:** Reinisch, B.W. and Huang, X. (2005). "Automatic calculation of electron density profiles from digital ionograms." Radio Science, 40.
- **True height inversion (POLAN):** Titheridge, J.E. (1985). "Ionogram analysis with the generalised program POLAN." Report UAG-93, World Data Center A.
- **Shimazaki formula for M(3000)F2:** Shimazaki, T. (1955). "World-wide daily variations in the height of the maximum electron density of the ionospheric F2 layer." J. Radio Res. Labs., 2, 85-97.

## Deliverables

1. **Literature review document** (R1 deliverable)
2. **Sounding schedule comparison document** (R2 deliverable)
3. **Simulation analysis notebook** with figures and recommendation (R3 deliverable)
4. **Python modules:** `fof2_extraction.py`, `prop_output.py` (or similar)
5. **Integration documentation** with block diagram of full data pipeline
6. **Unit tests** for all modules

## Dependencies

- Track 1 validation infrastructure (GIRO retrieval, comparison framework)
- Track 1 validation results (measurement noise characterization)
- GNU Radio / hardware team (for R4 implementation)
- Coordination with KC2G / prop maintainer (for R5 integration method)
- Python 3.8+, pandas, numpy, scipy, matplotlib

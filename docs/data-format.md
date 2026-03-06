# Raw Data Format (raw_data/)
- Raw data is recorded in a binary IQ file
- Data in raw_data/ is stored in zip files by day
- The rest of the data is stored on pi in directories by day (year/month/day/)
- The recording will contain the chirp along the direct path and the echo
- The file are named after the time the data was recorded and the sounding frequency in Hz.  The date string is formatted as "%Y_%m_%d_%H_%M_%S_".
Example: "2026_02_17_00_03_16_7025000"
- Data is stored on pi in directories by day (year/month/day/)
- Sample rate is 195312
- dtype float32
- Files are currently 125KB each.

# Virtual height (Scranton_data/)
- This is data is CSV files containing:
    - utc_time of the chirp,
    - tx frequency in Hz
    - virtual heights in km
    - if an echo was detected
- Stored in files by day

# GIRO (GIRO_data/)
- Digisonde data is provided by the Lowell GIRO Data Center (LGDC) at https://giro.uml.edu/.
- Local CSV files contain:
    - station id (Alepena: AL945, Millstone Hill: MHJ45)
    - time stamp 
    - cs - Autoscaling Confidence Score 
    - fof2 - F2 layer critical frequency
    - MUFD - Maximum usable frequency for ground distance D
    - foE - E layer critical frequency
    - hmF2 - Peak height F2-layer
    - hF2 - Minimum virtual height of F2 trace
    - Distance D for MUF calculations: 30000 km
- Stored in files by day

# Known issues 
- The GNU radio code generates blank files. These are named "no_name" and are to be discarded.




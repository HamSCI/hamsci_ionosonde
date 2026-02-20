# Raw Data Format
- Raw data is recorded in a binary IQ file
- The recording will contain the chirp along the direct path and the echo
- The file are named after the time the data was recorded and the sounding frequency in Hz.  The date string is formatted as "%Y_%m_%d_%H_%M_%S_".
Example: "2026_02_17_00_03_16_7025000"
- Data is stored in directories by day (year/month/day/)
- Sample rate is 195312
- dtype float32
- Files are currently 125KB each.


# Known issues 
- The GNU radio code generates blank files. These are named "no_name" and are to be discarded.




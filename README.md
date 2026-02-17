# HamSCI Ionosonde

Software for processing, analyzing, and validating data from the HamSCI low-cost chirp ionosonde system.

## About

This project supports the development of a **low-cost, low-power chirp ionosonde** for studying ionospheric impacts, as described in [Piccini et al. (2025)](docs/Piccini%20HamSCI%202025%20Poster.pdf). The system uses software-defined radio (SDR) technology to sound the ionosphere at a fraction of the cost of traditional ionosonde systems.

### How It Works

1. A chirp signal is generated and transmitted (2-10 MHz) using an SDR (Ettus N200 USRP or Red Pitaya SDRlab 122-16) controlled by GNU Radio.
2. The ionospheric echo is received on a separate antenna.
3. The transmitted chirp and received signal are cross-correlated in Python to determine the time delay between the direct path and the return echo.
4. The virtual layer height of the ionosphere is calculated from this time delay using the known speed of light.

During the **2024 total solar eclipse**, this system successfully detected the rising and falling of the ionosphere, producing results that closely matched data from the professional Wallops Island ionosonde -- demonstrating that a system costing less than a few thousand dollars can perform comparably to multimillion-dollar instruments.

### Hardware

- **SDR:** Ettus N200 USRP (current), Red Pitaya SDRlab 122-16 (in development)
- **Antennas:** Two multiband fan dipoles (TX and RX)
- **License:** FCC experimental license for 2-10 MHz at up to 300 watts

## Project Structure

```
hamsci_ionosonde/
├── data/               # Ionosonde data files
├── docs/               # Project documentation and references
├── CONTRIBUTING.md     # Contribution guidelines
├── LICENSE             # GPLv3
└── README.md           # This file
```

## Getting Started

### Prerequisites

- Python 3.8+
- GNU Radio (for SDR control)
- NumPy, SciPy, Matplotlib (for data processing)

### Installation

```bash
git clone git@github.com:HamSCI/hamsci_ionosonde.git
cd hamsci_ionosonde
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt  # when available
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

## Project Management

Development is tracked on the [HamSCI Ionosonde GitHub Project Board](https://github.com/orgs/HamSCI/projects/11).

## References

- Piccini, G. N., McGwier, R. W., Spalletta, R. A., Frissell, N. A., Mokhtari, M., & Erickson, P. J. (2025). *A Low-Cost Low-Power Chirp Ionosonde for Studying Eclipse Ionospheric Impacts.* HamSCI Workshop 2025.
- Lloyd, W. C. (2019). *Ionospheric Sounding During a Total Solar Eclipse.* Master's Thesis, Virginia Tech.
- McGwier, R. (2018). *Using GNU Radio and Red Pitaya for Citizen Science.* GNU Radio Conference 2018.

## Acknowledgements

This work is supported by NSF Grants AGS-2230345, AGS-2045755, AGS-2002278, NASA Grant 80NSSC23K1322, and NASA Pennsylvania Space Grant Consortium Grant 80NSSC20M0097/S003135-NASA.

Digisonde data is provided by the [Lowell GIRO Data Center (LGDC)](https://giro.uml.edu/).

## License

This project is licensed under the GNU General Public License v3.0 -- see [LICENSE](LICENSE) for details.

## Contact

- Gerard Piccini -- gerard.piccini@scranton.edu
- Dr. Nathaniel Frissell, W2NAF -- nathaniel.frissell@scranton.edu
- University of Scranton / MIT Haystack Observatory

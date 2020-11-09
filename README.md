# SPRISS
SamPling Reads algorIthm to eStimate frequent k-merS

### Data Preparation
See "data_preparation.txt".

### Installation
In SPRISS's folder, run "make" to compile SPRISS. Since SPRISS is built on KMC, see [KMC's page](https://github.com/refresh-bio/KMC) for details on requirements and installation.
In SAKEIMA's folder, run:
```
autoreconf -i
./configure
make -j 4
```
to compile SAKEIMA. See [SAKEIMA's page](https://github.com/VandinLab/SAKEIMA) for details on requirements and installation. 

### Reproducing Experimental Evaluations
Run:
```
python3 SPRISS/scripts/run_exact_results.py
python3 SPRISS/scripts/run_SPRISS_results.py
python3 SAKEIMA/scripts/run_SAKEIMA_results.py
python3 SPRISS/scripts/plot_figures.py
python3 SAKEIMA/scripts/run_GOS_results.py
python3 SAKEIMA/scripts/plot_GOS_figures.py
```

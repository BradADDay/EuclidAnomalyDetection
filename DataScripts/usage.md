# Usage of `get_data.sh`

In this directory there are two files: `get_data.sh` and `slurm_get_data.sh`. These are two bash scripts written to download data from the Euclid archive. The second script is simply a slurm batch script for getting data on BluePebble. 

`get_data.sh` takes a single argument and can be run as
```
Usage: get_data.sh [-f FILENAME]

    Options:
	-f, --filename: The input file containing a list of datafiles to download
```

The filename points to a text file with each row containing the name of a datafile to be downloaded, for example:
```
EUC_PHZ_PHZCAT__20241120T155047.708542Z_00.00.fits
EUC_PHZ_GALAXYSED__20241120T155146.342023Z_00.00.fits
EUC_PHZ_STARSED__20241120T155127.924796Z_00.00.fits
EUC_PHZ_PHZCAT__20241120T195218.219274Z_00.00.fits
```

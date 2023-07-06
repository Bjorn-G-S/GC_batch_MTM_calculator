# GC_batch_MTM_calculator
* [General](#general-info)
* [Purpose](#purpose)
* [Installation](#Installation)
* [How-to](#how-to)
* [Dependencies](#Dependencies)
* [Contact](#Contact)
* [License](#License)


## General

GC_batch_MTM_calculator is a python script to be used for 
calculating the methanol and DME yields and productivity of samples for the Methane-to-Methanol (MTM) from Gas Chromatography.
Currently GC_batch_MTM_calculator is used at the section for catalysis at
the University of Oslo.

## Purpose

GC_batch_MTM_calculator was created to improve data accecebility and has been designed
to be easily used. IT utalizes the ipywidgets and is designed for a Jupyter Lab interface.

## Installation

Download the python file `GC_class.py`, and save the GC data in a format similar to the one given in the example (`example_sheet.xlsx`) in its own or same directoty.

## How-to
To use the program:


NB: *Before runging the program, the directory where the .xlsx files with the raw data has to be presonalized. Do this by copying the directory destination into the string* `Main_Direct_GC = ...`, *in* `line 31`.

1. Open a Jupyter Notebook (`.ipynb`) in the same folder as the `GC_class.py` file.
2. Write the following in the first box of the notebook:
```
    %matplotlib widget
    %load_ext autoreload
    %autoreload 2
    %gui asyncio

    from GC_class import GC_analysis_MTM
    obj = GC_analysis_MTM()
```
3. Press Ctrl+Enter to run
4. Choose a data set formt he dropdown curtain.
5. Fill in Cu consentration if unknown, leave as 0). Press Enter to get final calculation.

## Dependencies

This script requires a python enviornment with the following packages, and the packaged these depend on:
```
python          (3.9.7)
pandas          (1.3.3)
numpy           (1.21.2)
matplotlib      (3.4.3)
ipywidgets      (7.6.5)
```
## Contact

For developer issues, please start a ticket in Github. You can also write to the dev team directly at  **b.g.solemsli@smn.uio.no**
#### Authors: 
Bjørn Gading Solemsli (@bjorngso).

## License
This script is under the MIT license scheme. 




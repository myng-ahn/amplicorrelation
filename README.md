# amplicorrelation
In order to run, download `out` and `results` folder from the CSE182: Final Project Google Drive (https://drive.google.com/drive/folders/1Y1aysIJ-7H8zIRMie9V6YaR03Xgk-G8T?usp=sharing). Copy `results` to the main (highest level) directory and `out` to the `amplicorrelation/` directory.

![image](https://github.com/myng-ahn/amplicorrelation/assets/78687742/95352b7d-f223-431a-a5ce-7487f305be27)

# Usage
To create html output of cyclic structure visualization and gene descriptions, `cd` into the `amplicorrelation/` directory and run
```
python write_html.py [-h] -s SAMPLE_NAME -a AMPLICON_NUMBER -c CYCLE_NUMBER
```
html output will be created and stored in the corresponding location in the `results` directory. For example, running
```
python write_html.py -s MFE280_ENDOMETRIUM -a 6 -c 2
```
will create `out/MFE280_ENDOMETRIUM_amplicon6/cycle2/MFE280_ENDOMETRIUM_amplicon6_cycle_2.html`.

# Introduction

Convert NIfTI images from `Hounsfield Units` to `Cormack Units` (and back). The intensity of voxels in CT scans are provided in calibrated [Hounsfield Units (HU](https://radiopaedia.org/articles/hounsfield-unit?lang=us), where air is -1000 and water is 0. Hard bone is [hypodense (dark)](https://www.stritch.luc.edu/lumen/meded/radio/curriculum/structure/imaging_tables_2013.htm) with values near 2000 (metal dental work can be even denser). Most soft tissue have values in the range –100 to 100 HU. This causes issues for many image processing tools developed for MR magnitude images (where the darkest possible value is zero). MR tools tend to assume that values near zero are air, and that there is a lot of dynamic range for soft tissue. Therefore, [Rorden et al.](https://pubmed.ncbi.nlm.nih.gov/22440645/) suggest a lossless conversion of Hounsfield to `Cormack` Units for image processing. Here we provide a Python implementation of this method.

Note that this implementation intentionally clamps the darks voxels to -1000 HU. Some GE CT use exceptionally dark voxels to indicate voxels outside the field of view. The [dcm_qa_ct](https://github.com/neurolabusc/dcm_qa_ct) repository includes an example CT where unsampled voxels have a value of -1500. Be aware that the clamping is not lossless for these extreme values. This is intentional, improving performance of tools that assume air is darkest. Therefore, after a round-trip of h2c and c2h the darkest values will have an intensity of -1000, regardless of the input.

This repository includes three Python scripts:

 - `make_hounsfield.py` makes a simulated NIfTI image in Hounsfield units, with voxel intensity incrementally increasing from -1024 to 1719.
 - `h2c.py` convert a NIfTI image from Hounsfield to Cormack Units (appending the `c` prefix).
 - `c2h.py` reverses the transform, converting a NIfTI image from Cormack to Hounsfield Units (appending the `h` prefix).
 
Usage:

```
git clone https://github.com/neurolabusc/h2c
cd h2c
python make_hounsfield.py
python h2c.py hounsfield.nii 
python c2h.py chounsfield.nii
```

Note that [niimath](https://github.com/rordenlab/niimath) provides a high performance native executable for computing the same conversions, and combining them with the many image processing functions of fslmath:

```
niimath hounsfield -h2c chounsfield
niimath chounsfield -c2h hchounsfield
```
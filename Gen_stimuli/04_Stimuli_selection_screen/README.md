# Response selection screen creation

The scripts in this folder are for creating the response selection images. They are directly saved into the `/images/` folder of the [experiment](../../Experiments/SiN/Experiment2/SiN_task/images).

Despite being numbered, the order of execution of the scripts does not matter.

## Package requirements

The .png files are created with the package [Pillow](https://pypi.org/project/pillow/) . Install it with `python3 -m pip install --upgrade Pillow`

## Response images

Original *CallSign* images from [MultiPic](https://doi.org/10.1080/17470218.2017.1310261)  
All non-modified callSign images must be copied into the directory of the script `Exp2_01_create_call_images.py`. The script will create a square black frame around the image and save them in the relevant folder of the experiment.

### CallSign and MultiPic Number:
Experiment 1:
| CallSign | MultiPic number | MultiPic filename | Note |
|:---------|:----------------|:------------------|:-----|
| Tiger | Nr. 98 | PICTURE_98.png | - |
| Adler | Nr. 703 | PICTURE_703.png | - |
| Drossel | Nr. 430 | PICTURE_430.png | - |
| Kröte | Nr. 612 | PICTURE_612.png | Actually a frog. Nr. 584 would be a toad. |

Experiment 2:
| CallSign | MultiPic number | MultiPic filename | Note |
|:---------|:----------------|:------------------|:-----|
| Ratte | Nr. 137 | PICTURE_137.png | technically a mouse |
| Tiger | Nr. 98 | PICTURE_98.png | - |
| Adler | Nr. 703 | PICTURE_703.png | - |
| Eule | Nr. 323 | PICTURE_323.png | - |
| Velo | Nr. 23 | PICTURE_23.png | "Fahrrad" |
| Auto | Nr. 302 | PICTURE_23.png | other options: Nr. 358 / Nr. 364 |

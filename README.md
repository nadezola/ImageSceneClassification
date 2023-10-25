# Image Scene Classifier
Image Scene Classification module from [DILAM paper](https://arxiv.org/abs/2305.18953) & [DILAM Github](https://github.com/jmiemirza/DILAM). 

This machine learning approach uses the first two layers of [YOLOv3](https://github.com/ultralytics/yolov3) 
(commit d353371) object detection model, 
pre-trained on a one image scene dataset (e.g., clear weather condition), for further image classication of 
different image scenes (e.g., adverse weather conditions).

![](docs/DILAM_WeatherClassifier.jpg "DILAM")

## Installation on Ubuntu 20.04
* Clone the repository recursively:
```bash
git clone --recurse-submodules https://github.com/nadezola/scene_classifier.git
```
* If you already cloned and forgot to use `--recurse-submodules` you can run: 
```bash
git submodule update --init
```

* We recommend to use Python3.8 virtual environment with `requirements.txt`:

```bash
# apt install python3.8-venv
python3.8 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```


## Dataset preparation
### Data structure:
```
data_root
|
├── images
|      ├──── test
|      |      ├─── *.jpg
|      |
|      ├──── train
|      |      ├─── *.jpg
|      |
|      └──── val
|             ├─── *.jpg
|
├── splits
|      ├──── scene_1
|      |      ├─── train.txt
|      |      └─── val.txt
|      |
|      ├──── scene_2
|      |      ├─── train.txt
|      |      └─── val.txt
|      |
|      ├──── ...
|
├── test.txt
├── train.txt
├── val.txt
|
└── scene_labels.csv 
```
* `test.txt`, `train.txt`, `val.txt` contain a list of images defining the train/val/test splits.
*  `scene_1`, `scene_2`, ... - scene names should match class names `CLS_SCENE` in file `opt.py`

### Splitting by Image Scene:
* To train the Image Scene Classifier, for example, for 4 adverse weather conditions:
_**clear, fog, rain, snow**_, you need to split 
the entire `train.txt` and `val.txt` by image scene (weather condition) and fill up the folder `splits`
* We provide example code to split the entire `train.txt` and `val.txt` by image scene, using
`scene_labels.csv` annotation file  
* Example of `scene_labels.csv`:

| Hash              | Weather |
|-------------------|---------|
| vienna20181007_f0 | fog     |
| vienna20181007_f1 | fog     |
| ...               |         |
| vienna20181015_f0 | rain    |

* Configure `opt.py`:
```
CLS_SCENE = ['clear', 'fog', 'rain', 'snow']
```

* Usage:
```bash
python data_splitting.py --data_root <path/to/data_root> 
                         --scene_lbls <path/to/file/with/scene/labels>  # scene_labels.cvs
                         --tsk <str>  # The column with labels in scene_labels.cvs, e.g. 'Weather'
                         --res_dir <path/to/folder/where/to/save/results>
```

* Results
```
# in data_root:

|
├── splits (initially empty)
|      |
|      ├──── clear
|      |      ├─── train.txt
|      |      └─── val.txt
|      |
|      ├──── fog
|      |      ├─── train.txt
|      |      └─── val.txt
|      |
|      ├──── rain
|      |      ├─── train.txt
|      |      └─── val.txt
|      |
|      └──── snow
|             ├─── train.txt
|             └─── val.txt    
```

## Train
Train the Image Scene Classification Head
* Configure `opt.py` file
* Pre-train the [YOLOv3](https://github.com/ultralytics/yolov3) model (commit d353371) on one image scene dataset (e.g., on clear weather condition) 
for your object detection task and put the pre-trained model in `checkpoints` folder
* Run:
```bash
python main.py --data_root <path/to/data/root/> 
               --mode 'train'
               --res_dir <path/to/folder/where/to/save/results>
```

## Evaluate
Evaluate the Image Scene Classification performance on validation dataset.
* Configure `opt.py` file
* Put the weights of Scene Classification Head in `checkpoints` folder
* Run:
```bash
python main.py --data_root <path/to/data/root/> 
               --mode 'eval'
               --weights <path/to/scene/classification/weights>
               --res_dir <path/to/folder/where/to/save/results>
               # --novis option to DO NOT visualize classification results
```

## Predict
Play the Image Scene Classifier on test dataset. No labels needed.
* Configure `opt.py` file
* Put the weights of Scene Classification Head in `checkpoints` folder
* Run:
```bash
python main.py --data_root <path/to/data/root/> 
               --mode 'predict'
               --weights <path/to/scene/classification/weights>
               --res_dir <path/to/folder/where/to/save/results>
               # --novis option to DO NOT visualize classification results
```
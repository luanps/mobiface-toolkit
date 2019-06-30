# MobiFace Python Toolkit

## Table of Contents

* [Installation](#installation)
* [How to Define a Tracker?](#how-to-define-a-tracker)
* [How to Run Experiments on MobiFace?](#how-to-run-experiments-on-mobiface)
* [How to Evaluate Performance?](#how-to-evaluate-performance)
* [How to Visualise the Results?](#how-to-visualise-the-results)
* [Acknowledgement](#acknowledgement)

### Installation
Please use **Python >= 3.5**.

We reccomend using Anaconda to manage your environment, once you've activated your python3 environment:
```
pip install -r requirements.txt
```
Then you can directly copy `mobiface` folder to your workspace to use it or install it by running: 
```
python setup.py install
```

### How to Define a Tracker?

To define a tracker using the toolkit, simply inherit and override `init` and `update` methods from the `Tracker` class. Here is a simple example:

```Python
from mobiface.trackers import Tracker

class CustomTracker(Tracker):
    def __init__(self, name = 'CustomTracker'):
        super(CustomTracker, self).__init__(
            name = name,  # tracker name
        )
    
    def init(self, image, box):
        # perform your initialisation here
        print('Initialisation done!')
        

    def update(self, image):
        # perform your tracking in the current frame
        # store the result in 'box'
        return box # [top_x,top_y, width, height]
```


### How to Run Experiments on MobiFace?
The toolkit expects the dataset in the following directory layout:

    mobiface80
    ├── train.meta.csv                  # Meta information for training videos
    ├── test.meta.csv                   # Meta information for testing videos
    ├── train                           # Training videos and annotations
    │   ├── ...
    │   ├── -0Qw1A50s_s_0.annot.csv     # Annotation csv file
    │   ├── -0Qw1A50s_s_0               # Please download and extract target frames in the folders
    │   │   ├── 00000000.jpg
    │   │   ├── 00000001.jpg
    │   │   ├── ...
    │   └── ...
    ├── test                            # Testing videos and annotations
    │   ├── ...
    │   ├── 7I5t6BAHSGQ_0.annot.csv     # Annotation csv file
    │   ├── 7I5t6BAHSGQ_0               # Please download and extract target frames in the folders
    │   │   ├── 00000000.jpg
    │   │   ├── 00000001.jpg
    │   │   ├── ...
    │   └── ...

> Please request the annotation files on [MobiFace](https://mobiface.github.io).
> Please download the videos using **[youtube-dl](https://github.com/ytdl-org/youtube-dl/)** and extract target frames using **[imageio](https://imageio.readthedocs.io/)** for consistent results.


Instantiate an `ExperimentMobiFace` object, and leave all experiment pipelines to its `run` method:

```Python
from mobiface.experiments import ExperimentMobiFace

# instantiate a tracker
tracker = CustomTracker()

# setup experiment (validation subset)
experiment = ExperimentMobiFace(
    root_dir='/path/to/mobiface80/',    # MOBIFACE80 root directory
    subset='all'                        # which subset to evaluate ('all', 'train' or 'test')
    result_dir='results',               # where to store tracking results
    report_dir='reports'                # where to store evaluation reports
)
experiment.run(tracker, visualize=True)
```

> Note that the toolkit provides image in **RGB** format, if your tracker expects BGR input, as returned by `cv2.imread()`, please flip the channels in `init` and `update` methods of your tracker class.

The tracking results will be stored in `result_dir`.

### How to Evaluate Performance?

Use the `report` method of `ExperimentMobiFace` for this purpose:

```Python
# report tracking performance
experiment.report([tracker.name])
```
All plots are saved in `reports` folder.


When you have different trackers in `result_dir`, you can give all tracker names in a list to report their performance together:

```Python
# report different trackers performance
experiment.report(['CustomTracker', 'CustomTracker_2', 'Customtracker_3'],
        mytracker = 'CustomTracker', # The name of the folder to save the plots
)
```

### Acknowledgement
This toolkit is heavily inspired by [GOT-10k](https://github.com/got-10k/toolkit)

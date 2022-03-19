Use this code in google colab to pull the repo directly. Follow the instructions in the link to get access token.
https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

```
!git clone https://{{username}}:{{token}}@github.com/burn874/MDP.git
%cd /content/MDP

!git config --global user.name "{{username}}"
!git config --global user.email "{{email}}"
!git config --global user.password "{{token}}"
```

## HOW TO USE INFERENCE CODE
```
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from ObjectDetection.onnx_predictor import *

detect_image('/content/MDP/ObjectDetection/images/train/AlphabetA_20.JPG')
```

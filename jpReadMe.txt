git clone https://github.com/johnpaulguzman/models.git
cd models
git remote add upstream https://github.com/tensorflow/models.git
git fetch upstream
### 3. Updating your fork from original repo to keep up with their changes:
git pull upstream master
######################################################################
pip install pipenv
pipenv --python 3.6
pipenv shell
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
pip install tensorflow pillow lxml jupyter matplotlib opencv-contrib-python mss Xlib pyautogui
cd research/object_detection/
python robot.py
######################################################################
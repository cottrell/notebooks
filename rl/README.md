# setup

    brew install ffmpeg

    conda create -n rl
    source activate rl
    conda install pandas numpy scipy ipython
    cd ~/dev && git clone https://github.com/openai/gym.git && cd gym && python setup.py develop
    conda install pytorch torchvision -c pytorch
    pip install atari-py ptan opencv-python tensorboardX tensorflow tensorboard
    pip install --upgrade pip
    ../roboschool/install.sh
    pip install pybullet
    pip freeze > pip_freeze.txt
    conda list --export > conda_list_export.txt


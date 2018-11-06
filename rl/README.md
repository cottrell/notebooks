# setup

    very rough notes, not a script

    brew install ffmpeg

    conda create -y -n rl
    source activate rl
    conda install -y pandas numpy scipy ipython
    [[ -d ~/dev/gym ]] || cd ~/dev && git clone https://github.com/openai/gym.git
    cd ~/dev/gym && python setup.py develop
    conda install -y pytorch torchvision -c pytorch
    pip install atari-py ptan opencv-python tensorboardX tensorflow tensorboard
    pip install --upgrade pip

    ../roboschool/install.sh
    pip install pybullet
    pip freeze > pip_freeze.txt
    conda list --export > conda_list_export.txt


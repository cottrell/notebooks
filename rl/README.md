# setup

    conda create -n rl
    source activate rl
    conda install pandas numpy scipy
    cd ~/dev && git clone https://github.com/openai/gym.git && cd gym && python setup.py develop
    conda install pytorch torchvision -c pytorch
    pip install atari-py ptan opencv-python tensorboardX tensorflow tensorboard

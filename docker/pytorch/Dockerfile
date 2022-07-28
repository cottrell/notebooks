FROM ubuntu:22.04
RUN apt-get update
RUN apt-get install -y python3-pip
RUN ln -s /usr/bin/python3 /usr/bin/python
# RUN apt-get install -y wget
# RUN wget https://bootstrap.pypa.io/get-pip.py
# RUN python get-pip.py
RUN python -m pip install pip --upgrade
# CPU
# RUN pip install --root-user-action=ignore torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
# GPU
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116



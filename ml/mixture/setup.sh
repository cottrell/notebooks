# READ THIS IF YOU NEED MULTIPLE VERSIONS: https://blog.kovalevskyi.com/multiple-version-of-cuda-libraries-on-the-same-machine-b9502d50ae77
conda create -n tfp python=3.6
# they stopped doing tfp-nightly-gpu not sure why but was told to drop the gpu and it will be fine
pip install tf-nightly-gpu tfp-nightly ipython matplotlib pandas
cd ../../extractors; python setup.py develop; cd -
cd ../../mylib; python setup.py develop; cd -

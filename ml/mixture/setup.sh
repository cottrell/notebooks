# READ THIS IF YOU NEED MULTIPLE VERSIONS: https://blog.kovalevskyi.com/multiple-version-of-cuda-libraries-on-the-same-machine-b9502d50ae77
conda create -n tfp python=3.6
pip install tf-nightly-gpu tfp-nightly-gpu ipython matplotlib pandas
cd ../../extractors; python setup.py develop; cd -
cd ../../mylib; python setup.py develop; cd -

#!/bin/bash -e
cd $HOME/projects/notebooks/my-gym/toplevelrepo/corelib && python setup.py develop
cd $HOME/projects/notebooks/extractors && python setup.py develop
cd $HOME/projects/notebooks/my-gym/toplevelrepo/our && python setup.py develop
cd $HOME/projects/notebooks/my-gym && python setup.py develop

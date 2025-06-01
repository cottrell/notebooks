#!/bin/bash -ex
CMD="uv pip install -e ."
cd $HOME/projects/notebooks/my-gym/toplevelrepo/corelib && $CMD
cd $HOME/projects/notebooks/my-gym/toplevelrepo/our && $CMD
cd $HOME/projects/notebooks/my-gym && $CMD
cd $HOME/projects/notebooks/my-gym/my/gym/usr/cottrell/synthetic_data_generators && $CMD
cd $HOME/projects/notebooks/my-gym/my/gym/usr/cottrell/equinox_utils && $CMD
cd $HOME/projects/notebooks/my-gym/my/gym/usr/cottrell/scraper_utils && $CMD
cd $HOME/projects/notebooks/my-gym/toplevelrepo/our/our/extractors/xml_iterator && make build && $CMD

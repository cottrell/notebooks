#!/bin/bash
xvfb-run -s "-screen 0 640x480x24" python $*

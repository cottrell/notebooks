#!/bin/sh -e

# source activate rl
echo $(type python)
# return

ROBOSCHOOL_PATH=~/dev/roboschool

brew install cmake tinyxml assimp ffmpeg

# see https://github.com/openai/roboschool/issues/118
brew reinstall boost-python3 --without-python --with-python3 --build-from-source
ln -s /usr/local/lib/libboost_python36.a /usr/local/lib/libboost_python3.a
ln -s /usr/local/lib/libboost_python36.dylib /usr/local/lib/libboost_python3.dylib

# brew qt getting in the way?
conda install qt
export PKG_CONFIG_PATH=$(dirname $(dirname $(which python)))/lib/pkgconfig

cd ~/dev
git clone https://github.com/olegklimov/bullet3 -b roboschool_self_collision
mkdir bullet3/build
cd    bullet3/build
cmake -DBUILD_SHARED_LIBS=ON -DUSE_DOUBLE_PRECISION=1 -DCMAKE_INSTALL_PREFIX:PATH=$ROBOSCHOOL_PATH/roboschool/cpp-household/bullet_local_install -DBUILD_CPU_DEMOS=OFF -DBUILD_BULLET2_DEMOS=OFF -DBUILD_EXTRAS=OFF  -DBUILD_UNIT_TESTS=OFF -DBUILD_CLSOCKET=OFF -DBUILD_ENET=OFF -DBUILD_OPENGL3_DEMOS=OFF ..
make -j4
make install
cd ../..

pip install -e $ROBOSCHOOL_PATH


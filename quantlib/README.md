See the notes. But these are notes on the notes.

# quantlib

Generally you just want to use the version distributed through pip (Quantlib). This is if you want to build yourself.

https://www.quantlib.org/install/linux.shtml

    sudo apt-get install libboost-all-dev
    cd dev
    git clone https://github.com/lballabio/QuantLib.git
    cd /home/cottrell/dev/QuantLib

    sudo apt-get install automake autoconf libtool
    ./autogen.sh

    mkdir local
    PREFIX=/home/cottrell/dev/QuantLib/local
    ./configure --prefix=$PREFIX
    make
    # sudo make install
    make install # for local dev no sudo should be needed
    # sudo ldconfig # is this sudo needed?
    ldconfig

Test with (defaults):

    cd Examples/BermudanSwaption
    g++ BermudanSwaption.cpp -o BermudanSwaption -lQuantLib
    ./BermudanSwaption

Test with custom location:

    PREFIX=/home/cottrell/dev/QuantLib/local
    g++ BermudanSwaption.cpp -I$PREFIX/include -o BermudanSwaption -L$PREFIX/lib -lQuantLib

# quantlib python

It looks like you need to muck around with PREFIX manually here. See the notes. Basically doesn't work as expected.

https://www.quantlib.org/install/linux-python.shtml

    sudo apt-get install automake autoconf libtool
    sudo apt-get install swig
    ./autogen.sh
    ./configure
    make -C Python
    sudo make -C Python install



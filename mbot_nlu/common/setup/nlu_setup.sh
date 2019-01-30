#!/bin/bash

# nlu common setup dir
nlu_setup_dir="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# bazel install
echo 'WARNING: internet connection is required for next step...'
# bash ${nlu_setup_dir}/bazel_installation.sh

# pip installs
pip_packagelist=(
    asciitree
    tensorflow==1.4.0
    numpy
    msgpack<0.6
    msgpack_numpy
)

pip3_packagelist=(
    numpy
    msgpack<0.6
    msgpack_numpy
)

# Install python packages listed in array above in python 2
pip install ${pip_packagelist[@]} --user

# Install python packages listed in array above in python 3
pip3 install ${pip3_packagelist[@]} --user

# custom commands
echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
curl https://bazel.build/bazel-release.pub.gpg | sudo apt-key add -
sudo apt-get update

# apt installs
debian_packagelist=(
    openjdk-8-jdk
    bazel
    swig
    python-mock
    graphviz
    libgraphviz-dev
)

# Install debian packages listed in array above
sudo apt-get install -y ${debian_packagelist[@]}

# custom commands
sudo apt-get install --only-upgrade bazel
pip install pygraphviz --install-option="--include-path=/usr/include/graphviz" --install-option="--library-path=/usr/lib/graphviz/" --user

# clone tensorflow models (SocRob fork) including submodules
mkdir $HOME/Software
cd $HOME/Software && git clone --recursive https://github.com/socrob/models.git

# configure tensorflow models
cd $HOME/Software/models/syntaxnet/tensorflow && bash configure

# install the SyntaxNet and DRAGNN Python modules
export PYTHON_LIB_PATH=/usr/lib/python2.7/dist-packages
export PYTHON_BIN_PATH=`which python`
cd $HOME/Software/models/syntaxnet

mkdir /tmp/syntaxnet_pkg
bazel-bin/dragnn/tools/build_pip_package --output-dir=/tmp/syntaxnet_pkg
pip install /tmp/syntaxnet_pkg/syntaxnet-0.2-cp27-cp27mu-linux_x86_64.whl --user

#!/bin/bash

# get bazel script and zip file from internet
if [ ! -f bazel-0.5.4-installer-linux-x86_64.sh ]; then
    wget https://github.com/bazelbuild/bazel/releases/download/0.5.4/bazel-0.5.4-installer-linux-x86_64.sh
fi

# run the bazel installation script
sudo bash bazel-0.5.4-installer-linux-x86_64.sh


#!/bin/bash

# Install Rust safely inside the home directory
export CARGO_HOME=$HOME/.cargo
wget https://sh.rustup.rs -O rustup.sh
sh rustup.sh -y --no-modify-path
export PATH="$HOME/.cargo/bin:$PATH"

# Install Python requirements
pip install -r requirements.txt

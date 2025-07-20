#!/bin/bash
python -m venv manimgl
source manimgl/bin/activate
mkdir manimgl_lib_source
cd manimgl_lib_source
git clone https://github.com/dan0326/manimPM.git
cd manimPM
pip install -e .
cd ../
pip install -r ../requirements.txt
cd ../
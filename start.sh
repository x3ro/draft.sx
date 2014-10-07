#!/bin/bash -xe


source venv/bin/activate
pip install -r requirements.txt
honcho -f Procfile.dev start

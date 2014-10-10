# draft.sx

Painlessly share your markdown documents.



## Running locally

Note: If you know a better (i.e. easier) way of running a Flask app (with it's dependencies) locally, then please let me know :)

Install the following dependencies:

* pip
* pyenv
* virtualenv
* redis

If you don't have the required python version, install it (see `.python-version`). After that, in the draft.sx root run

    virtualenv venv

After that you can start the application by running `start.sh`. Note that you might need to adjust the way in which redis is started in `Procfile.dev`!

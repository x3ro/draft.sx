# draft.sx

Painlessly share your markdown documents.



## Running locally

Install the following dependencies:

* pip
* virtualenv
* redis

If you don't have the required python version, install it (see `.python-version`). After that, in the draft.sx root run

    virtualenv venv

After that you can start the application by running `start.sh`. Note that you might need to adjust the way in which redis is started in `Procfile`!



## Deploying

Follow [this guide](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-14-04), but using Python 3. Gunicorn server can be started using 

    gunicorn --workers 3 --bind unix:draftsx.sock -m 007 draft:app

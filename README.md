# draft.sx

Painlessly share your markdown documents.



## Running

Install the following dependencies:

* docker
* docker-compose
* make

For the development setup, run

    make run

For the production environment, run

    make production

In both cases, you can now access draft.sx at port 80, probably on localhost. If you're using `docker-machine`, find out the correct IP by running `docker-machine ip the-machine-name`.

**Note:** You need to run `make build` after changing `requirements.txt`.

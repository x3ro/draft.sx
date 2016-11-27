# draft.sx

Painlessly share your markdown documents.



## Running

Install the following dependencies:

* docker
* docker-compose
* compass [^meh-compass]

For the development setup, run

    docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

For the production environment, just run

    docker-compose up

**Note:** You need to run `docker-compose build` after changing `requirements.txt`.

[^meh-compass]: I wanted to keep it python-only, but the python tooling around SASS was just too cumbersome to use :(

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




## Deploying onto a Digital Ocean Docker instance

Note that the files in `doc/` and the deploy script assume a couple of paths, IPs and usernames, so please modify if your needs differ :)

* Run `ufw enable`
* Install docker-compose
* Add user (`lucas` in my case)
* Clone draft.sx repository (using HTTPS) into `$HOME/draft.sx`
* Add docker and docker-compose to sudoers w/ NOPASSWD (see `doc/sudoers`)
* Add `doc/draftsx.service` to `/etc/systemd/system/`
* Enable service w/ `systemctl enable draftsx`
* Start service w/ `systemctl start draftsx`
* Optional: check out how I'm deploying by looking at `scripts/deploy`

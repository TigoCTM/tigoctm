# Tigo CTM

### Version
1.0.0

### Installation
Tigo CTM requires [Docker](https://www.docker.com/), [Docker Compose](https://docs.docker.com/compose/install/) and [Docker Machine](https://docs.docker.com/machine/install-machine/) (this last one only with OS X) to run.

### Development
Tigo CTM uses Gulp for fast developing.
Make a change in your file and instantanously see your updates!

Open your favorite Terminal and run these commands:

```sh
$ docker-compose build
$ docker-compose run --rm app npm install
$ docker-compose up
```

Open a web browser an enter to: `http://localhost:3000` (For OS X users: `http://192.168.99.100:3000`).

If you want to see how is going to work the app like in production, follow these steps:

With Docker Machine:

```sh
$ echo "192.168.99.100 dev.tigoctm.com" | sudo tee -a /etc/hosts > /dev/null
```

Without Docker Machine:

```sh
$ echo "127.0.0.1 dev.tigoctm.com" | sudo tee -a /etc/hosts > /dev/null
```

And then, run:

```sh
$ docker-compose run --rm app gulp build
```

Open a web browser an enter to: `http://dev.tigoctm.com`.

### Production

```sh
$ docker-compose -f docker-compose-production.yml build
$ docker-compose -f docker-compose-production.yml run --rm app npm install
$ docker-compose -f docker-compose-production.yml up -d
```

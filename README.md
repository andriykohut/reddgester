# reddgester - reddit digester

Toy project where I'm trying to use interesting tools/libraries.
It provides an API for triggering email reddit digest.

## Installation

I've used `docker-compose` to glue everything together, so it should be pretty easy, just run `docker-compose build` and then `docker-compose up`

## Design
The project consists of 3 main parts: api, digester and mailer. Each of this parts has it's own dependancies, `Dockerfile`, `requirements.txt`, etc.
### API
Single endpoint  `/trigger_digest`:
```sh
curl -H "Content-Type: application/json" \
    -X POST -d '{"limit": 10, "r": "python", "to": "bob@bob.com"}' \
    http://localhost:8080/trigger_digest
```
will send an email with top 10 posts from https://www.reddit.com/r/Python to `bob@bob.com`

Build with [aiohttp](https://github.com/KeepSafe/aiohttp), triggers RPC to [nameko](https://github.com/onefinestay/nameko)-based `digester` microservice.

### Digester
[nameko](https://github.com/onefinestay/nameko)-based `digester` microservice. Grabs the data from reddit using [praw](https://github.com/praw-dev/praw) and sends it to the mailer

### Mailer
Another nameko-based microservice. It just sends the digest with [smtplib](https://docs.python.org/3.5/library/smtplib.html). Nothing fancy. By default compose launches [MailHog](https://github.com/mailhog/MailHog) where you can check out the digest being sent (MailHog web interface runs on `8025` port), but you can use any other SMTP server, just change this env vars in `mailer` section of `docker-compose.yml`:
```yaml
environment:
    DIGEST_FROM: andriy.kogut@gmail.com
    SMTP_HOST: mailhog
    SMTP_PORT: 1025
```

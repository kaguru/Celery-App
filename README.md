# LNH AUTHENICATION SERVICE

Simple Flask Celery Application
## Installation

Use the package manager [pipenv](https://pypi.org/project/pipenv/) to install foobar.

```bash
# ACTIVATE ENVIRONEMENT
pipenv shell

# INSTALL PACKAGES
pipenv shell
```

## USAGE

```python
# RUN RabbitMQ with Management Panel
docker run -p 5672:5672 -p 8080:15672 -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=pass rabbitmq:3-management

# RUN Redis Server 
docker run -p 6379:6379 redis

# RUN Celery Worker
celery -A tasks worker --loglevel=info

# Monitor Redis
docker exec -it <redis_container_id> bash
redis-cli monitor

# RUN APP
python app.py


```
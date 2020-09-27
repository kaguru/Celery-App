# CELERY APP

A Simple Celery Application

## Docker Images Installation

```bash
# REDIS DOCKER IMAGE
docker pull redis

# RABBITMQ DOCKER IMAGE
docker pull rabbitmq
```

## Packages Installation

Use the package manager [pip](https://pypi.org/project/pip/) to install packages.

```bash
# ACTIVATE ENVIRONEMENT
source venv/bin/activate

# INSTALL PACKAGES
pip install -r requirements.txt
```


## Usage

```python
# RUN RabbitMQ with Management Panel
docker run -p 5672:5672 -p 8080:15672 -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=pass rabbitmq:3-management

# RUN Redis Server 
docker run -p 6379:6379 redis

# RUN Celery Worker
celery -A tasks worker --loglevel=info


# RUN APP
python app.py

# Monitor RedisServer
docker exec -it <redis_container_id> bash
redis-cli monitor

```
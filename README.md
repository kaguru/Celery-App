# CELERY APP

A Simple Celery Application


## Usage

```python
# Build Docker Base Images
docker build -t ubuntu_18_pipenv -f ./Dockerfile_base .
docker build -t ubuntu_18_pipenv_celery -f ./Dockerfile_base_celery .


# Build and Run Containers
docker-compose build
docker-compose up

# Monitor RedisServer
docker exec -it <redis_container_id> bash
redis-cli monitor
```
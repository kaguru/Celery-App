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


## Trigger tasks
#### PASS
[http://127.0.0.1:5000/add?x=4&y=7](http://127.0.0.1:5000/add?x=4&y=7)
<br>
[http://127.0.0.1:5000/divide?x=10&y=2](http://127.0.0.1:5000/divide?x=10&y=2)

#### FAIL AFTER RETRYING
[http://127.0.0.1:5000/add?x=4&y=R](http://127.0.0.1:5000/add?x=4&y=R)
<br>
[http://127.0.0.1:5000/divide?x=10&y=0](http://127.0.0.1:5000/divide?x=10&y=0)

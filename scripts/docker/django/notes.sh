# Docker image for Django creation (Mac)
# docker system prune -a  # delete all containers and images
# docker rm [name]
# docker rm -f [name]
# docker rm --force [name]
# docker rm -vf $(docker ps -a -q)
cd ~/Projects/Homepage/scripts/docker/django
docker build -t homepage-django .
docker images

docker run -p 10.0.0.3:8001:8000 homepage-django
# docker rmi homepage-django homepage-django-2
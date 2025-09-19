name=backend
docker stop $name
docker rm -f $name
docker build -t $name .
docker run -d -p 8001:8000 --name $name $name
docker logs -f $name
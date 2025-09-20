name=backend
docker stop $name
docker rm -f $name
docker build -t $name --target builder .

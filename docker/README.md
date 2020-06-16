### - Docker commands:
    + docker build -t hello-world-docker .
    + docker images hello-world-docker
    + docker run --rm -d -v 'pwd':/app -p 5000:5000 hello-world-docker
    + docker logs 5ca3f6989e88

        - The --rm argument tells the Docker server to remove this container once it stops
        running. This is useful to prevent old containers from clogging the local filesystem.

        - The -d argument tells the Docker server to run this container in the background.

        - The -v argument specifies that the current directory
        (pwd) is mapped to the /app directory inside the Docker container.
        This is essential for the local development workflow we want
        to achieve because it enables us to edit the application files
        locally and have them be auto-reloaded by the Flask development
        server running inside the container.

        - The -p 5000:5000 argument maps the first port (5000) locally
        to the second port (5000) inside the container.”

    + docker ps
    + docker stop 6be154deee83
    + docker rmi hello-world-docker

    $ Docker Registry (Upload a docker image to DockerHub)
    - docker login
    - docker tag hello-world-docker hello-world-docker:v1 (tag image)

    + Before you can publish the hello-world-docker image to Docker Hub,
      you also need to tag it with the Docker Hub repository name,
      which contains your username or your organization name.
      In our case, this repository is mdrahali/hello-world-docker:

      $ docker tag hello-world-docker:latest mdrahali/hello-world-docker:latest
      $ docker tag hello-world-docker:v1 mdrahali/hello-world-docker:v1

      $ docker push mdrahali/hello-world-docker:latest
      $ docker push mdrahali/hello-world-docker:v1


### + run docker image :

    - Run docker image as a daemon :
    $ docker run --rm -d -v `pwd`:/app -p 5000:5000 hello-world-docker


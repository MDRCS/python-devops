# python-devops

### - Command-line:
    + ps -eo pcpu,pid,user,args | sort -r | head -10 (CPU Utility)
    - htop - an interactive process viewer
    + brew install htop
    + htop (launch command)
    + h (for help) s (for setup) > (for sorting) t (show as a tree)
    + pip list --format=json (display dict of packages and versions)

### - Version Control - Compatibility
    + pip install setuptools twine
    + python3 setup.py sdist (Create a dist folder to manage Versions [major].[minor].[patch])

    --> The newly created tar.gz file is an installable package!
    This package can now be uploaded to PyPI for others to install directly from it.
    By following the version schema, it allows installers to ask for a specific version (0.0.1 in this case),
    and the extra metadata passed into the setup() function enables other tools to discover it and show information about it,
    such as the author, description, and version.”

    + pip install dist/hello-world-0.0.1.tar.gz

    - Upload Package to PyPI:
    + login
    + twine upload --repository-url https://test.pypi.org/legacy/ \
        dist/hello-world-0.0.1.tar.gz

    - Install the package from the source:
    + python3 -m pip install --index-url https://test.pypi.org/simple/hello-world

    - Automate Upload package to PyPI:
    + make deploy-pypi

    +  Changelog (linux only)
    - sudo apt-get install devscripts
    -  $ export DEBEMAIL="alfredo@example.com"
       $ export DEBFULLNAME="Alfredo Deza”
    -  dch --package "hello-world" --create -v "0.0.1" \
       -D stable "New upstream release” (Produce Changelog)


### - Naming Convention
    + {region}.{prod|staging|dev}.{server_name}
    Ex: us-west2.dev.server1

### - Testing:
    + pytest testing_params.py

### - Run docker-compose :

    $ git clone https://github.com/realpython/flask-by-example.git
    $ cd db & vi docker-compose.yaml
    -> paste :
        version: "3"
        services:
          db:
            image: "postgres:11"
            container_name: "postgres"
            ports:
              - "5432:5432"
            volumes:
              - dbdata:/var/lib/postgresql/data
        volumes:
          dbdata:


    $ docker-compose up -d db

    - Inspect the logs for the db service :
    $ docker-compose logs db

    $ docker ps -al

    # check volume of postgres database
    $ docker volume ls | grep dbdata

    - to connect to db
    $ docker-compose exec db psql -Upostgres

        or -> docker exec -it $(docker-compose ps -q db ) psql -Upostgres

    # create database
    $ postgres=# create database wordcount;

    # list all databases
    $ \l

    - exit cli
    $ \q

    + Connect to the wordcount database and create a role called wordcount_dbadmin
      that will be used by the Flask application:

    $ postgres=# CREATE ROLE wordcount_dbadmin;
    $ postgres=# ALTER ROLE wordcount_dbadmin LOGIN;
    $ postgres=# ALTER USER wordcount_dbadmin PASSWORD 'MYPASS';
    $ postgres=# \q

    - Command for storing data from sql script
    $ docker exec -it $(docker-compose ps -q postgres9 ) pg_dump -Upostgres > backup.sql

    # - we have a password of postgresql db and we don't want to store it in a hardcoded manner.
    + The DATABASE_URL variable definition refers to another variable called DBPASS, instead of
      hardcoding the password for the wordcount_dbadmin user. The docker-compose.yaml file is
      usually checked into source control, and best practices are not to commit secrets such
      as database credentials to GitHub. Instead, use an encryption tool such as sops to manage a secrets file.


    Here is an example of how to create an encrypted file using sops with PGP encryption.
    First, install gpg on macOS via brew install gpg, then generate a new PGP key with an empty passphrase:

    $ brew install gpg
    $ gpg --generate-key
        {passphrase : mdrahali1, user id : mdrahali, email: elrahali.md@gmail.com}

    #next download sops from the source :
    -> https://github.com/mozilla/sops/releases


    $ cd webapp_flask
    $ pip install -U sops
    $ sops -v
    $ sops --pgp "1A577283451C84A95AC2DC006690F9D02C7A44AB" environment.secrets

    + This will open the default editor and allow for the input of the plain-text secrets. In this example,
      the contents of the environment.secrets file are:

    $ export DBPASS=MYPASS

    After saving the environment.secrets file, inspect the file to see that it is encrypted, which makes it
    safe to add to source control:

    $ cat environment.secrets

    To decrypt the file, run:
    $ export GPG_TTY=$(tty)
    $ sops -d environment.secrets

    ++ Start a migration of database schema (sops, docker) :
    $ source <(sops -d environment.secrets); docker-compose up -d migrations

    ++ Verify that the migrations were successfully run by inspecting the database and verifying that two tables were created:
       alembic_version and results:

    $ docker-compose exec db psql -U
    $ \dt

    - Part 4 in the “Flask By Example” tutorial is to deploy a Python worker process based on Python RQ that talks to an instance of Redis.
    ++ Start the redis service on its own by specifying it as an argument to :

    $ docker-compose up -d redis
    $ docker-compose logs redis

    ++ The next step is to create a service called worker for the Python RQ worker process in docker-compose.yaml:

      worker:
        image: "flask-by-example:v1"
        command: "worker.py"
        environment:
          APP_SETTINGS: config.ProductionConfig
          DATABASE_URL: postgresql://wordcount_dbadmin:$DBPASS@db/wordcount
          REDISTOGO_URL: redis://redis:6379”
            [...]

    - Run the worker service just like the redis service, with docker-compose up -d:

    $ docker-compose up -d worker
    $ docker-compose logs worker

    # Run the Flask app
    - Start up the app service with docker compose up -d, while also running sops -d on
      the encrypted file containing DBPASS, then sourcing the decrypted file before calling docker-compose:

    $ source <(sops -d environment.secrets); docker-compose up -d app

    ++ Container Orchestration: Kubernetes
    If you are experimenting with Docker, or if running a set of Docker containers on a single machine is all you need,
    then Docker and Docker Compose would be sufficient for your needs. However, as soon as you move from the number 1 (single machine)
    to the number 2 (multiple machines), you need to start worrying about orchestrating the containers across the network. For production scenarios,
    this is a given. You need at least two machines to achieve fault tolerance/high availability.”

    ++ We will use a tool called Kompose to translate this YAML file into a set of Kubernetes manifests.

    To get a new version of Kompose on a macOS machine, first download it from the Git repository, then move it to /usr/local/bin/kompose,
    and make it executable. Note that if you rely on your operating system’s package management system (for example, apt on Ubuntu systems
    or yum on Red Hat systems) for installing Kompose, you may get a much older version that may not be compatible to these instructions.

    -> https://kompose.io/
    # macOS
    $ curl -L https://github.com/kubernetes/kompose/releases/download/v1.19.0/kompose-darwin-amd64 -o kompose

    $ chmod +x kompose
    $ sudo mv ./kompose /usr/local/bin/kompose

    Run the kompose convert command to create the Kubernetes manifest files from the existing docker-compose.yaml file:

    $ cd webapp_flask
    $ kompose convert

    $ minikube start
    $ kubectl config use-context minikube
    $ kubectl get nodes

    # Start provisionning yaml files related to your webapp
    $ kubectl delete all --all (clean up)
    $ kubectl create -f dbdata-persistentvolumeclaim.yaml
    $ kubectl get pvc
    $ kubectl create -f db-deployment.yaml
    $ kubectl get deployments
    $ kubectl get pods

    ++ Next, create the database for the example Flask application. Use a similar command to docker exec to run the psql command
       inside a running Docker container. The form of the command in the case of a Kubernetes cluster is kubectl exec:

    $ kubectl exec -it db-57967c4668-q82mp -- psql -U postgres
    $ postgres=# CREATE ROLE wordcount_dbadmin;
    $ postgres=# ALTER ROLE wordcount_dbadmin LOGIN;
    $ postgres=# ALTER USER wordcount_dbadmin PASSWORD 'MYPASS';
    $ postgres=# create database wordcount_dev;
    $ postgres=# \l
    $ postgres=# \q

    ++ The next step is to create the Service object corresponding to the db deployment, that will expose the deployment to the other
       services running inside the cluster, such as the Redis worker service and the main application service.

    $ kubectl create -f db-service.yaml
    $ kubectl get svc

    ++ The next service to deploy is Redis.
    $ kubectl create -f redis
    $ kubectl create -f redis-deployment.yaml
    $ kubectl create -f redis-service.yaml
    $ kubectl get svc

    So far, the two services that have been deployed, db and redis, are independent of each other. The next part of the application is the worker process,
    which needs to talk to both PostgreSQL and Redis. This is where the advantage of using Kubernetes services comes into play. The worker deployment can
    refer to the endpoints for PostgreSQL and Redis by using the service names. Kubernetes knows how to route the requests from the client (the containers
    running as part of the pods in the worker deployment) to the servers (the PostgreSQL and Redis containers running as part of the pods in the db and redis
    deployments, respectively).

    One of the environment variables used in the worker deployment is DATABASE_URL. It contains the database password used by the application. The password
    should not be exposed in clear text in the deployment manifest file, because this file needs to be checked into version control. Instead,
    create a Kubernetes Secret object.

    First, encode the password string in base64:
    $ echo MYPASS | base64

    Then, create a manifest file describing the Kubernetes Secret object that you want to create. Since the base64 encoding of the password is not secure,
    use sops to edit and save an encrypted manifest file secrets.yaml.enc:

    $ sops --pgp "1A577283451C84A95AC2DC006690F9D02C7A44AB" secrets.yaml.enc

    Inside the editor, add these lines:

    apiVersion: v1
    kind: Secret
    metadata:
      name: fbe-secret
    type: Opaque
    data:
      dbpass: TVlQQVNTCg==

    The secrets.yaml.enc file can now be checked in because it contains the encrypted version of the base64 value of the password.

    To decrypt the encrypted file, use the sops -d command:

    $ sops -d secrets.yaml.enc

    apiVersion: v1
    kind: Secret
    metadata:
      name: fbe-secret
    type: Opaque
    data:
      dbpass: TVlQQVNTCg==

    - Pipe the output of sops -d to kubectl create -f to create the Kubernetes Secret Object:
    $ sops -d secrets.yaml.enc | kubectl create -f -
    $ kubectl get secrets

    - To get the base64-encoded Secret back, use:
    $ kubectl get secrets fbe-secret -ojson | jq -r ".data.dbpass"

    - To get the plain-text password back, use the following command on a macOS machine:

    $ kubectl get secrets fbe-secret -ojson | jq -r ".data.dbpass" | base64 -D TVlQQVNTCg==

    - launch the worker
    $ kubectl create -f worker-deployment.yaml

    $ kubectl get pods
    $ kubectl describe pod worker-65bb94d587-88g96 | tail -10

    # + dockerhub credentials

    The deployment tried to pull the griggheo/flask-by-example:v1 private Docker image from Docker Hub,
    and it lacked the appropriate credentials to access the private Docker registry. Kubernetes includes
    a special type of object for this very scenario, called an imagePullSecret.

    Create an encrypted file with sops containing the Docker Hub credentials and the call to kubectl create secret:

    $ sops --pgp "1A577283451C84A95AC2DC006690F9D02C7A44AB" \
    create_docker_credentials_secret.sh.enc

    The contents of the file are:

    DOCKER_REGISTRY_SERVER=docker.io
    DOCKER_USER=mdrahali
    DOCKER_EMAIL=elrahali.md@gmail.com
    DOCKER_PASSWORD=mohamed-2

    kubectl create secret docker-registry myregistrykey \
    --docker-server=$DOCKER_REGISTRY_SERVER \
    --docker-username=$DOCKER_USER \
    --docker-password=$DOCKER_PASSWORD \
    --docker-email=$DOCKER_EMAIL”

    + Create secret for docker registry
    $ sops -d create_docker_credentials_secret.sh.enc | bash -

    + Inspect secret
    $ kubectl get secrets myregistrykey -oyaml

    The only change to the worker deployment manifest is to add these lines:

      imagePullSecrets:
            - name: myregistrykey
     Include it right after this line:

     restartPolicy: Always
    Delete the worker deployment and recreate it:

    $ kubectl delete -f worker-deployment.yaml

    $ kubectl create -f worker-deployment.yaml

    Now the worker pod is in a Running state, with no errors:

    $ kubectl get pods

    ++ Inspect the worker pod’s logs with the kubectl logs command:

    $ kubectl logs worker-65c65bf75c-268p6

    The next step is to tackle the application deployment. When the application was deployed in a docker-compose setup,
    a separate Docker container was employed to run the migrations necessary to update the Flask database. This type of
    task is a good candidate for running as a sidecar container in the same pod as the main application container.
    The sidecar will be defined as a Kubernetes initContainer inside the application deployment manifest. This type of container
    is guaranteed to run inside the pod it belongs to before the start of the other containers included in the pod.

    Add this section to the app-deployment.yaml manifest file that was generated by the Kompose utility, and delete the migrations-deployment.yaml file:

      initContainers:
      - args:
        - manage.py
        - db
        - upgrade
        env:
        - name: APP_SETTINGS
          value: config.ProductionConfig
        - name: DATABASE_URL
          value: postgresql://wordcount_dbadmin:@db/wordcount
        image:
            [...]

    $ rm migrations-deployment.yaml

    ++ Reuse the fbe-secret Secret object created for the worker deployment in the application deployment manifest :

    $ kubectl create -f app-deployment.yaml
    $ kubectl get pods

    % For debugging purpose :

    # to access initContainer logs
    $ kubectl logs <pod-name> -c <init-container-2>
    $ kubectl logs app-79d46bd986-hhh6s -c migrations

    # access database inside pod :
    $ kubectl exec -it db-6c9b67bcd6-wgscs -- psql -U postgres

    $ kubectl create -f app-service.yaml
    $ kubectl get svc

    $ minikube service app

    -> test with this url : www.bbc.com/news/world-asia-53061476


    # kmeans benchmark :

    Forking Processes with Pool()
    A straightforward way to test out the ability to fork multiple processes and run a function against them is to calculate KMeans clustering with the sklearn machine learning library.
    A KMeans calculation is computed intensively and has a time complexity of O(n**2), which means it grows exponentially slower with more data.
    This example is a perfect type of operation to parallelize, either at the macro or the micro level. In the following example, the make_blobs method
    creates a dataset with 100k records and 10 features. This process has timing for each KMeans algorithm as well as the total time it takes:

    $ python3 kmeans-sequentials.py

        KMeans cluster fit in 0.28795695304870605
        KMeans cluster fit in 0.28539109230041504
        KMeans cluster fit in 0.26807498931884766
        KMeans cluster fit in 0.27394938468933105
        KMeans cluster fit in 0.2867238521575928
        KMeans cluster fit in 0.28345322608947754
        KMeans cluster fit in 0.27866387367248535
        KMeans cluster fit in 0.2906341552734375
        KMeans cluster fit in 0.2845587730407715
        KMeans cluster fit in 0.2843918800354004
        Performed 10 KMeans in total time:3.764841079711914


    In the following example, the multiprocessing.Pool.map, the method is used to distribute 10 KMeans cluster operations to a pool of 10 processes.
    This example occurs by mapping the argument of 100000 to the function do_kmeans:

    $ python3 kmeans-multi-processing.py

        KMeans cluster fit in 0.9413900375366211
        KMeans cluster fit in 0.8751249313354492
        KMeans cluster fit in 0.9543578624725342
        KMeans cluster fit in 0.9621539115905762
        KMeans cluster fit in 0.8940467834472656
        KMeans cluster fit in 0.9359569549560547
        KMeans cluster fit in 0.9152288436889648
        KMeans cluster fit in 1.0032238960266113
        KMeans cluster fit in 0.9099111557006836
        KMeans cluster fit in 0.9742820262908936
        Performed 10 KMeans in total time: 1.2758479118347168

    This example shows why it is essential to profile code and also be careful about immediately jumping to concurrency.
    If the problem is small scale, then the overhead of the parallelization approach could slow the code down in addition
    to making it more complex to debug.

    ++ Running True Multicore Multithreaded Python Using Numba
    One common performance problem with Python is the lack of true, multithreaded performance. This also can be fixed with Numba.
    Here’s an example of some basic operations:

    Launching a EKS Kubernetes Cluster in AWS with Pulumi

    + Start by creating a new directory:
    $ mkdir pulumi_eks
    $ cd pulumi_eks

    $ download the content of this folder ->  https://github.com/pulumi/examples/tree/master/aws-py-eks

    - Install dependencies (a virtualenv is recommended):

    $ virtualenv -p python3 venv
    $ source venv/bin/activate
    $ pip3 install -r requirements.txt

    - Create a new stack

    $ pulumi stack init python-eks-testing

    - Set the AWS region:

    $ pulumi config set aws:region us-east-2

    - Run pulumi up to preview and deploy changes:

    $ pulumi up

    - View the cluster name via stack output:

    $ pulumi stack output

    - Verify that the EKS cluster exists, by either using the AWS Console or running

    $ aws eks list-clusters

    - Update your KubeConfig, Authenticate to your Kubernetes Cluster and verify you have API access and nodes running.
    %% link local kubectl to aws:eks

    $ aws eks --region us-east-2 update-kubeconfig --name $(pulumi stack output cluster-name)

    $ kubectl get nodes


    # to delete this cluster
    $ pulumi destroy


    ++ Deploying the Flask Example Application to EKS :

    $ kubectl create -f redis-deployment.yaml
    $ kubectl create -f dbdata-persistentvolumeclaim.yaml
    $ kubectl create -f db-deployment.yaml
    $ kubectl logs db-6c9b67bcd6-9r5bl

    $ kubectl create -f redis-service.yaml

    We hit a snag when trying to create the db deployment. GKE provisioned a persistent volume that was mounted as
    /var/lib/postgresql/data, and according to the error message above, was not empty.
    Delete the failed db deployment:

    $ kubectl delete -f db-deployment.yaml

    Create a new temporary pod used to mount the same dbdata PersistentVolumeClaim as /data inside the pod, so its filesystem can
    be inspected. Launching this type of temporary pod for troubleshooting purposes is a useful technique to know about:

    $ kubectl create -f pvc-inspect.yaml

    Use kubectl exec to open a shell inside the pod so /data can be inspected:
    $ kubectl exec -it pvc-inspect -- sh
    $ cd /data
    $ /data # ls -la
    $ rm -rf lost\+found/
    $ exit

    Note how /data contained a directory called lost+found that needed to be removed.
    Delete the temporary pod:
    $ kubectl delete pod pvc-inspect

    Create the db deployment again, which completes successfully this time:

    $ kubectl create -f db-deployment.yaml
    $ kubectl get pods

    Create wordcount database and role:
    $ kubectl exec -it db-6c9b67bcd6-wgscs -- psql -Upostgres

    $ postgres=# create database wordcount;
    $ postgres=# \q

    $ kubectl exec -it db-6c9b67bcd6-wgscs -- psql -U postgres wordcount
    $ wordcount=# CREATE ROLE wordcount_dbadmin;
    $ wordcount=# ALTER ROLE wordcount_dbadmin LOGIN;
    $ wordcount=# ALTER USER wordcount_dbadmin PASSWORD
    $ wordcount=# \q

    $ kubectl create -f db-service.yaml

    Create the Secret object based on the base64 value of the database password.
    The plain-text value for the password is stored in a file encrypted with sops:

    $ echo MYNEWPASS | base64
    $ pip install sops
    $ sops secrets.yaml.enc
        apiVersion: v1
        kind: Secret
        metadata:
            name: fbe-secret
        type: Opaque
        data:
          dbpass: TVlORVdQQVNTCg==

    $ sops -d secrets.yaml.enc | kubectl create -f -
    $ kubectl describe secret fbe-secret

    - Create another Secret object representing the Docker Hub credentials:
    $ sops -d create_docker_credentials_secret.sh.enc | bash -

    ++ Since the scenario under consideration is a production-type deployment of the appication to EKS,
       set replicas to 3 in worker- deployment.yaml to ensure that three worker pods are running at all times:

    $ kubectl create -f worker-deployment.yaml

    ++ Make sure that three worker pods are running:

    $ kubectl get pods

    ++ Similarly, set replicas to two in app-deployment.yaml:
    $ kubectl create -f app-deployment.yaml

    ++ Make sure that two app pods are running:
    $ kubectl get pods

    Create the app service:
    $ kubectl create -f app-service.yaml

    ++ Note that a service of type LoadBalancer was created:
    $ kubectl describe service app

    - Test the application by accessing the endpoint URL based on the IP address corresponding to LoadBalancer Ingress:
      http://aa2c4f5986b55453289d9f92aa1e7e4b-1329777127.us-east-2.elb.amazonaws.com:5000/

    -> test with this url : www.bbc.com/news/world-asia-53073338

    Installing Prometheus and Grafana Helm Charts
    In its current version (v2 as of this writing), Helm has a server-side component called Tiller that needs certain permissions
    inside the Kubernetes cluster.
    Create a new Kubernetes Service Account for Tiller and give it the proper permissions:

    $ kubectl -n kube-system create sa tiller

    $ kubectl create clusterrolebinding tiller-role-binding --clusterrole cluster-admin --serviceaccount=kube-system:tiller
    $ helm init --service-account tiller
    $ kubectl patch deploy --namespace kube-system \
        tiller-deploy -p  '{"spec":{"template":{"spec": {"serviceAccount":"tiller"}}}}'

    $ kubectl get pods --namespace=kube-system

    1- install Helm
    # go to https://github.com/helm/helm/releases/tag/v3.2.1
    # copy the link of linux files
    $ wget https://get.helm.sh/helm-v3.2.1-linux-amd64.tar.gz
    $ ls

    2- unzip the folder
    $ tar zxvf helm-v3.2.1-linux-amd64.tar.gz
    $ sudo mv darwin-amd64/helm /usr/local/bin
    $ rm helm-v3.2.1-linux-amd64.tar.gz
    $ rm -rf ./darwin-amd64

    $ helm version

    + Create a namespace called monitoring:
    $ kubectl create namespace monitoring

    + Install Prometeous :

    $ helm install --name prometheus --namespace monitoring stable/prometheus
        or helm install stable/prometheus-operator --version=8.2.0 --name=monitoring --namespace=monitoring
    $ kubectl get pods -nmonitoring
    $ kubectl get services -nmonitoring
    $ kubectl get configmaps -nmonitoring

    Connect to Prometheus UI via the kubectl port-forward command:
    $ export PROMETHEUS_POD_NAME=$(kubectl get pods --namespace monitoring \
      -l "app=prometheus,component=server" -o jsonpath="{.items[0].metadata.name}")

    $ echo $PROMETHEUS_POD_NAME
    prometheus-server-7555945646-d86gn

    $ kubectl --namespace monitoring port-forward $PROMETHEUS_POD_NAME 9090

    -> Go to localhost:9090 in a browser and see the Prometheus UI.

    ++ Install the Grafana Helm chart in the monitoring namespace:
    $ helm install --name grafana --namespace monitoring stable/grafana

    List Grafana-related pods, services, configmaps, and secrets in the monitoring namespace:

    $ kubectl get pods -nmonitoring | grep grafana
    $ kubectl get services -nmonitoring | grep grafana
    $ kubectl get configmaps -nmonitoring | grep grafana
    $ kubectl get secrets -nmonitoring | grep grafana

    Retrieve the password for the admin user for the Grafana web UI:
    $ kubectl get secret --namespace monitoring grafana \
      -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

    Connect to the Grafana UI using the kubectl port-forward command:

    # search for grafana pod
    $ kubectl get pods -nmonitoring | grep grafana
    # forward a port
    $ kubectl --namespace monitoring port-forward grafana-55744579f5-rrv7b 3000

    -> login admin/BPvivW4HbcL4C9AahJyon5RmhoeWuNvGlsCqqrnC

    List the charts currently installed with helm list. When a chart is installed, the current installation is called a “Helm release”:
    $ helm list

    Most of the time you will need to customize a Helm chart. It is easier to do that if you download the chart and install it from the local filesystem with helm.
    Get the latest stable Prometheus and Grafana Helm charts with the helm fetch command, which will download tgz archives of the charts:

    $ mkdir charts
    $ cd charts
    $ helm fetch stable/prometheus
    $ helm fetch stable/grafana

    Unarchive the tgz files, then remove them:
    $ tar xfz prometheus-11.5.0.tgz; rm prometheus-11.5.0.tgz
    $ tar xfz grafana-5.2.1.tgz; rm grafana-5.2.1.tgz


    The templatized Kubernetes manifests are stored by default in a directory called templates under the chart directory, so in this case these locations
    would be prometheus/templates and grafana/templates. The configuration values for a given chart are declared in the values.yaml file in the chart directory.
    As an example of a Helm chart customization, let’s add a persistent volume to Grafana, so we don’t lose the data when we restart the Grafana pods.
    Modify the file grafana/values.yaml and set the the value of the enabled subkey under the persistence parent key to true (by default it is false) in this section:

    persistence:
      type: pvc
      enabled: true

    Upgrade the existing grafana Helm release with the helm upgrade command. The last argument of the command is the name
    of the local directory containing the chart. Run this command in the parent directory of the grafana chart directory:

    $ helm upgrade grafana grafana/

    Verify that a PVC has been created for Grafana in the monitoring namespace:
    $ kubectl describe pvc grafana -nmonitoring

    Another example of a Helm chart customization, this time for Prometheus, is modifying the default retention period of 15 days for the data stored in Prometheus.
    Change the retention value in prometheus/values.yaml to 30 days:

      ## Prometheus data retention period (default if not specified is 15 days)
      ##
      retention: "30d"

    Upgrade the existing Prometheus Helm release by running helm upgrade. Run this command in the parent directory of the prometheus chart directory:
    $ helm upgrade prometheus prometheus/

    Verify that the retention period was changed to 30 days. Run kubectl describe against the running Prometheus pod in the monitoring namespace and look
    at the Args section of the output:

    $ kubectl get pods -nmonitoring

    $ kubectl describe pod prometheus-server-57d8c46b6b-d5qgb -nmonitoring

    # delete all the cluster from eks aws :
    $ pulumi destroy


### ++ Serverless :

    - Lambda functions can be triggered by other cloud services, use cases include:

    + Extract-Transform-Load (ETL) data processing, where, as an example, a file is uploaded to S3, which triggers the execution of a
      Lambda function that does ETL processing on the data and sends it to a queue or a backend database
    + ETL processing on logs sent by other services to CloudWatch
    + Scheduling tasks in a cron-like manner based on CloudWatch Events triggering Lambda functions
    + Real-time notifications based on Amazon SNS triggering Lambda functions
    + Email processing using Lambda and Amazon SES
    + Serverless website hosting, with the static web resources such as Javascript, CSS, and HTML stored in S3 and fronted by the CloudFront CDN service,
      and a REST API handled by an API Gateway routing the API requests to Lambda functions, which communicate with a backend such as Amazon RDS or Amazon DynamoDB

    Caas (container as a service) vs Faas (function as a service) :

    How do you choose between FaaS and CaaS? In one dimension, it depends on the unit of deployment. If you only care about short-lived functions, with few
    dependencies and small amounts of data processing, then FaaS can work for you. If, on the other hand, you have long-running processes with lots of dependencies
    and heavy computing power requirements, then you may be better off using CaaS. Most FaaS services have severe limits for running time (15 minutes maximum for Lambda),
    computing power, memory size, disk space, and HTTP request and response limits. The upside to FaaS’ short execution times is that you only pay for the duration of the function.


    Install serverless OSS:

    $ sudo npm install -g serverless

    + Deploying Python Function to AWS Lambda

    Start by cloning the Serverless platform examples GitHub repository:
    The Python HTTP endpoint is defined in the file handler.py:

    $ git clone https://github.com/serverless/examples.git
    $ cd aws-python-simple-http-endpoint
    $ cd ~/.aws
    $ cat credentials
    $ export AWS_PROFILE=IAM_SES

    The Serverless platform uses a declarative approach for specifying the resources it needs to create with a YAML file
    called serverless.yaml. Here is file that declares a function called currentTime, corresponding to the Python function endpoint from the handler module defined previously:

    $ brew upgrade node
    $ sudo npm install -g serverless

    Modify the Python version to 3.7 in serverless.yaml:
        provider:
          name: aws
          runtime: python3.7

    Deploy the function to AWS Lambda by running the serverless deploy command:
    $ serverless deploy

    Test the deployed AWS Lambda function by hitting its endpoint with curl:
    handler: handler.endpoint events:

    $ curl https://3a88jzlxm0.execute-api.us-east-1.amazonaws.com/dev/ping

    Invoke the Lambda function directly with the serverless invoke command:
    $ serverless invoke --function currentTime

    Invoke the Lambda function directly and inspect the log (which is sent to AWS CloudWatch Logs) at the same time:
    $ serverless invoke --function currentTime --log

    One other thing we want to draw your attention to is the heavy lifting behind the scenes by the Serverless platform in the creation of AWS resources that are part of the Lambda setup. Serverless creates a CloudFormation stack called, in this case, aws-python-simple-http-endpoint-dev. You can inspect it with the aws CLI tool:
    $ aws cloudformation describe-stack-resources \
      --stack-name aws-python-simple-http-endpoint-dev
      --region us-east-1 | jq '.StackResources[].ResourceType'

Setup
-----
Install Minikube
Install kubectl
Install Helm


Start Minikube cluster
----------------------
minikube start


Connect docker CLI on Host to Docker Daemon inside Minikube
------------------------------------------------------------
eval $(minikube docker-env)
docker images

Do this step from any terminal that you will use


Build container:
-----------------
Update build.sh and then
./build.sh


Install the greetings helm chart:
---------------------------------
helm install greetings1 -n greetings1 --create-namespace ./greetings-chart --set NODE_PORT=32765 --set GREETING="This is greetings1"
helm install greetings2 -n greetings2 --create-namespace ./greetings-chart --set NODE_PORT=32764 --set GREETING="This is greetings2"


Query application endpoints:
----------------------------
URL1=`minikube service greetings -n greetings1 --url`
curl $URL1/greetings
curl $URL1/listcontents
curl $URL1/getk8sobjects

URL2=`minikube service greetings -n greetings2 --url`
curl $URL2/greetings
curl $URL2/listcontents
curl $URL2/getk8sobjects


Delete Helm releases:
----------------------
helm delete greetings1 -n greetings1
helm delete greetings2 -n greetings2


Use the plugins:
-----------------
export PATH=$PATH:`pwd`
kubectl greetings show greetings1
kubectl greetings show greetings2
kubectl greetings delete greetings1 greetings1
kubectl greetings delete greetings2 greetings2



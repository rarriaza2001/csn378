Setup
-----

1) Install Google Cloud CLI on your machine
   - Follow the instructions from: https://cloud.google.com/sdk/docs/install

2) Configure authentication for gcloud CLI. We need this step to create GKE cluster
   - gcloud auth login --> Follow the prompts (you will have to open browser window and paste the generated link,
       then paste the generated code in the verification field in your console.)
   - Create Project in Google Cloud Console --> Note down the Project ID. Remember that Project ID is different than the Project's Name.
       You will need Project ID in subsequent steps.
   - Set environment variables (Linux/MacOS use export command for this)
   - export PROJECT_ID=<Project-ID-from-previous-step>
   - export CLOUDSDK_COMPUTE_ZONE=us-central1-b
   - gcloud config set project ${PROJECT_ID}
   - If the first creation of project fails, you can use 
     - gcloud projects create <your-proposed-project-id>
   - gcloud auth configure-docker

3) Enable Google cloud billing account and enable Kubernetes Engine API for your project
   - https://console.cloud.google.com/billing
     Make sure that you provide correct billing address. It was observed that providing incorrect address
     can cause your account to get suspended.
   - https://console.cloud.google.com/apis/library/browse?filter=category:compute&project=<your-project-name>

4) Create GKE cluster
   - ./create-gke-cluster.sh <gcp-project-id> cluster1 

5) Once the cluster is created, you can open traffic to the ports on your cluster VM by following these steps:
   -  Go to VPC Network -> Firewall -> Select the rule that has following name:
      gke-cluster_name-<string of letters+numbers>-all
   -> Hit Edit
   -> In the Source IP ranges, enter: 0.0.0.0/0
   -> In the Specified protocols and ports -> in TCP, enter: 32760, 32761
   -> Hit Save

6) Download KubePlus kubectl plugins and setup the Path
   - wget https://github.com/cloud-ark/kubeplus/raw/master/kubeplus-kubectl-plugins.tar.gz
   - tar -zxvf kubeplus-kubectl-plugins.tar.gz
   - export KUBEPLUS_HOME=`pwd`
   - export PATH=$KUBEPLUS_HOME/plugins:$PATH
   - kubectl kubeplus commands 

7) Deploy KubePlus
   - KUBEPLUS_NS=default
   - wget https://raw.githubusercontent.com/cloud-ark/kubeplus/master/provider-kubeconfig.py
   - python3 -m venv venv
   - source venv/bin/activate
   - pip3 install -r requirements.txt
   - apiserver=`kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}'`
   - python3 provider-kubeconfig.py -s $apiserver -x cluster1 create $KUBEPLUS_NS
   - deactivate

8) Build container and push to GCR
   - Update build.sh and then
   - ./build.sh

9) Create the Greeting Kind:
   1. Update greetings-service-composition.yaml (see assignment requirements)
   2. kubectl upload chart <chart-tgz> kubeplus-saas-provider.json
   2. kubectl create -f greetings-service-composition.yaml --kubeconfig=kubeplus-saas-provider.json
   3. Verify that the Kind has been registered
      - kubectl get resourcecompositions
      - kubectl get crds

10) Retrieve Greeting instance YAMLs:
    1. kubectl man Greeting -k kubeplus-saas-provider.json > greetings1.yaml
    2. kubectl man Greeting -k kubeplus-saas-provider.json > greetings2.yaml

11) Update greetings1.yaml and greetings2.yaml as required (see assignment requirements)

12) Create Greeting instances:
    1. kubectl create -f greetings1.yaml
    2. kubectl create -f greetings2.yaml

13) Verify Greeting instances:
    1. kubectl get greetings
    2. kubectl get ns

14) Access metrics endpoint:
    1. kubectl appmetrics show Greeting greetings1 kubeplus-saas-provider.json
    2. kubectl appmetrics show Greeting greetings2 kubeplus-saas-provider.json

15) Check and note the resources created by KubePlus:
    1. kubectl appresources Greeting greetings1 -k kubeplus-saas-provider.json
    2. kubectl appresources Greeting greetings2 -k kubeplus-saas-provider.json

16) (DO NOT RUN THIS BEFORE SUBMISSION; Use it only while you are developing/debugging;
     We need your application instances to be running for grading)  
    Delete application instances
    1. kubectl delete -f greetings1
    2. kubectl delete -f greetings2

APP URL:
---------
Include your metrics endpint app url


NOTE:
-----
Keep your GKE cluster running till we complete the grading. You can delete the cluster
after the grades are released.

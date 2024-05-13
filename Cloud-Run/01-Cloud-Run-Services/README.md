# Google Cloud Run Services

## Step-01: Introduction
1. Create a Cloud Run Service
2. Update Applications
3. Revision URLs
4. Traffic Splitting
5. Autoscaling
6. Implement all the above features using `gcloud run`

## Step-02: Create Service and Access it
- Go to Cloud Run -> Create Service
- **Deploy one revision from an existing container image:** stacksimplify/google-cloud-run:v1
- **Service Name:** myservice1
- **Authentication:** Allow unauthenticated invocations
- **Container port:** 80
- REST ALL LEAVE TO DEFAULTS
- Click on **CREATE**
```t
# Docker Image used
stacksimplify/google-cloud-run:v1

# Access Application on Browser
https://myservice1-czbx2i66ca-uc.a.run.app
```

## Step-03: Update Application - v2
- Go to Cloud Run -> myservice1 -> EDIT & DEPLOY NEW REVISION
- **Deploy one revision from an existing container image:** stacksimplify/google-cloud-run:v2
- **Serve this revision immediately:** CHECKED
- Click on **DEPLOY**
```t
# Docker Image used
stacksimplify/google-cloud-run:v2

# Access Application on Browser
https://myservice1-czbx2i66ca-uc.a.run.app
```

## Step-04: Cloud Run Revisions and Traffic Splitting
- Split Traffic between version 1 and version 2
- version-1: 50%
- version-2: 50%
```t
# Access Application on Browser
https://myservice1-czbx2i66ca-uc.a.run.app
```

## Step-05: Add Revision URLs
- Add Revision URLs
- **version-1:** myappv1
- **version-2:** myappv2
```t
# myappv1 Revision URL
https://myappv1---myservice1-czbx2i66ca-uc.a.run.app/

# myappv2 Revision URL
https://myappv2---myservice1-czbx2i66ca-uc.a.run.app/
```

## Step-06: Deploy V3 Application with Serve this revision immediately UNCHECKED
- Go to Cloud Run -> myservice1 -> EDIT & DEPLOY NEW REVISION
- **Deploy one revision from an existing container image:** stacksimplify/google-cloud-run:v3
- **Serve this revision immediately:** UNCHECKED
- Click on **DEPLOY**
```t
# Docker Image used
stacksimplify/google-cloud-run:v3

# Access Application on Browser 
https://myservice1-czbx2i66ca-uc.a.run.app
Observation: V2 version will be still serving
```
### Add Revision URL for V3
- **version-3:** myappv3
```t
# Access Application on Browser using Revision URL
https://myappv3---myservice1-czbx2i66ca-uc.a.run.app/
Observation: 
1. V2 version will be still serving
2. V3 is not live, can be tested using revision URL. 
```
### Traffic Split to V3: 10%
```t
# Access Application on Browser using Revision URL
https://myservice1-czbx2i66ca-uc.a.run.app/
Observation: 
1. V2 version will be serving 90%
2. V3 version will be serving 10% - Gradual Rollout
```

## Step-07: Traffic Splitting
- **version-1:** 33%
- **version-2:** 33%
- **version-3:** 34%
```t
# Access Application on Browser using Revision URL
https://myservice1-czbx2i66ca-uc.a.run.app/
Observation: Traffic splits between 3 versions
```

## Step-08: Verify Additional Tabs
- Verify Logs Tabs
- Verify Metrics Tabs
- Verify Security Tabs

## Step-09: Cloud Run Autoscaling 
- [Cloud Run Autoscaling](https://cloud.google.com/run/docs/configuring/min-instances)
- Discuss about the concepts
  - Minimum number of instances
  - Maximum number of instances
  - Cold Starts

## Step-10: gcloud: Create Google Cloud Run Service 
```t
# gcloud Project Settings
gcloud config list
PROJECT_ID=[YOUR-PROJECT-ID]
PROJECT_ID=kdaida123
REGION=us-central1
gcloud config set core/project $PROJECT_ID
gcloud config set run/region $REGION
gcloud config list

# Help
gcloud run services --help
gcloud run deploy --help

# List Cloud Run Services
gcloud run services list

# Create Google Cloud Run Service
gcloud run deploy myservice102 \
--image=stacksimplify/google-cloud-run:v1 \
--allow-unauthenticated \
--port=80 

# List Cloud Run Services
gcloud run services list

# Describe Cloud Run Service
gcloud run services describe myservice102 
```

## Step-11: gcloud: List and Describe Revisions
```t
# Help 
gcloud run revisions --help

# List Revisions
gcloud run revisions list

# Describe Revision
gcloud run revisions describe <Revision-Name> 
gcloud run revisions describe myservice102-00001-2rk 
```

## Step-12: gcloud: Update Application
```t
# Update Application 
gcloud run services update
gcloud run services update --help 

# Update Application 
gcloud run services update myservice102 --image=stacksimplify/google-cloud-run:v2

# List Revisions
gcloud run revisions list 

# Describe Revision
gcloud run revisions describe <Revision-Name> 
gcloud run revisions describe myservice102-00001-2rk 
```
## Step-13: gcloud: Update Traffic
```t
# Help
gcloud run services update-traffic --help

# List Revisions
gcloud run revisions list 

# Set Tags (Add Revision URLs)
gcloud run services update-traffic myservice102 \
--set-tags=myappv1=myservice102-00001-2rk,myappv2=myservice102-00002-xgl 

# Update Traffic - V1-50%, V2-50%
gcloud run services update-traffic myservice102 \
--to-revisions=myservice102-00001-2rk=50,myservice102-00002-xgl=50 

## 1. You can also refer to the current or future LATEST revision in --to-revisions by the string "LATEST". 
## 2. To set 10% of traffic to always float to the latest revision:
gcloud run services update-traffic myservice102 \
--to-revisions=myservice102-00001-2rk=100,myservice102-00002-xgl=0 
gcloud run services update-traffic myservice102 --to-revisions=LATEST=10 

# To assign 100% of traffic to the current or future LATEST revision run
gcloud run services update-traffic myservice102 --to-latest 
```

## Step-14: gcloud: Delete Cloud Run Service
```t
# List Cloudn Run Services
gcloud run services list 

# Delete Cloud Run Service
gcloud run services delete myservice102 
gcloud run services delete myservice1
```


## Docker Images
- [stacksimplify/google-cloud-run:v1](https://hub.docker.com/repository/docker/stacksimplify/google-cloud-run/tags)
- [stacksimplify/google-cloud-run:v2](https://hub.docker.com/repository/docker/stacksimplify/google-cloud-run/tags)
- [stacksimplify/google-cloud-run:v3](https://hub.docker.com/repository/docker/stacksimplify/google-cloud-run/tags)

# Docker Image


## Step-01: Build, Tag and Push Docker Image
```t
# Build Docker Image
docker build -t google-cloud-run-job-demo1 .

# Tag Docker Image
docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]
docker tag google-cloud-run-job-demo1:latest stacksimplify/google-cloud-run-job-demo1:1.0.0

# Push Docker Image
docker login
docker push stacksimplify/google-cloud-run-job-demo1:1.0.0
```

## Temp
```t
docker build -t google-cloud-run-job-demo2-screenshot .
docker tag google-cloud-run-job-demo2-screenshot:latest stacksimplify/google-cloud-run-job-demo2-screenshot:1.0.0
docker push stacksimplify/google-cloud-run-job-demo2-screenshot:1.0.0
```


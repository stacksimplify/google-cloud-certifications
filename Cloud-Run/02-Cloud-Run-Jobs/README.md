# Cloud Run Jobs

## Step-01: Introduction
- Demo-1: Create very basic Cloud Run Job
- Demo-2: Create a advanced Cloud Run Job demo 
  - Uses Cloud IAM
  - Uses Cloud Storage Buckets
  - Create demo using gcloud commands
  - Also Schedule the Job using Triggers

## Step-02: Create Cloud Run Job
- Go to Cloud Run -> Create Job
- **Container Image URL:** stacksimplify/google-cloud-run-job-demo1:1.0.0
- **Job Name:** google-cloud-run-job-demo1
- **Region:** us-central1
- **Number of Tasks:** 10
- REST ALL LEAVE TO DEFAULTS
- Click on **Create**
```t
# Docker Images
stacksimplify/google-cloud-run-job-demo1:1.0.0
```

## Step-03: Review and Execute Job
- Go to Cloud Run -> Jobs -> google-cloud-run-job-demo1
- Click on **Execute**
- Review **Tasks** and **Logs**

## Step-04: Update Job
- Click on **EDIT** to update job

## Step-05: Screenshot Job
- [Review Screenshot Job](https://github.com/GoogleCloudPlatform/jobs-demos/tree/main/screenshot)
- Google Service we use
- IAM Service Account
- Cloud Storage Buckets
- Cloud Run Jobs


## Step-06: gcloud: Setup Project and Region
```t
# Project Config
PROJECT_ID=[YOUR-PROJECT-ID]
REGION=us-central1
gcloud config set core/project $PROJECT_ID
gcloud config set run/region $REGION
```

## Step-09: gcloud: Create IAM Service Account and Associate Cloud Storage Admin role
```t
# Create IAM Service Account for a Job to upload screenshots to Cloud Storage 
gcloud iam service-accounts create screenshot-sa --display-name="Screenshot app service account"

# Grant the service account permissions to access Cloud Storage
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --role roles/storage.admin \
  --member serviceAccount:screenshot-sa@$PROJECT_ID.iam.gserviceaccount.com 
```

## Step-10: Create Cloud Run Jobs
```t
# Command Help
gcloud run jobs --help

# Create Cloud Run Job
gcloud run jobs create screenshot-demo2 \
  --image=stacksimplify/google-cloud-run-job-demo2-screenshot:1.0.0 \
  --args="https://www.stacksimplify.com" \
  --args="https://github.com/stacksimplify" \
  --tasks=2 \
  --task-timeout=5m \
  --set-env-vars=BUCKET_NAME=screenshot-$PROJECT_ID \
  --service-account=screenshot-sa@$PROJECT_ID.iam.gserviceaccount.com
  
# List Cloud Run Jobs
gcloud run jobs list

# Review Container Arguments on Cloud Run console
1. Go to Cloud Run -> Jobs -> screenshot-demo2 -> EDIT
2. Verify "Container Arguments" section
```

## Step-11: gcloud: Execute Cloud Run Job and Verify
```t
# Cloud Run Jobs - Execute Job
gcloud run jobs execute JOB-NAME
gcloud run jobs execute screenshot-demo2

# Describe Job Execution
gcloud run jobs executions describe <EXECUTION_NAME>
gcloud run jobs executions describe screenshot-demo2-w4gtf

# Describe Task from a Job
gcloud run jobs executions tasks describe screenshot-demo2-w4gtf-task0
gcloud run jobs executions tasks describe screenshot-demo2-w4gtf-task1
```
## Step-12: gcloud: Update Cloud Run Job
```t
# Update Job
gcloud run jobs update screenshot-demo2 \
  --args="https://github.com/stacksimplify/aws-eks-kubernetes-masterclass" \
  --tasks=1

# Execute Job
gcloud run jobs execute screenshot-demo2
```

## Step-13: Schedule a Job
```t
# Enable Cloud Scheduler
gcloud services enable cloudscheduler.googleapis.com

# ADD SCHEDULE TRIGGER
- Go to Cloud Run -> Jobs -> screenshot-demo2 -> TRIGGERS
- Name: screenshot-demo2-scheduler-trigger
- Region: us-central1
- Frequency: */5 * * * *  (Runs every 5 minutes)
- Timezone: Select accordingly
- Click on CONTINUE
- Service Account: Compute Engine default service account
- CREATE

# WAIT FOR 10MINUTES
- Verify if the jobs executed automatically
```

## Docker Images used
- [stacksimplify/google-cloud-run-job-demo1:1.0.0](https://hub.docker.com/r/stacksimplify/google-cloud-run-job-demo1/tags)
- [stacksimplify/google-cloud-run-job-demo2-screenshot:1.0.0](https://hub.docker.com/r/stacksimplify/google-cloud-run-job-demo2-screenshot/tags)

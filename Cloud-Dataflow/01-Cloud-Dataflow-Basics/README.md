# Cloud Dataflow - Batch Job

## Step-01: Introduction
- Create a simple Batch Job
- Batch Job: Will run to completion
- Stream Job: Runs continuously
- **Pre-requisite:** Create Cloud Storage Bucket 


## Step-02: Create a Job from template
- Go to Dataflow -> Create job from template
- **Job name:** wordcount-batch-job
- **Regional endpoint:** us-central1
- **Dataflow template:** Word count
- **Required Parameters**
  - **Input Files in Cloud Storage:** gs://dataflow-samples/shakespeare/kinglear.txt
  - **Output Cloud Storage file prefix:** gs://mybucket1071/wordcounts/
  - **Temporary location:** gs://mybucket1071/wordcountstemp/
- Click on **RUN JOB**

## Step-03: Verify the following
- Go to Dataflow -> Jobs -> wordcount-batch-job 
- Job Graph
- Execution Details 
- Job Metrics
- Cost
- Logs

## Step-04: Verify the output in Cloud Storage Bucket
- Go to Cloud Storage -> mybucket1021 -> wordcounts
- Review output file


## Step-05: gcloud: Dataflow commands
```t 
# List Jobs
gcloud dataflow jobs list

# Describe Job
gcloud dataflow jobs describe JOB_ID
```

## Step-06: Review kinglear.txt file
```t
# Access it on browser
https://storage.googleapis.com/dataflow-samples/shakespeare/kinglear.txt

# Download kinglear.txt
gcloud storage cp gs://dataflow-samples/shakespeare/kinglear.txt .
```
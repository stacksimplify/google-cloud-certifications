# Cloud Functions - Cloud Storage Trigger

## Step-01: Introduction
- Create Cloud Storage Bucket
- Create Cloud Function with Cloud Storage Events Trigger

## Step-02: Create Cloud Storage Bucket
- Go to Cloud Storage -> CREATE 
- **Name your bucket:** mycfdemobucket1021 (Should be unique in google cloud)
- REST ALL LEAVE TO DEFAULTS
- Click CREATE


## Step-03: Create Cloud Function with Cloud Storage Event Trigger
- Go to Cloud Functions -> CREATE
### 1. Configuration Tab
- **Environment:** 2nd gen
- **Function name:** cf-demo3-events-storage
- **Region:** us-central1
- **Trigger:** Cloud Storage
- **Event Type:** google.cloud.storage.object.v1.finalized (Object created or updated)
- **BUCKET:** mycfdemobucket1021
- Click on **MORE OPTIONS** and review the settings
```t
# Warning message
Service account(s) might not have enough permissions to deploy the function with selected trigger. To mitigate potential errors, you can grant them the following roles:
roles/eventarc.eventReceiver to 1057267725005-compute@developer.gserviceaccount.com

# Add role
Click on GRANT ALL
```
- REST ALL LEAVE TO DEFAULTS
- Click to **NEXT**
### 2. Code Tab
- **Runtime:** Nodejs20 (default as on today)
- LEAVE THE AUTO-POPULATED CODE AS-IS. 
- JUST REVIEW THE CODE and Click on **DEPLOY**
```javascript
const functions = require('@google-cloud/functions-framework');

// Register a CloudEvent callback with the Functions Framework that will
// be triggered by Cloud Storage.
functions.cloudEvent('helloGCS', cloudEvent => {
  console.log(`Event ID: ${cloudEvent.id}`);
  console.log(`Event Type: ${cloudEvent.type}`);

  const file = cloudEvent.data;
  console.log(`Bucket: ${file.bucket}`);
  console.log(`File: ${file.name}`);
  console.log(`Metageneration: ${file.metageneration}`);
  console.log(`Created: ${file.timeCreated}`);
  console.log(`Updated: ${file.updated}`);
});
```

## Step-04: Review Cloud Function Logs
- Go to Cloud Function -> cf-demo2-events-storage -> Logs

## Step-05: Cloud Storage: Upload New File 
- Go to Cloud Storage -> Upload a file -> myfile1.txt
- Go to Cloud Function -> cf-demo2-events-storage -> Logs

## Step-06: Cloud Storage: Upload updated file
- Go to Cloud Storage -> Upload a file -> myfile1.txt
- Go to Cloud Function -> cf-demo2-events-storage -> Logs

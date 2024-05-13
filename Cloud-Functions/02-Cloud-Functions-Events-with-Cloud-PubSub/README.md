# Cloud Functions - Cloud Pub/Sub Trigger

## Step-01: Introduction
- Create Cloud Pub/Sub Topic
- Create Cloud Function with Cloud Pub/Sub Events Trigger

## Step-02: Create Cloud Pub/Sub Topic
- Go to Cloud Pub/Sub -> CREATE TOPIC
- **Topic ID:** mytopic1
- REST ALL LEAVE TO DEFAULTS
- Click CREATE
- Review Pub/Sub Topics and Subscriptions
  - Review Topic
  - Review Subscription

## Step-03: Create Cloud Function with Cloud Pub/Sub Event Trigger
- Go to Cloud Functions -> CREATE
### 1. Configuration Tab
- **Environment:** 2nd gen
- **Function name:** cf-demo2-events-pubsub
- **Region:** us-central1
- **Trigger:** Cloud Pub/Sub
- **Cloud Pub/Sub Topic:** mytopic1
- Click on **MORE OPTIONS** and review the settings
- REST ALL LEAVE TO DEFAULTS
- Click to **NEXT**
### 2. Code Tab
- **Runtime:** Nodejs20 (default as on today)
- LEAVE THE AUTO-POPULATED CODE AS-IS. 
- JUST REVIEW THE CODE and Click on **DEPLOY**
```javascript
const functions = require('@google-cloud/functions-framework');

// Register a CloudEvent callback with the Functions Framework that will
// be executed when the Pub/Sub trigger topic receives a message.
functions.cloudEvent('helloPubSub', cloudEvent => {
  // The Pub/Sub message is passed as the CloudEvent's data payload.
  const base64name = cloudEvent.data.message.data;

  const name = base64name
    ? Buffer.from(base64name, 'base64').toString()
    : 'World';

  console.log(`Hello, ${name}!`);
});
```

## Step-04: Review Cloud Function Logs
- Go to Cloud Function -> cf-demo2-events-pubsub -> Logs

## Step-05: Publish Messages in Cloud Pub/Sub Topic
- Go to Cloud Pub/Sub -> mytopic1 -> MESSAGES -> PUBLISH MESSAGE
- **Number of Messages:** 10
- **Message Body:** My Pub/Message
- Click on **PUBLISH**

## Step-05: Review Cloud Function Logs
- Go to Cloud Function -> cf-demo2-events-pubsub -> Logs

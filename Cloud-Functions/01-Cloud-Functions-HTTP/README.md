# Cloud Functions - HTTPS Trigger

## Step-01: Introduction
1. Create Cloud Function with HTTP Trigger
2. Access Cloud Function on browser and verify
3. Review all settings in Cloud Run
4. Edit Cloud Function to deploy v2.js file
5. Access Cloud Function on browser with v2 version and verify
6. Cloud Run Split Traffic between v1 and v2 and verify


## Step-02: Create Cloud Function with HTTPS Trigger
### 1. Configuration Tab
- Environment: 2nd gen
- Function name: cf-demo1-http
- Region: us-central1
- Trigger: HTTPS
- Authentication: Allow unauthenticated invocations
- REST ALL LEAVE TO DEFAULTS
- Click to **NEXT**
### 2. Code Tab
- Runtime: Nodejs20 (default as on today)
```javascript
const functions = require('@google-cloud/functions-framework');

functions.http('helloHttp', (req, res) => {
  //res.send(`Hello ${req.query.name || req.body.name || 'World 101'}!`);
  res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Cloud Functions Demo</title>
    </head>
    <body style="background-color: lightblue; color: black;">
      <h1>Welcome to Cloud Functions Demo</h1>
      <h2>Application Version: V1</h2>
    </body>
    </html>
  `);
});
```
- Review and **Deploy**


## Step-03: Access Application and Verify Cloud Run Service
```t
# Access using Auto-generated URL
https://us-central1-kdaida123.cloudfunctions.net/cloud-function-demo1-http

# Cloud Run Service
1. Go to Cloud Run Service -> cf-demo1-http
2. Review the "Revisions" Tab
```

## Step-04: Deploy V2 of Cloud Function
- Go to Cloud Functions -> cf-demo1-http -> EDIT
### 1. Configuration Tab
- Click to **NEXT**
### 2. Code Tab
- Runtime: Nodejs20 (default as on today)
- COPY the CODE and **Deploy**
```javascript
const functions = require('@google-cloud/functions-framework');

functions.http('helloHttp', (req, res) => {
  //res.send(`Hello ${req.query.name || req.body.name || 'World 101'}!`);
  res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Cloud Functions Demo</title>
    </head>
    <body style="background-color: lightyellow; color: black;">
      <h1>Welcome to Cloud Functions Demo</h1>
      <h2>Application Version: V2</h2>
    </body>
    </html>
  `);
});
```


## Step-05: Cloud Run - Revisions
- Go to Cloud Run -> cf-demo1-http -> Revisions -> Manage Traffic
  - V1 Revision: 50%
  - V2 Revision: 50%
- Test


---
title: GCP Google Cloud Platform - Synthetic Monitor Custom script
description: Learn to use Cloud Synthetic Monitor Custom script
---

## Step-01: Introduction
- Learn to use Cloud Synthetic Monitor Custom script

## Step-02: Synthetic Monitoring - Custom Script
- Go to Cloud Monitoring -> Detect -> Synthetic Monitoring -> **CREATE SYNTHETIC MONITOR**
- **Name:** synthetic-monitor-custom-script
- **Response timeout:** 30 seconds
- **Check Frequency:** 1 minute
### Cloud Function
- **Function name:** synthetic-monitor-custom-script-1
- **Region:** us-central1
- REST ALL LEAVE TO DEFAULTS
```js
// Copyright 2023 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

const { instantiateAutoInstrumentation, runSyntheticHandler } = require('@google-cloud/synthetics-sdk-api');
// Run instantiateAutoInstrumentation before any other code runs, to get automatic logs and traces
instantiateAutoInstrumentation();
const functions = require('@google-cloud/functions-framework');
const axios = require('axios');
const assert = require('node:assert');

functions.http('SyntheticFunction', runSyntheticHandler(async ({logger, executionId}) => {
  /*
   * This function executes the synthetic code for testing purposes.
   * If the code runs without errors, the synthetic test is considered successful.
   * If an error is thrown during execution, the synthetic test is considered failed.
   */
  logger.info('Making an http request using synthetics, with execution id: ' + executionId);
  const url = 'https://stacksimplify.com/'; // URL to send the request to
  return await assert.doesNotReject(axios.get(url));
}));
```
- Click on **APPLY FUNCTION**
### Alerts and notifications
- **Create Alert:** enable
- **Alert name:** synthetic failure custom script
- **Alert Duration:** 1 minute
- **Notification Channels:** gcpuser08
- Click on **CREATE**


## Step-03: Verify Cloud Function
- WAIT FOR 5 MINUTES FOR CLOUD FUNCTION TO GET DEPLOYED AND READY
- Go to Cloud Functions

## Step-04: Verify Synthetic monitor 
- Go to Cloud Monitoring -> Detect -> Synthetic Monitoring

## Step-05: Verify Alert Policies
- Go to Cloud Monitoring -> Detect -> Alerting -> Policies
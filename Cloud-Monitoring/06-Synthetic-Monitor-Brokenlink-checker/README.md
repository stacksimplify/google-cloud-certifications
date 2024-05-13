---
title: GCP Google Cloud Platform - Synthetic Monitor Brokenlink Checker
description: Learn to create Brokenlink Checker using  Cloud Synthetic Monitoring 
---

## Step-01: Introduction
- Learn to create Brokenlink Checker using  Cloud Synthetic Monitoring 

## Step-02: Synthetic Monitoring - Broken-link Checker Template
- Go to Cloud Monitoring -> Detect -> Synthetic Monitoring -> **CREATE SYNTHETIC MONITOR**
- **Name:** synthetic-monitor-brokenlink-checker
- **Response timeout:** 30 seconds
- **Check Frequency:** 1 minute
### URI configuration
- **ORIGIN URI:** https://stacksimplify.com
- REST ALL LEAVE TO DEFAULTS
### Cloud Function
- **Function name:** synthetic-monitor-brokenlink-checker-1
- **Region:** us-central1
- REST ALL LEAVE TO DEFAULTS
```js
// [START monitoring_synthetic_monitoring_broken_links_invocation]

const functions = require('@google-cloud/functions-framework');
const GcmSynthetics = require('@google-cloud/synthetics-sdk-broken-links');

const options = {
  origin_uri: 'https://stacksimplify.com',
  link_limit: 10,
  query_selector_all: 'a',
  wait_for_selector: '',
  get_attributes: ["href"],
  link_order: 'FIRST_N',
  link_timeout_millis: 30000,
  max_retries: 0,
  per_link_options: {
	},
  total_synthetic_timeout_millis: 60000,
  screenshot_options: {
		capture_condition: 'FAILING',
		storage_location: ''
	},
};

functions.http('BrokenLinkChecker', GcmSynthetics.runBrokenLinksHandler(options));
      
// [END monitoring_synthetic_monitoring_broken_links_invocation]
```
- Click on **APPLY FUNCTION**
### Alerts and notifications
- **Create Alert:** enable
- **Alert name:** synthetic failure mocha template
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


## Step-06: Clean-up
```t
# Delete Synthetic Monitors
Go to Cloud Monitroing -> Detect -> Synthetic Monitoring
1. synthetic-monitor-custom-script
2. synthetic-monitor-mocha-template
3. synthetic-monitor-brokenlink-checker

# Delete Cloud Functions
Go to Cloud Functions -> 
1. synthetic-monitor-custom-script-1
2. synthetic-monitor-mocha-template-1
3. synthetic-monitor-brokenlink-checker-1
```
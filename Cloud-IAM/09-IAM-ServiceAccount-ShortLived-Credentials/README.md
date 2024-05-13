---
title: Google Cloud IAM - Service Accounts - Short-lived credentials
description: Learn to create Cloud IAM Service Accounts Short-lived credentials
---

## Step-01: Introduction
- Create Cloud IAM Service Accounts Short-lived credentials 

## Step-02: Configure Cloud Shell gcloud with Normal user
```t
# Lists accounts whose credentials have been obtained using gcloud init
gcloud auth list

# Authorize with a user account without setting up a configuration.
gcloud auth login

# Lists accounts whose credentials have been obtained using gcloud init
gcloud auth list
```

## Step-03: Assign/Verify Service Account Token Creator Role to Normal User
```t
# Assign Service Account Token Creator Role
Normal User: gcpuser08@gmail.com
Role-1: Compute Viewer
Role-2: Service Account Token Creator
```

## Step-04: Create Service Account with required roles
```t
# Create Service Account with required roles
Service Account: mystorageadmin101@gcplearn9.iam.gserviceaccount.com 
Role-1: Service Account User
Role-2: Storage Admin
```

## Step-05: Create Access Token using gcloud auth print-access-token 
- **Default Access Token lifetime:** 3600 seconds
```t
# Lists accounts whose credentials have been obtained using gcloud init
gcloud auth list
Observation: Ensure you are using the normal user gcpuser08@gmail.com

# Set Environment Variables
PROJECT_ID="gcplearn9"
BUCKET_NAME="kalyanbucket201"
REGION="us-central1"
SA_NAME="mystorageadmin101@gcplearn9.iam.gserviceaccount.com"

# Create Access Token
ACCESS_TOKEN="$(gcloud auth print-access-token --impersonate-service-account=$SA_NAME)"
echo $ACCESS_TOKEN
```

## Step-06: Create Cloud Storage Bucket
```t
# Create Cloud Storage Bucket
curl -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "'"$BUCKET_NAME"'",
           "location": "'"$REGION"'"
         }' \
     "https://storage.googleapis.com/storage/v1/b?project=$PROJECT_ID"

# Verify the bucket
Goto -> Cloud Storage -> Buckets 
Observation: New bucket should be created     
```

## Step-07: Create OAuth Token with configurable lifetime for the access time
```t
# Set Environment Variables
PROJECT_ID="gcplearn9"
BUCKET_NAME="kalyanbucket202"
REGION="us-central1"
SA_NAME="mystorageadmin101@gcplearn9.iam.gserviceaccount.com"

# oauthrequest.json: Create it on CloudShell
vi oauthrequest.json 
{
  "scope": [
    "https://www.googleapis.com/auth/cloud-platform"
  ],
  "lifetime": "600s"
}

# Create Access Token
curl -X POST \
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     -H "Content-Type: application/json; charset=utf-8" \
     -d @oauthrequest.json \
     "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/$SA_NAME:generateAccessToken"

# Obserevation:
1. OAuth Access Token is valid only for 600seconds (10minutes)     

## SAMPLE OUTPUT
{
  "accessToken": "ya29.c.c0AY_VpZjWQdMVeBE2HdfUeLItuy0UW36fBta_DctVXfcRnCKtHHTi4-WP3HKELIOrSEGZWXAcyL68xUt074GtjmkFHVaQQNCpJtraSn01vGz1tPyE5UcfK7Rn84OhJmx3oaE2Km81g3weT5pGiam-V0zC1C7am_3tKOy0JGwDsp8KU69zTlsQIm4qpsrVOXXEUrr9ZqrZvSTZiMWJcT8Hwq0dqrHnrOisgzCxyXVInTk05ZLIJlmU0CTwxllKcbpyJSNRsS-KyY08mmkaai46lFVeIKajo3JXoea2pfufzPDA80Y8eSLIckVPwJrQWHlJHtoYS1gGEFVmPSWtbfjybOT9h581jMBGGnbltmxq6Bj93bmnchWo53pT3tsnP81t7Iw-D0JiOtsbO4sqOaMFrDIkC_2q6XiTrNPbaPj_et4RSrfSC5B8a5zyPITc1YEZo87rPeXnYbhzZV9Boj0l5fY18J4jOOPJurSrchiMsIhF73DsMwkWWKb1hgOaIQ59nXW9kq2yfsuS6BHRUaAN0CeWJUdmTawY2SDcdLCol4Wr8IG_dHqlEmh-DTKjTDTkTBy1IvGZ-y7n9Gz9on5bBAbjzrbff_trhWtEzAPwXNN7OMhdSHJhH637DrB9RWrybqJnyBVtM3RyeMcQa1w8s1Viq0Y8cdYXbV8Ru2dxr0kU52Uk5kdviV5dIYMc2-pSmBMeluksVzXse0rlYRfIr4JbQcyWcI9ISOS-wiyQQY2eBf5y7cezz6p-vtr9v4X2VV-Z7Xrbu4OtMt6cSe7w-eo1j9Yxj3M_QxoitQ0fUfpx3SV6fRd08dWtVZO3-sxzFJzz3b0V_-nykQ4j32BeXJsXgeqr27WMYIWXgrUu_9s3ii6m-3SrVFSShuxl1yqzBf7hQBb49yfnFF3Rn_BW_hqM_ftI2_4f4_xOQfmchhhglpBh84s6SI93z9b7X8sbh3316iJUwfsufxnMqzStihF5gU5YIe1SkBjrxRczjXZMRZ0xopeF3px",
  "expireTime": "2024-04-18T06:15:44Z"
}

# Set Access Token from the above respone
OAUTH_ACCESS_TOKEN=ya29.c.c0AY_VpZjWQdMVeBE2HdfUeLItuy0UW36fBta_DctVXfcRnCKtHHTi4-WP3HKELIOrSEGZWXAcyL68xUt074GtjmkFHVaQQNCpJtraSn01vGz1tPyE5UcfK7Rn84OhJmx3oaE2Km81g3weT5pGiam-V0zC1C7am_3tKOy0JGwDsp8KU69zTlsQIm4qpsrVOXXEUrr9ZqrZvSTZiMWJcT8Hwq0dqrHnrOisgzCxyXVInTk05ZLIJlmU0CTwxllKcbpyJSNRsS-KyY08mmkaai46lFVeIKajo3JXoea2pfufzPDA80Y8eSLIckVPwJrQWHlJHtoYS1gGEFVmPSWtbfjybOT9h581jMBGGnbltmxq6Bj93bmnchWo53pT3tsnP81t7Iw-D0JiOtsbO4sqOaMFrDIkC_2q6XiTrNPbaPj_et4RSrfSC5B8a5zyPITc1YEZo87rPeXnYbhzZV9Boj0l5fY18J4jOOPJurSrchiMsIhF73DsMwkWWKb1hgOaIQ59nXW9kq2yfsuS6BHRUaAN0CeWJUdmTawY2SDcdLCol4Wr8IG_dHqlEmh-DTKjTDTkTBy1IvGZ-y7n9Gz9on5bBAbjzrbff_trhWtEzAPwXNN7OMhdSHJhH637DrB9RWrybqJnyBVtM3RyeMcQa1w8s1Viq0Y8cdYXbV8Ru2dxr0kU52Uk5kdviV5dIYMc2-pSmBMeluksVzXse0rlYRfIr4JbQcyWcI9ISOS-wiyQQY2eBf5y7cezz6p-vtr9v4X2VV-Z7Xrbu4OtMt6cSe7w-eo1j9Yxj3M_QxoitQ0fUfpx3SV6fRd08dWtVZO3-sxzFJzz3b0V_-nykQ4j32BeXJsXgeqr27WMYIWXgrUu_9s3ii6m-3SrVFSShuxl1yqzBf7hQBb49yfnFF3Rn_BW_hqM_ftI2_4f4_xOQfmchhhglpBh84s6SI93z9b7X8sbh3316iJUwfsufxnMqzStihF5gU5YIe1SkBjrxRczjXZMRZ0xopeF3px

# Verify if OAUTH_ACCESS_TOKEN set
echo $OAUTH_ACCESS_TOKEN
```

## Step-06: Create Cloud Storage Bucket
```t
# Set Environment Variables
PROJECT_ID="gcplearn9"
BUCKET_NAME="kalyanbucket202"
REGION="us-central1"

# Create Cloud Storage Bucket
curl -X POST -H "Authorization: Bearer $OAUTH_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "'"$BUCKET_NAME"'",
           "location": "'"$REGION"'"
         }' \
     "https://storage.googleapis.com/storage/v1/b?project=$PROJECT_ID"

# Verify the bucket
Goto -> Cloud Storage -> Buckets 
Observation: 
1. New bucket should be created     
```

## Step-07: Other Shord-lived Credentials creation options
- [Generate OpenID Connect ID tokens](https://cloud.google.com/iam/docs/create-short-lived-credentials-delegated#sa-credentials-oidc)
- [Create a self-signed JSON Web Token (JWT)](https://cloud.google.com/iam/docs/create-short-lived-credentials-delegated#sa-credentials-jwt)
- [Create a self-signed blob](https://cloud.google.com/iam/docs/create-short-lived-credentials-delegated#sa-credentials-blob)

## Additional References
 - https://cloud.google.com/iam/docs/create-short-lived-credentials-direct
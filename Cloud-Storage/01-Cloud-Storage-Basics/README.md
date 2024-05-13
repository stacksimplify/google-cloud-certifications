# Cloud Storage Basics

## Step-01: Introduction
- Create and Manage Buckets
  - Using Web Console
  - Using gcloud commands

## Step-02: Web Console: Create and manage Cloud Storage Buckets
- Go to Cloud Storage -> Click on **CREATE**
- Name your bucket: mybucket1031
- Choose where to store your data: us(multiple regions in united states) (LEAVE TO DEFAULTS)
- Choose a storage class for your data: Set a default class (Standard) (LEAVE TO DEFAULTS)
- Choose how to control access to objects: Uniform (LEAVE TO DEFAULTS)
- Choose how to protect object data: None (LEAVE TO DEFAULTS)
- Click on CREATE
- Review the newly created bucket
### Bucket Settings
- OBJECTS
- CONFIGURATION
- PERMISSIONS
- PROTECTION
- LIFECYCLE
- OBSERVABILITY
- INVENTORY REPORTS

### Manage Objects in Bucket
- UPLOAD FILES
- UPLOAD FOLDERS
- CREATE FOLDER
- TRANSFER DATA
- DOWNLOAD
- DELETE


## Step-03: gcloud: Create and manage Cloud Storage Buckets
```t
# Set Project config
gcloud config set project VALUE
gcloud config set project mydatabases123

# Create Cloud Storage Bucket
gcloud storage buckets create gs://BUCKET_NAME
gcloud storage buckets create gs://mybucket1032

# List Cloud Storage Buckets
gcloud storage buckets list

# Describe Cloud Storage Bucket
gcloud storage buckets describe gs://mybucket1032

# Delete Cloud Storage Bucket (DONT DELETE)
gloud storage buckets delete gs://mybucket1032
```

## Step-04: Manage objects in Cloud Storage Buckets
```t
# List Buckets
gcloud storage ls

# Upload to Cloud Storage Buckets
cd Cloud-Storage/01-Cloud-Storage-Basics
gcloud storage cp myhtmlfiles/*.html gs://mybucket1032/myapp1

# List Files from a Bucket
gcloud storage ls BUCKET_NAME
gcloud storage ls gs://mybucket1032/myapp1

# Download from Cloud Storage Buckets
mkdir downloadfiles
gcloud storage cp gs://mybucket1032/myapp1/*.html downloadfiles/

# COPY Objects between two Cloud Storage Buckets
gcloud storage buckets create gs://mybucket1033
gcloud storage cp gs://mybucket1032/myapp1/*.html gs://mybucket1033/myapp1/
gcloud storage ls gs://mybucket1033/myapp1

# Move Command: Rename Objects with a given prefix to new prefix
gcloud storage mv gs://mybucket1032/myapp1 gs://mybucket1032/myapp2
gcloud storage ls gs://mybucket1032/myapp1 - Should fail
gcloud storage ls gs://mybucket1032/myapp2 - Should succeed

# cat: writes text files in a bucket to stdout 
gcloud storage cat gs://BUCKET_NAME/*.txt
gcloud storage cat gs://mybucket1032/myapp2/*.html

# Delete Objects in a Cloud Storage Bucket
gcloud storage ls gs://mybucket1032/myapp2
gcloud storage rm gs://mybucket1032/myapp2/v1-index.html
gcloud storage ls gs://mybucket1032/myapp2
```
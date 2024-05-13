# Google Cloud Firestore Fundamentals

## Step-01: Introduction
- Create a Firestore database using gcloud
- Import and Export Data using Web console and gcloud  

## Step-02: gcloud: Create Cloud Firestore Instance
```t
# Project Config
gcloud config set project PROJECT-ID
gcloud config set project gcplearn9

# Template: Create Firestore Database 
gcloud firestore databases create \
--database=DATABASE_ID \
--location=LOCATION \
--type=DATABASE_TYPE \

# Replace values: Create Firestore Database
gcloud firestore databases create \
--database=myfirestore2 \
--location=us-east1 \
--type=firestore-native
Additional Notes:
Two modes
1. firestore-native
2. datastore-mode

# List Databases
gcloud firestore databases list

# Describe Database
gcloud firestore databases describe --database=myfirestore2

# Update Database (Enable Point in time recovery)
gcloud firestore databases update --database=myfirestore2 --enable-pitr
```

## Step-03: Export Data
- **Export one or more collection groups:** apps
- **Destination:** myfirestore-exports-101
- Click on **EXPORT**

## Step-04: Import Data
- Go to Firestore -> myfirestore2 -> Import/Export -> IMPORT
- **Filename:** myfirestore-exports-101/FILE
- Click on **IMPORT**
- Go to **Data** and Verify

## Step-05: Export Data using gcloud from myfirestore1
```t
# Export Data
gcloud firestore export gs://mybucket1071/cliexport/ --collection-ids='apps' --database=myfirestore1

# Verify the export files in Cloud Storage Bucket
Go to Cloud Storage Bucket -> mybucket1071/cliexport/
```

## Step-06: Import Data using gcloud to myfirestore2
```t
# Delete Collection
Go to myfirstore2 -> Data -> Delete Collection -> apps

# Import Data to myfirestore2
gcloud firestore import gs://mybucket1071/cliexport --collection-ids='apps' --database=myfirestore2
```

## Step-07: List and Describe Operations using gcloud
```t
# List and Describe Operations to Get outputUriPrefix
gcloud firestore operations list --database=myfirestore1

# Describe Operations to Get outputUriPrefix
gcloud firestore operations describe <OPERATION-NAME>
gcloud firestore operations describe projects/kdaida123/databases/myfirestore1/operations/ASA5NmYxMmQ0NzNmOTctZTUxYi0xZGU0LThlY2MtNTJiMmM0N2UkGnNlbmlsZXBpcAkKMxI
```

## Step-08: Delete Firestore Databases
- Go to Firestore -> myfirestore1 -> DELETE
- Go to Firestore -> myfirestore2 -> DELETE
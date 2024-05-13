# Create BigQuery Dataset, Table, Load Data and Query 

## Step-01: Introduction
- Create new Dataset
- Create new Table and load data
- Run Queries using Google Cloud Console
- Run Queries using bq command line

## Step-02: Create New Dataset
- Go to BigQuery -> Analysis -> BigQuery Studio -> gcplearn9 -> Create Dataset
- **Dataset ID:** babynames
- REST ALL LEAVE TO DEFAULTS
- Click on **CREATE DATASET**

## Step-03: Create Table
- **Create table from:** Upload
- Select file: yob2014.txt
- File format: CSV
- DESTINATION:
  - Project: gcplearn9
  - Dataset: babynames
  - Table: names_1938
  - Table Type: Native table
- REST ALL LEAVE TO DEFAULTS
- Click on **CREATE TABLE**  

## Step-04: Query using Google Cloud Web Console
```t
# Query-1: Get records limit to 15
SELECT * FROM `gcplearn9.babynames.names_1938` LIMIT 15

# Query-2: Total Records Count
SELECT COUNT(*) FROM `gcplearn9.babynames.names_1938`
```

## Step-05: Query using bq cli using Google Cloud Shell
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Query-1: Get records limit to 15
bq query --nouse_legacy_sql \
'SELECT * FROM gcplearn9.babynames.names_1938 LIMIT 15'

# Query-2: Total Records Count
bq query --nouse_legacy_sql \
'SELECT COUNT(*) FROM gcplearn9.babynames.names_1938'   
```

## Step-06: Clean-Up / Delete
### Step-06-01: Delete Dataset
- Go to BigQuery -> Analysis -> BigQuery Studio -> gcplearn9 -> babynames -> DELETE
### Step-06-02: Delete Project
- Go to IAM -> Manage Resources -> Select Project -> gcplearn9
- DElETE Project

# Cloud Spanner Basics

## Step-01: Introduction
- Using google cloud web console
  - Create Cloud Spanner Instance 
  - Create Databases
  - Create Table
  - Insert Data
  - Query Data
- Using gcloud  
  - Create Cloud Spanner Instance 
  - Create Databases
  - Create Table
  - Insert Data
  - Query Data

## Step-02: Create Cloud Spanner Instance
- Go to Cloud Spanner -> **Create a Provisioned Instance**
- **Instance Name:** mycsinstance1
- **Instance ID:** mycsinstance1
- Click on **CONTINUE**
- **Choose Location:** Regional
- **Select a configuration:** us-central1
- Click on **CONTINUE**
- **Select Unit:** Nodes
- **Choose a scaling mode:** Autoscaling
  - **Minimum:** 1
  - **Maximum:** 3
- REST ALL LEAVE TO DEFAULTS
- Click on **CREATE**


## Step-03: Create Cloud Spanner Database
- Go to Cloud Spanner -> mycsinstance1 -> INSTANCE -> Overview -> **CREATE DATABASE**
- **Name your database:** mywebappdb
- **Select database dialect:** Google Standard SQL (leave to defaults)
- **Define your schema (optional):** 
  - Explore Options like DDL Templates, Shortcuts
```sql
# Create Table
CREATE TABLE myusers (
  userid INT64 NOT NULL,
  firstname STRING(1024),
  lastname  STRING(1024)
  ) PRIMARY KEY(userid);
```
- Click on **CREATE**



## Step-04: Load Data and Query Data
- Go to Cloud Spanner -> mycsinstance1 -> mywebappdb -> Overview Tab
- Go to Cloud Spanner -> mycsinstance1 -> mywebappdb -> Spanner Studio
```t
# Load/Insert Data into Table
INSERT INTO myusers (userid, firstname, lastname) VALUES
    (1, 'John', 'Doe'),
    (2, 'Jane', 'Smith'),
    (3, 'Alice', 'Johnson'),
    (4, 'Bob', 'Williams'),
    (5, 'Eva', 'Miller');

# Query Table
select * from myusers;
```

## Step-05: gcloud: Create Cloud Spanner Instance
```t
# Set Project 
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# To see the set of instance configurations that are available for your project:
gcloud spanner instance-configs list

# Create Cloud Spanner Instance
gcloud spanner instances create mycsinstance2 \
  --config=regional-us-central1 \
  --description="mycsinstance2" --nodes=1

# List Cloud Spanner Instances
gcloud spanner instances list

# Describe Cloud Spanner Instance
gcloud spanner instances describe mycsinstance2

# To set it as default Instance (OPTIONAL)
gcloud config set spanner/instance mycsinstance2

# Create Database in Cloud Spanner Instance: mycsinstance2
gcloud spanner databases create myappdb --instance=mycsinstance2 \
 --ddl='CREATE TABLE myapptable (appid INT64, appname STRING(1024)) PRIMARY KEY(appname)'

# List Databases
gcloud spanner databases list --instance=mycsinstance2

# Describe Databases
gcloud spanner databases describe myappdb --instance=mycsinstance2

# Write Data - Row-1
gcloud spanner rows insert --database=myappdb --instance=mycsinstance2 \
  --table=myapptable \
  --data=appid=1,appname=myapp1

# Write Data - Row-2
gcloud spanner rows insert --database=myappdb --instance=mycsinstance2 \
  --table=myapptable \
  --data=appid=2,appname=myapp2

# Write Data - Row-3  
gcloud spanner rows insert --database=myappdb --instance=mycsinstance2 \
  --table=myapptable \
  --data=appid=3,appname=myapp3

# Query-1: List all Records
gcloud spanner databases execute-sql myappdb \
  --instance=mycsinstance2 \
  --sql='SELECT * FROM myapptable'

# Query-2: WHERE appid=1
gcloud spanner databases execute-sql myappdb \
  --instance=mycsinstance2 \
  --sql='SELECT * FROM myapptable WHERE appid = 1'

# List Database Sessions
gcloud spanner databases sessions list --database=myappdb --instance=mycsinstance2  
```


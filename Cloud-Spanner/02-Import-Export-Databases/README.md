# Cloud Spanner Import/Export Databases

## Step-01: Introduction
- Export database from mycsinstance1
- Import database to mycsintance2 and verify
- In the process, the jobs for export and import will be created in Cloud Dataflow. We will review the whole process in detail.

## Step-02: Export mywebappdb from mycsinstance1
- **Pre-requisite:** Ensure Cloud Dataflow API is enabled
- Go to Cloud Spanner -> mycsinstance1 -> Import/Export -> Export
- Choose where to store your export: mycsbukcet101/mycsinstance1exports
- Choose a database to export: mywebappdb
- Choose a region for the export job: us-central1
- Click on **EXPORT**

## Step-03: Verify Cloud Dataflow Job for EXPORT
- Go to Cloud Dataflow -> Jobs -> cloud-spanner-export-mycsinstance1-mywebappdb
  - Job Graph
  - Execution Details
  - Logs -> SHOW
- Go to Compute Instances -> Verify if a Compute Instance created to complete this Dataflow job.
- Go to Cloud Spanner -> mycsintance1 -> Import/Export -> Verify if EXPORT is succeeded
- Go to  Cloud Storage -> Buckets -> mycsbucket101 -> mycsinstance1exports -> REVIEW EXPORTED Files

## Step-04: Import mywebappdb to mycsinstance2
- Go to Cloud Spanner -> mycsinstance1 -> Import/Export -> Import
- Choose a source: mycsbukcet101/mycsinstance1exports/mycsinstance1-mywebappdb-2024-01-27_18_27_11-7586062960548585929/
- Select database dialect: Google Standard SQL
- Name your database: mywebappdb (desired name)
- Choose a region for the import job: us-central1
- Click on **IMPORT**


## Step-05: Verify Cloud Dataflow Job for IMPORT
- Go to Cloud Dataflow -> Jobs ->  cloud-spanner-import-mycsinstance2-mywebappdb
  - Job Graph
  - Execution Details
  - Logs -> SHOW
- Go to Compute Instances -> Verify if a Compute Instance created to complete this Dataflow job.
- Go to Cloud Spanner -> mycsintance2 -> Import/Export -> Verify if IMPORT is succeeded

## Step-06: Verify mywebappdb in mycsintance2
- Go to Cloud Spanner -> mycsintance2 -> mywebappdb -> Spanner Studio
- Run Queries
```t
# Query Table
select * from myusers;
```


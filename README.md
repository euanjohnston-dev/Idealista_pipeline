# Data Ingestion and Load with DLT and Rapid API

## Technical Overview
This project focuses on extracting data from Idealista's API using the DLT package and Rapid API. The extracted data is then loaded into BigQuery via Cloud Storage.

- The DLT package can be taken to be performing the EtL from EtLT as it is directly unpacking the json in the destination with an infered schema.

## Connected REPOS
- DBT models to be executed as a separate cloud function (The T in EtLT):
- https://github.com/euanjohnston92-berlin/idealista_dbt_pipeline

- Gsheets checking pipeline (for manual verification of property duplicates)
- https://github.com/euanjohnston92-berlin/gsheets_check_pipeline

## Connected Documents
- Sample sheets checking file:
https://docs.google.com/spreadsheets/d/199qkCzNyFEOFWVZcBou1n4Fh-3x1vBVpUfPj_ElurlA

## Problem Statement
My partner and I are looking at potentially buying a home abroad and have struggled to cut through the noise to get useful buy side information. Whilst in our target area of Portugal the idealista site does provide a lot of good information unfortunately the site lists multiple duplicate properties making it hard to see the true depth of the market or run analysis on average property prices etc. 

## Solution
The series of transformations run highlight amongst other things potential duplicate listings to be checked. I have connected the output from the dbt model 'dim_duplicates_to_check.sql' to a gsheet which would then be uploaded to an further bigquery schema 'sheets_check' via an additional dlt pipeline. De-duplicating these listings allows for the core analysis to take place being the able to analyse accurately: 
1. Number of active unique listings.
2. Properties added and removed.
3. Number of multiple listed properties. 
4. Average price/sqm data.

I have analysed the output in a data studio dashboard:
https://lookerstudio.google.com/reporting/d13f508f-5101-49af-95bb-e0db1eb54483/page/p_0hgvz5kibd  

## Prerequisites
- Python
- DLT Package
- Rapid API Key
- Google Cloud Platform (GCP) Account

## Setup
1. Clone the repository.
2. Install the required dependencies: `pip install -r requirements.txt`
3. Obtain a Rapid API key and configure it.
4. Set up Google Cloud Storage and BigQuery.
5. Configure the Idealista.py script to your personal target area.
6. Setup a Gsheet to analyse and then re-upload the duplicates (I have done this via an additional dlt pipeline)

## Usage
1. The repo is setup to be run on cloud functions. 
2. Monitor Cloud Storage for ingested data.
3. Explore the loaded data in BigQuery and then whichever visualisation tool you choose to connect.

## Contributing and further development

- Idealista does not actively highlight the recent properties removed (assumed sold). This could be tracked via their api if that data was stored.
e.g from the output of the property id's saved from the properties/list api above use this list to periodically save the subsequent details from the properties/detail api. When message = "ad not found" -> assume sold (if combined with other listings).

This would be hugely valuable information as Portugal and in fact most of Europe does not have a multiple listng service.
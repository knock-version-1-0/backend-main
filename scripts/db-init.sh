#!/bin/bash

# Define variables
SQL_DIR=/sql/

# Loop through all .sql files in SQL_DIR and execute them using psql
for file in $SQL_DIR*.sql
do
  echo "Executing file: $file"
  psql -U $POSTGRES_USER -d $POSTGRES_DB -w -f $file
done

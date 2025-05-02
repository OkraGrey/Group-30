#!/bin/bash

# Check if the date parameter is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <YYYY-MM-DD>"
  exit 1
fi

# Extract year, month, and day from the input date
DATE=$1
YEAR=$(echo $DATE | cut -d'-' -f1)
MONTH=$(echo $DATE | cut -d'-' -f2)
DAY=$(echo $DATE | cut -d'-' -f3)

# Local paths (modify according to your actual data directory)
LOCAL_DATA_DIR="/home/hasnain_unix/myData/raw_data"
USER_LOG_FILE="${LOCAL_DATA_DIR}/${DATE}.csv"
METADATA_FILE="${LOCAL_DATA_DIR}/metadata.csv"

# Correct HDFS directories for Hive partitioning
HDFS_LOG_DIR="/raw/logs/year=${YEAR}/month=${MONTH}/day=${DAY}"
HDFS_METADATA_DIR="/raw/metadata"

# ---------------------- #
# 1. Upload User Log File
# ---------------------- #

# Create the HDFS directory for logs (partitioned by date)
echo "Creating HDFS directory: $HDFS_LOG_DIR"
hdfs dfs -mkdir -p "$HDFS_LOG_DIR"

# Upload the log file to HDFS
echo "Uploading $USER_LOG_FILE to $HDFS_LOG_DIR"
hdfs dfs -put -f "$USER_LOG_FILE" "$HDFS_LOG_DIR/"

# ------------------------- #
# 2. Upload Metadata (Once)
# ------------------------- #

# Check if metadata already exists in HDFS
if ! hdfs dfs -test -e "$HDFS_METADATA_DIR/metadata.csv"; then
    echo "Uploading metadata to $HDFS_METADATA_DIR"
    hdfs dfs -mkdir -p "$HDFS_METADATA_DIR"
    hdfs dfs -put "$METADATA_FILE" "$HDFS_METADATA_DIR/"
else
    echo "Metadata already exists in HDFS: $HDFS_METADATA_DIR"
fi

echo "Ingestion completed for date: $DATE"


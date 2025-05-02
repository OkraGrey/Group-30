import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Define output directory
output_dir = '/home/hasnain_unix/myData/raw_data'
os.makedirs(output_dir, exist_ok=True)

# ------------------------- #
# Generate User Activity Logs
# ------------------------- #

# Configuration
start_date = datetime(2023, 9, 1)
num_days = 7
actions = ['play', 'pause', 'skip', 'forward']
devices = ['mobile', 'desktop', 'tablet']
regions = ['US', 'EU', 'APAC']
user_ids = range(100, 200)
content_ids = range(1000, 1011)

# Generate data for each day
for day in range(num_days):
    current_date = start_date + timedelta(days=day)
    rows = []

    for _ in range(random.randint(20, 30)):
        row = {
            'user_id': random.choice(user_ids),
            'content_id': random.choice(content_ids),
            'action': random.choice(actions),
            'timestamp': current_date.strftime("%Y-%m-%d %H:%M:%S"),
            'device': random.choice(devices),
            'region': random.choice(regions),
            'session_id': f"S{random.randint(1000, 9999)}"
        }
        rows.append(row)

    # Convert to DataFrame
    df = pd.DataFrame(rows)

    # Save to CSV
    file_path = os.path.join(output_dir, f"{current_date.strftime('%Y-%m-%d')}.csv")
    df.to_csv(file_path, index=False)
    print(f"Generated file: {file_path}")

# ------------------------- #
# Generate Content Metadata
# ------------------------- #

metadata = [
    [1000, 'Summer Vibes', 'Pop', 180, 'DJ Alpha'],
    [1001, 'Rock Anthem', 'Rock', 240, 'The Beats'],
    [1002, 'Morning Podcast', 'Podcast', 3600, 'Talk Show'],
    [1003, 'Global News', 'News', 900, 'Anchor X'],
    [1004, 'Jazz Classics', 'Jazz', 300, 'Jazz Band'],
    [1005, 'Workout Hits', 'Pop', 200, 'Fit DJ'],
    [1006, 'Evening Relaxation', 'Jazz', 600, 'Calm Notes'],
    [1007, 'Chill Beats', 'Jazz', 400, 'Smooth Artist']
]

# Convert to DataFrame
df_metadata = pd.DataFrame(metadata, columns=['content_id', 'title', 'category', 'length', 'artist'])

# Save metadata to CSV
metadata_file_path = os.path.join(output_dir, "metadata.csv")
df_metadata.to_csv(metadata_file_path, index=False)
print(f"Generated metadata file: {metadata_file_path}")


import os

def get_csv_size_in_mb(file_path):
    # Get the file size in bytes
    file_size_bytes = os.path.getsize(file_path)
    
    # Convert bytes to megabytes
    file_size_mb = file_size_bytes / (1024 * 1024)
    
    return file_size_mb

paths = ["/Users/manavk/Documents/puppod/puppod-ml/dogs.csv", "/Users/manavk/Documents/puppod/puppod-ml/lifetime_stats.csv", "/Users/manavk/Documents/puppod/puppod-ml/sessions.csv"]
for path in paths:
    size_in_mb = get_csv_size_in_mb(path)
    print(f"Size of '{path}' is {size_in_mb:.2f} MB")
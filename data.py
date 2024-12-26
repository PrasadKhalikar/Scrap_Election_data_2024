import json

# Step 1: Load the data from the JSON file
file_path = "scraped_data.json"

with open(file_path, "r") as file:
    data = json.load(file)
    print("Original Data:")
    for entry in data:
        print(entry)

# Step 2: Keep only the desired indices
desired_indices = [0, 1, 2, 3, 15, 16, 28, 29, 30]
filtered_data = [[row[i] for i in desired_indices if i < len(row)] for row in data]

# Step 3: Save the filtered data back to the JSON file
with open(file_path, "w") as file:
    json.dump(filtered_data, file, indent=4)
    print("\nFiltered data saved to scraped_data.json")

# Step 4: Verify the filtered data
with open(file_path, "r") as file:
    loaded_data = json.load(file)
    print("\nFiltered Data:")
    for entry in loaded_data:
        print(entry)

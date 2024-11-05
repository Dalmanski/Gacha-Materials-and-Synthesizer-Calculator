# Define the materials dictionary
materials = {
    "Green": 123,
    "Blue": 12,
    "Purple": 21,
    "Yellow": 2
}

# Convert dictionary keys to a list
material_keys = list(materials.keys())

# Access the second material (index 1) and its value
index = 1  # Index for "Blue"
material_name = material_keys[index]  # Get the material name
material_value = materials[material_name]  # Get the corresponding value

# Print the material name and value
print(f"{material_name}: {material_value}")

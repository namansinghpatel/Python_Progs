import pickle

# Deserialize from a binary format
with open("data.pk1", "rb") as file:
    loaded_data = pickle.load(file)

print(
    loaded_data
)  # Output: {'name': 'Alice', 'age': 25, 'languages': ['English', 'Spanish']}

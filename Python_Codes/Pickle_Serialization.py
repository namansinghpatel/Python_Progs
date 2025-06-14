import pickle

data = {"name": "Alice", "age": 25, "languages": ["English", "Spanish"]}

# Serialize to a binary format
with open("data.pk1", "wb") as file:
    #pickle.dump(data, file)  # Writing binary serialized data

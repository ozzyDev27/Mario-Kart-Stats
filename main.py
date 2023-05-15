import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean
from nearpy import Engine
from nearpy.hashes import RandomBinaryProjections
from alive_progress import alive_it

# Load dataset
df = pd.read_csv("stats.csv")
df = df.drop(columns=["Unnamed: 0"])

N_ROWS = df.shape[0]

# Define the dimension of your vector space
dimension = 12

# Define the number of bits for the binary hash
num_bits = 10

# Create a list of vectors and their corresponding labels
print("Creating vectors...")
vectors = []
labels = []
for idx, row in alive_it(df.iterrows(), total=N_ROWS):
    vector = np.array(row[['GroundSpeed', 'WaterSpeed', 'AirSpeed', 'AntiGravitySpeed', 
                           'Acceleration', 'Weight', 'GroundHandling', 'WaterHandling', 
                           'AirHandling', 'AntiGravityHandling', 'Traction', 'MiniTurbo']])
    label = f"{row['Driver']}_{row['Vehicle']}_{row['Tire']}_{row['Glider']}"
    vectors.append(vector)
    labels.append(label)

# Create random binary hash with num_bits bits
print("Creating random binary hash...")
rbp = RandomBinaryProjections('rbp', num_bits)

# Create engine with pipeline configuration
print("Creating engine...")
engine = Engine(dimension, lshashes=[rbp])

print("Storing vectors...")
# Index the vectors in the engine with their corresponding labels
for vector, label in alive_it(zip(vectors, labels), total=N_ROWS):
    engine.store_vector(vector, label)

# Define the input stats to search for nearest neighbors
input_stats = np.array([100 for x in list(range(12))])

# Get nearest neighbors
print("Querying nearest neighbors...")
query = engine.neighbours(input_stats)

# Extract the labels of the nearest neighbors
nearest_labels = [result[1] for result in query]

# Parse the labels to extract the driver, vehicle, tire, and glider
nearest_drivers = [label.split("_")[0] for label in nearest_labels]
nearest_vehicles = [label.split("_")[1] for label in nearest_labels]
nearest_tires = [label.split("_")[2] for label in nearest_labels]
nearest_gliders = [label.split("_")[3] for label in nearest_labels]

# Print the nearest neighbors
for driver, vehicle, tire, glider in zip(nearest_drivers, nearest_vehicles, nearest_tires, nearest_gliders):
    print(f"Closest match: driver={driver}, vehicle={vehicle}, tire={tire}, glider={glider}")

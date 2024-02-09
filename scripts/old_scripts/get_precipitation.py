import re
import numpy as np
from sklearn.linear_model import LinearRegression

# Open the file and read the data
filename = "/data/trieHashimoto/th_experiment_data_3/logs/0225_setHead_100000_[0:10]_pop.txt"  # Replace with the name of your file
with open(filename, 'r') as f:
    lines = f.readlines()

# Extract the 'POPPED Hash' values and row indices
hash_values = []
row_indices = []
for i, line in enumerate(lines):
    match = re.search(r'POPPED Hash: (0x[0-9a-fA-F]+)', line)
    if match:
        hash_values.append(int(match.group(1), 16))
        row_indices.append(i)

# Convert the lists to NumPy arrays
X = np.array(row_indices).reshape(-1, 1)
y = np.array(hash_values).reshape(-1, 1)

# Create a LinearRegression object and fit the data
reg = LinearRegression().fit(X, y)

# Print the coefficients of the linear regression line
print('Slope:', reg.coef_[0][0])
print('Intercept:', reg.intercept_[0])
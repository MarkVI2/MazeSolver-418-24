import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import sys
from PIL import Image

import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()


from PySpice.Spice.NgSpice.Shared import NgSpiceShared
from PySpice.Probe.Plot import plot
from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
import itertools

# Load the Ngspice library



# from wand.image import Image

# def convert_png_to_pgm(input_file, output_file):
#     with Image(filename=input_file) as img:
#         img.format = 'pgm'
#         img.save(filename=output_file)

# input_file = 'input.png'
# output_file = 'output.pgm'

# convert_png_to_pgm(input_file, output_file)



from PIL import Image

# def rgb_to_grayscale(rgb):
#     r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
#     gray = (0.5 * r) + (0.5* g) + (0 * b)
#     return gray


# # Load the image
# img = Image.open('input.png')

# # Convert to a NumPy array
# np_img = np.array(img)

# # height, width =np_img.shape

# # Convert to grayscale
# grayscale_img = rgb_to_grayscale(np_img)

# # # Convert back to PIL Image
# # grayscale_img_pil = Image.fromarray(grayscale_img.astype(np.uint8))


# # # Save the grayscale image
# # grayscale_img_pil.save('grayscale_img_pil.png')



# # Set a upper and lower threshold value (e.g., 127)
# uthreshold = 200
# lthreshold = 50
# # Create a binary image
# binary_img = np.where((grayscale_img > lthreshold) & (grayscale_img < uthreshold), 255,  0)


# # Convert back to PIL Image
# binary_pil_img = Image.fromarray(binary_img.astype(np.uint8))

# # Save the binary image
# binary_pil_img.save('binary_image.png')


def get_neighbors(i, j, rows, cols, circuit_array):
    neighbors = ""
    for di, dj in itertools.product([-1, 0, 1], repeat=2):
        if di == 0 and dj == 0:
            continue
        ni, nj = i + di, j + dj
        if (0 <= ni < rows and 0 <= nj < cols and circuit_array[ni, nj] == 1):
            neighbors= f"{neighbors},{ni}_{nj}".lstrip(",")
  #  return (f"circuit.R({i}_{j}, "{i}_{j}",,100@u_Ohm)")


# Create a circuit
circuit = Circuit('Custom Circuit')

# Define the numpy array representing the circuit

np_arr = np.array(
    [[1,0,0,1,0],
    [1,1,0,1,0],
    [0,1,1,1,0],
    [0,0,1,1,0],
    [0,0,0,1,1]]
)

circuit_array = np_arr

#
rows, cols = circuit_array.shape


# Define a dictionary to hold the nodes of each wire
nodes_dict = {}


# Create a resistor for each 1 in the array
for i in range(rows):
    for j in range(cols):
            if circuit_array[i,j] == 1:
                # Create a resistor node for this position
                resistor_node = f"r{i}_{j}"
                nodes_dict[(i, j)] = resistor_node
                # Add the resistor to the circuit
                for neighbor_i, neighbor_j in [(i+1, j),(i, j+1)]:
                    if 0 <= neighbor_i < rows and 0 <= neighbor_j < cols and circuit_array[neighbor_i, neighbor_j] == 1:
                        a=f"n{neighbor_i}_{neighbor_j}"
                        circuit.R(resistor_node, f"n{i}_{j}",a,1@u_Ohm)
                        break
                                 

#connect the input to the top-left resistor
circuit.V("input", 'n0_0', circuit.gnd, 100@u_V)


# Connect the bottom-right resistor to the output
circuit.V("output", f"n{rows-1}_{cols-1}", circuit.gnd, 0@u_V)



print( "circuit with",rows,"rows and",cols,"cols  ")
print (circuit)

#Set up an analysis
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.operating_point()


for i in range(rows):
    for j in range(cols):
            if circuit_array[i,j] == 1:
                node = f"print(' V at {i}_{j}', analysis.n{i}_{j}[0], end='')"
                exec(node)
    print()

exit()




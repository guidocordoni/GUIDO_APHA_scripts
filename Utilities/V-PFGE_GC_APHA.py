import os
from Bio import SeqIO
from Bio.Restriction import EcoRI, BamHI, HindIII, EagI, SacII, SmaI, KpnI, XhoI, ApaI, NarI, ClaI, NotI, XbaI, SpeI, AvrII
import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import squareform  # Import squareform function

# Set seed for reproducibility
np.random.seed(42)

# Prompt the user to enter the folder containing DNA sequence FASTA files
folder_path = input("Enter the folder path containing DNA sequence FASTA files: ").strip()

# List of available enzymes
available_enzymes = [EcoRI, BamHI, HindIII, EagI, SacII, SmaI, KpnI, XhoI, ApaI, NarI, ClaI, NotI, XbaI, SpeI, AvrII]

print("Available enzymes:")
for i, enzyme in enumerate(available_enzymes, 1):
    print(f"{i}. {enzyme.__name__}")

# Prompt the user for enzyme selection
selected_enzyme_index = int(input("Enter the number corresponding to the enzyme you want to use: ")) - 1

# Check if the selected index is valid
if 0 <= selected_enzyme_index < len(available_enzymes):
    enzyme = available_enzymes[selected_enzyme_index]
    print(f"Selected enzyme: {enzyme.__name__}")
else:
    print("Invalid enzyme selection. Exiting.")
    exit(1)

# Function to perform in silico digestion and size estimation
def simulate_pfge(sequence, enzyme):
    fragments = enzyme.catalyze(sequence)
    fragment_sizes = [len(fragment) for fragment in fragments]
    return fragment_sizes

# Initialize a dictionary to store fragment sizes for each sequence
fragment_sizes_dict = {}

# Find the maximum fragment size in the dataset
max_fragment_size = 0

# Function to process a single DNA sequence
def process_sequence(filename):
    sequence_name = os.path.splitext(filename)[0]
    sequence_path = os.path.join(folder_path, filename)

    with open(sequence_path, "r") as fasta_file:
        dna_sequence = SeqIO.read(fasta_file, "fasta").seq

    fragment_sizes = simulate_pfge(dna_sequence, enzyme)
    
    return sequence_name, fragment_sizes

# Process each FASTA file in the folder in parallel
for filename in os.listdir(folder_path):
    if filename.endswith(".fasta") or filename.endswith(".fa"):
        sequence_name, fragment_sizes = process_sequence(filename)
        fragment_sizes_dict[sequence_name] = fragment_sizes

        # Update max_fragment_size if needed
        max_fragment_size = max(max_fragment_size, max(fragment_sizes, default=0))

# Pad fragment size lists to have the same length
for sequence_name in fragment_sizes_dict:
    fragment_sizes = fragment_sizes_dict[sequence_name]
    fragment_sizes += [0] * (max_fragment_size - len(fragment_sizes))

# Convert fragment sizes to a matrix for clustering
fragment_sizes_matrix = np.array(list(fragment_sizes_dict.values()))

# Calculate pairwise dice distances between sequences
# Note: dice distances are calculated based on presence/absence of fragments
dice_distances = pairwise_distances(fragment_sizes_matrix > 0, metric='dice')

# Convert to condensed distance matrix if it's not condensed
if np.any(np.triu(dice_distances, k=1)):
    dice_distances = squareform(dice_distances)

# Perform hierarchical clustering using the dice distances and ward linkage method
linkage_matrix = linkage(dice_distances, method='average')

# Reorder the data based on dendrogram clustering order
dendrogram_leaves = dendrogram(linkage_matrix, labels=list(fragment_sizes_dict.keys()), no_plot=True)
reordered_indices = dendrogram_leaves['leaves']
reordered_sequence_names = [list(fragment_sizes_dict.keys())[i] for i in reordered_indices]
fragment_sizes_matrix = fragment_sizes_matrix[reordered_indices]

# Create a virtual gel
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Plot fragment sizes for each sequence
for i, (sequence_name, fragment_sizes) in enumerate(zip(reordered_sequence_names, fragment_sizes_matrix)):
    y_values = [i] * len(fragment_sizes)
    ax1.scatter(fragment_sizes, y_values, marker='|', s=100, alpha=0.8)

ax1.set_xlabel("Fragment Size (bp)")
ax1.set_yticks(range(len(reordered_sequence_names)))  # Show strain names on the y-axis
ax1.set_yticklabels(reordered_sequence_names)  # Set strain names as y-axis labels
ax1.set_title("Virtual PFGE Simulation")
ax1.grid(axis='x', linestyle='--', alpha=0.6)

# Plot the dendrogram on the right
dendrogram(linkage_matrix, labels=reordered_sequence_names, orientation='right', ax=ax2, leaf_font_size=8, color_threshold=0.5)
ax2.set_title('Dendrogram (dice)')
ax2.set_xlabel('Distance')
ax2.set_yticks([])

# Show the plot
plt.tight_layout()
plt.show()

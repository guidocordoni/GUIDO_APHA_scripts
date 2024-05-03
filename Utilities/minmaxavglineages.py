import pandas as pd
'''This script calculates the min, max and avg snp distances within and between lineages that you can visually see on a phylogenetic tree.
how to use it :
1) create different files called lineage_A.txt, lineage_B.txt etc. The list of isolates are taken from what you see on the tree. If you are using microreact there is the possibility to select isolates within the lineage and export the metadata. You will need to have a one column files with the header called FILE
2) Adjust input lineage files and snp-dists matrix below (notr the #comments)
3 your results will ve in distance_results.csv file.

I suggest to put this script the lineages files and the snp-dists file in the same folder, so running the file with the command 
python minmaxavglineages.py you will have all in the same folder.''' 

def read_isolates_list(lineage_file):
    with open(lineage_file, 'r') as file:
        isolates = [line.strip() for line in file]
    return isolates

def calculate_distance(matrix, isolates_list1, isolates_list2=None):
    distances = []
    if isolates_list2 is None:  # Calculate within-lineage distances
        for i in range(len(isolates_list1)):
            for j in range(i + 1, len(isolates_list1)):
                isolate_i = isolates_list1[i]
                isolate_j = isolates_list1[j]
                if isolate_i in matrix.index and isolate_j in matrix.columns:
                    distance = matrix.loc[isolate_i, isolate_j]
                    distances.append(distance)
    else:  # Calculate between-lineage distances
        for isolate1 in isolates_list1:
            for isolate2 in isolates_list2:
                if isolate1 in matrix.index and isolate2 in matrix.columns:
                    distance = matrix.loc[isolate1, isolate2]
                    distances.append(distance)
    return distances

def main():
    lineages = ['A', 'B'] # Add or remove lineages here
    similarity_matrix_file = "your_snp-dists_matrix.tsv" # This is your snp-dists matrix
    similarity_matrix = pd.read_csv(similarity_matrix_file, index_col=0, delimiter='\t')

    within_lineage_distances = {}
    between_lineage_distances = {}

    # Calculate distances within each lineage
    for lineage in lineages:
        lineage_file = f"lineage_{lineage}.txt"
        isolates_list = read_isolates_list(lineage_file)
        distances_within = calculate_distance(similarity_matrix, isolates_list)
        within_lineage_distances[lineage] = distances_within

    # Calculate distances between lineages
    for i in range(len(lineages)):
        for j in range(i + 1, len(lineages)):
            lineage_i = lineages[i]
            lineage_j = lineages[j]
            isolates_i = read_isolates_list(f"lineage_{lineage_i}.txt")
            isolates_j = read_isolates_list(f"lineage_{lineage_j}.txt")
            distances_between = calculate_distance(similarity_matrix, isolates_i, isolates_j)
            between_lineage_distances[(lineage_i, lineage_j)] = distances_between

    # Calculate statistics for between-lineage distances
    results_between = []
    for (lineage_i, lineage_j), distances in between_lineage_distances.items():
        if distances:
            min_distance_between = min(distances)
            max_distance_between = max(distances)
            avg_distance_between = sum(distances) / len(distances)
            results_between.append((f"Between {lineage_i} and {lineage_j}", min_distance_between, max_distance_between, avg_distance_between))

    # Calculate statistics for within-lineage distances
    results_within = []
    for lineage, distances in within_lineage_distances.items():
        if distances:
            min_distance_within = min(distances)
            max_distance_within = max(distances)
            avg_distance_within = sum(distances) / len(distances)
            results_within.append((f"Within {lineage}", min_distance_within, max_distance_within, avg_distance_within))

    # Save results to CSV
    df_between = pd.DataFrame(results_between, columns=["Group", "Min Distance", "Max Distance", "Average Distance"])
    df_within = pd.DataFrame(results_within, columns=["Group", "Min Distance", "Max Distance", "Average Distance"])
    df = pd.concat([df_between, df_within], ignore_index=True)
    df.to_csv("results.csv", index=False)

if __name__ == "__main__":
    main()


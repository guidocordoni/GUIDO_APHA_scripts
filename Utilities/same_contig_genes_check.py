import pandas as pd
#Using results from Abricate search if AMR or virulence profiles are located on the same contig for each isolate. create a input table with columns SEQUENCE, GENE, %COVERAGE and save the file as .csv. Update the input and output below (see the #)

def check_contig_coverage_relationship(input_file, contig_gene_counts_output):
    # Read the input CSV file
    df = pd.read_csv(input_file)

    # Extract isolate and contig from the SEQUENCE column
    df[['Isolate', 'Contig']] = df['SEQUENCE'].str.split('_N', expand=True)

    # Group by isolate and contig, count unique genes
    contig_gene_counts = df.groupby(['Isolate', 'Contig'])['GENE'].nunique().reset_index()

    # Count total genes per isolate
    total_genes_per_isolate = df.groupby('Isolate')['GENE'].nunique().reset_index()

    # Merge contig_gene_counts with total_genes_per_isolate
    contig_gene_counts = pd.merge(contig_gene_counts, total_genes_per_isolate, on='Isolate', suffixes=('_contig', '_total'))

    # Calculate percentage of genes on the same contig for each isolate
    contig_gene_counts['Percentage_Same_Contig'] = (contig_gene_counts['GENE_contig'] / contig_gene_counts['GENE_total']) * 100

    # Check for missing genes in each isolate
    missing_genes = df.pivot_table(index='Isolate', columns='GENE', values='SEQUENCE', aggfunc='count').isnull().sum(axis=1).reset_index()
    missing_genes.columns = ['Isolate', 'Missing_Genes_Count']

    # Merge missing_genes with contig_gene_counts
    contig_gene_counts = pd.merge(contig_gene_counts, missing_genes, on='Isolate')

    # Save results to CSV
    contig_gene_counts.to_csv(contig_gene_counts_output, index=False)

if __name__ == "__main__":
    input_file = "yourinput.csv" #your input goes here
    contig_gene_counts_output = "youroutput.csv" #your output goes here
    check_contig_coverage_relationship(input_file, contig_gene_counts_output)



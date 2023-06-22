import gzip
import os
# This script is currently setted to take the first 1000 sequences from a set of fastq.gz sequences and save them in a folder (REDUCED_SEQ) creating fastq.gz files that have the same names of the original ones. You can modify the value 1000 below to the desidered number of sequences needed.
#Use this script to generate short sequences for testing pipelines or scripts on your personal SCE avoiding incurring in the costs of bigger SCE machines.
# Made by Guido Cordoni guido.cordoni@apha.gov.uk
def extract_first_1000_sequences(input_file, output_file):
  with gzip.open(input_file, "rb") as f_in:
    with gzip.open(output_file, "wb") as f_out:
      for i in range(1000):
        line = f_in.readline()
        f_out.write(line)

def main():
#Inssert your input and output folder here
  input_folder = "RAW_READS"
  output_folder = "REDUCED_SEQ"

  if not os.path.exists(output_folder):
    os.mkdir(output_folder)

  for input_file in os.listdir(input_folder):
    if input_file.endswith(".fastq.gz"):
      output_file = os.path.join(output_folder, input_file)
      extract_first_1000_sequences(os.path.join(input_folder, input_file), output_file)

if __name__ == "__main__":
  main()


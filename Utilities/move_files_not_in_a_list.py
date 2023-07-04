#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 13:58:57 2023

@author: guidocordoni
"""
import os
import shutil

def move_non_listed_files(directory, file_list_file, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)
    with open(file_list_file, 'r') as f:
        file_list = [line.strip() for line in f.readlines()]
    for filename in os.listdir(directory):
        if filename.endswith(".fasta") and filename not in file_list:
            source_path = os.path.join(directory, filename)
            destination_path = os.path.join(destination_folder, filename)
            shutil.move(source_path, destination_path)
            print(f"Moved file: {source_path} to {destination_path}")

# Example usage
directory_path = '/home/guidocordoni/fsx/ranch-52/PATHSAFE_raw_meat/fasta'
file_list_file = '/home/guidocordoni/Desktop/list.txt'
destination_folder = '/home/guidocordoni/fsx/ranch-52/PATHSAFE_raw_meat/fasta/not_meat'

move_non_listed_files(directory_path, file_list_file, destination_folder)

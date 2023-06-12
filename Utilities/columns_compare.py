import pyfiglet

graphic = pyfiglet.figlet_format("COLUMNS COMPARE V 1.0")
print(graphic)
print("This script will compare 2 columns in a list.txt file and will report:\n")
print("1) entries of the first column")
print("2) entries of the second column")
print("3) entries present in both columns")
print("4) entries present only in the first column")
print("5) entries present only in the second column\n")
print("Prepare a file containing values of the first and second columns (tab-spaced, no headline) and save it as list.txt")
print("Use list.txt as an argument (python columns_compare.py list.txt)\n")

def compare_entries(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"File {file_path} not found. Please provide a valid list.txt file.")
        return

    entries_master_list = []
    entries_folder = []

    for line in lines:
        columns = line.strip().split("\t")  # Assuming columns are separated by tabs

        if len(columns) >= 1:
            entry_master_list = columns[0]
            entries_master_list.append(entry_master_list)

        if len(columns) >= 2:
            entry_folder = columns[1]
            entries_folder.append(entry_folder)

    if not entries_master_list or not entries_folder:
        print("The file does not contain data in both columns.")
        return

    if len(entries_master_list) > len(entries_folder):
        entries_folder.extend([""] * (len(entries_master_list) - len(entries_folder)))

    print("Entries present in first column:")
    for entry in entries_master_list:
        print(entry)

    print("\nEntries present in second column:")
    for entry in entries_folder:
        print(entry)

    print("\nEntries present in both first and second column:")
    common_entries = set(entries_master_list) & set(entries_folder)
    for entry in common_entries:
        print(entry)

    print("\nEntries missing from first column:")
    missing_master_list = set(entries_folder) - set(entries_master_list)
    for entry in missing_master_list:
        print(entry)

    print("\nEntries missing from second column:")
    missing_folder = set(entries_master_list) - set(entries_folder)
    for entry in missing_folder:
        print(entry)


# Usage example
compare_entries("list.txt")


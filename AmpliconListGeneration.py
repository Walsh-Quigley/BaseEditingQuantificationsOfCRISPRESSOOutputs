import csv
import os

def create_common_amplicon_file():
    filename = "CommonAmpliconGeneration.csv"
    fieldnames = [
        "Name", "Protospacer_sequence", "Editor",
        "Guide Orientation relative to amplicon", "Amplicon", "note",
        "Tolerated Sequences", "Tolerated positions", "Intended Edits"
    ]

    start = input("Do you want to create the file 'CommonAmpliconGeneration.csv'? (yes/no): ").strip().lower()
    if start != 'yes':
        print("Alright, if any information is missing you will have an opportunity to correct it later.")
        return

    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        while True:
            row_data = {}
            for field in fieldnames:
                value = input(f"Enter value for '{field}': ").strip()
                print(f"{field}: {value}")
                row_data[field] = value

            writer.writerow(row_data)
            print("Row added successfully.")

            cont = input("Would you like to add another row? (yes/no): ").strip().lower()
            if cont != 'yes':
                print("Finished adding rows.")
                break






create_common_amplicon_file()
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


import csv
import os

def retrieveCRISPRessoInputs(search_term):
    csv_path = './../Common_amplicon_list.csv'
    rows = []
    updated = False

    guideSequence = ""
    ampliconSequence = ""
    guideOrientation = ""

    with open(csv_path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
            if row[0].upper() == search_term:
                guideSequence = row[1].upper().replace("\r", "").replace("-", "")[:20].strip()
                guideOrientation = row[3].upper().replace("\r", "").strip()
                ampliconSequence = row[4].upper().replace("\r", "").strip()

                if not guideSequence:
                    guideSequence = input(f"Missing guide sequence for {search_term}. Please enter it: ").strip().upper()[:20]
                    row[1] = guideSequence
                    updated = True

                if not guideOrientation:
                    guideOrientation = input(f"Missing guide orientation for {search_term}. Please enter it: ").strip().upper()
                    row[3] = guideOrientation
                    updated = True

                if not ampliconSequence:
                    ampliconSequence = input(f"Missing amplicon sequence for {search_term}. Please enter it: ").strip().upper()
                    row[4] = ampliconSequence
                    updated = True

                break

    if updated:
        with open(csv_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        print(f"CSV updated with new values for {search_term}.")

    print(f"Guide Sequence Variable: {guideSequence}")
    print(f"Amplicon Sequence Variable: {ampliconSequence}")
    print(f"Guide Orientation: {guideOrientation}")

    return guideSequence, ampliconSequence, guideOrientation

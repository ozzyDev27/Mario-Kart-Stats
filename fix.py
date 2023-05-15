import csv

# Open the input and output files
with open('stats.csv', 'r') as input_file, open('output.csv', 'w', newline='') as output_file:

    # Create CSV reader and writer objects
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)

    # Keep track of seen builds
    seen_builds = set()

    # Iterate over rows in the input file
    for row in reader:

        # Get the stats at the end of the row
        stats = tuple(row[-3:])

        # If we haven't seen these stats before, write the row to the output file and add the stats to seen_builds
        if stats not in seen_builds:
            writer.writerow(row)
            seen_builds.add(stats)

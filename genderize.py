from genderize import Genderize, GenderizeException
import csv
import sys
import os.path
import time

import jpyhelper as jpyh

def genderize():
    if len(sys.argv) != 3:
        print("Plrease specify input and output files: python genderize.py [input file path] [output file path]")
        sys.exit();

    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    filename, file_extension = os.path.splitext(sys.argv[2])
    ofile = filename + "_" + time.strftime("%Y%m%d-%H%M%S") + ".csv"
    print("\n--- Input file: " + dir_path + os.sep + sys.argv[1])
    print("--- Output file: " + dir_path + os.sep + ofile + "\n")

    csv.field_size_limit(sys.maxsize)

    #Initialize API key
    genderize = Genderize(
        user_agent='GenderizeDocs/0.0',
        api_key='')

    with open(sys.argv[1], encoding="utf8") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        names = []
        for row in readCSV:
            names.append(row)

        names.pop(0)

        print("--- Read CSV with " + str(len(names)) + " names")

        chunks = list(jpyh.splitlist(names, 10));

        print("--- Processed into " + str(len(chunks)) + " chunks")

        if jpyh.query_yes_no("\n---! Ready to send to Genderdize. Proceed?") == False:
            print("Exiting...\n")
            sys.exit()

        if os.path.isfile(ofile):
            if jpyh.query_yes_no("---! Output file exists, overwrite?") == False:
                print("Exiting...\n")
                sys.exit()
            print("\n")

        response_time = [];
        with open(ofile, 'w', newline='', encoding="utf8") as f:
            writer = csv.writer(f)
            writer.writerow(list(["names", "gender", "probability", "count"]))
            chunks_len = len(chunks)
            for index, chunk in enumerate(chunks):
                while True:
                    try:
                        start = time.time()
                        dataset = genderize.get(chunk)
                    except GenderizeException as e:
                        print("\n" + e)

                        if "response not in JSON format" in str(e):
                            if jpyh.query_yes_no("\n---! 502 detected, try again?") == True:
                                print("Exiting...\n")
                                pass
                            else:
                                break
                        print("\n---!! GenderizeException - You probably exceeded the request limit, please add or purchase a API key\n")
                        sys.exit()

                    response_time.append(time.time() - start)
                    print("Processed chunk " + str(index + 1) + " of " + str(chunks_len) + " -- Time remaining (est.): " + \
                        str( round( (sum(response_time) / len(response_time) * (chunks_len - index - 1)), 3)) + "s")

                    for data in dataset:
                        writer.writerow(data.values())
                    break

if __name__ == "__main__":
    genderize()

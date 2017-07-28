from genderize import Genderize, GenderizeException
import csv
import sys
import os.path
import time
import argparse
import logging

import jpyhelper as jpyh

def genderize(args):
    print(args)

    #File initialization
    dir_path = os.path.dirname(os.path.realpath(__file__))

    logging.basicConfig(filename=dir_path + os.sep + "log.txt", level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger=logging.getLogger(__name__)

    ofilename, ofile_extension = os.path.splitext(args.output)

    ofile = ofilename + "_" + time.strftime("%Y%m%d-%H%M%S") + ".csv"
    ifile = args.input

    if os.path.isabs(ifile):
        print("\n--- Input file: " + ifile)
    else:
        print("\n--- Input file: " + dir_path + os.sep + ifile)

    if os.path.isabs(ofile):
        print("--- Output file: " + ofile)
    else:
        print("--- Output file: " + dir_path + os.sep + ofile + "\n")

    #File integruty checking
    if not os.path.exists(ifile):
        print("--- Input file does not exist. Exiting.\n")
        sys.exit()

    if not os.path.exists(os.path.dirname(ofile)):
        print("--- Error! Invalid output file path. Exiting.\n")
        sys.exit()

    #Some set up stuff
    csv.field_size_limit(sys.maxsize)

    #Initialize API key
    if not args.key == "NO_API":
        print("--- API key: " + args.key + "\n")
        genderize = Genderize(
            user_agent='GenderizeDocs/0.0',
            api_key=args.key)
        key_present = True
    else:
        print("--- No API key provided.\n")
        key_present = False

    #Open ifile
    with open(ifile, 'r', encoding="utf8") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        names = []
        for row in readCSV: #Read CSV into names list
            names.append(row)

        names.pop(0) #Remove header

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
                        temp = []
                        if args.nostrip == True:
                            temp = chunk
                        else:
                            for c in chunk:
                                temp.append(str(c[0]).strip("\n"))


                        if key_present:
                            dataset = genderize.get(temp)
                        else:
                            dataset = Genderize().get(temp)
                    except GenderizeException as e:
                        #print("\n" + str(e))
                        logger.error(e)

                        #Error handling
                        if "response not in JSON format" in str(e) and args.catch == True:
                            if jpyh.query_yes_no("\n---!! 502 detected, try again?") == True:
                                print("Exiting...\n")
                                pass
                            else:
                                break
                        if "Invalid API key" in str(e) and args.catch == True:
                            print("\n---!! Error, invalid API key! Check log file for details.\n")
                            sys.exit()

                        print("\n---!! GenderizeException - You probably exceeded the request limit, please add or purchase a API key. Check log file for details.\n")
                        sys.exit()

                    response_time.append(time.time() - start)
                    print("Processed chunk " + str(index + 1) + " of " + str(chunks_len) + " -- Time remaining (est.): " + \
                        str( round( (sum(response_time) / len(response_time) * (chunks_len - index - 1)), 3)) + "s")

                    for data in dataset:
                        writer.writerow(data.values())
                    break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bulk genderize.io script')
    required = parser.add_argument_group('required named arguments')

    required.add_argument('-i','--input', help='Input file name', required=True)
    required.add_argument('-o','--output', help='Output file name', required=True)
    parser.add_argument('-k','--key', help='API key', required=False, default="NO_API")
    parser.add_argument('-c','--catch', help='Try to gracefully handle server 502 errors', required=False, action='store_true', default=True)
    parser.add_argument('-ns','--nostrip', help='Do not strip blank lines from input csv', required=False, action='store_true', default=False)

    genderize(parser.parse_args())

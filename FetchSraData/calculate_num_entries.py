
import sys
import math
#def main(args):
def main():

    percentage_spotsAvg = float(sys.argv[1])
    file_size = float(sys.argv[2])
    avgLength = int(sys.argv[3])
    if percentage_spotsAvg == 0:
        percentage_spotsAvg = 1
    if avgLength == 0:
        avgLength = 1
    size_run = (file_size * 1048576 * (percentage_spotsAvg/100) )
    num_entries = math.ceil(size_run/avgLength)
    print(num_entries)
    #return num_entries


if __name__ == "__main__":
    main()
    #main(sys.argv[1:])

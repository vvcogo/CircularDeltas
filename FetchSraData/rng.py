import random
import sys

def main():
    random.seed(int(sys.argv[1]))
    print(random.randint(0, int(sys.argv[2])))

if __name__ == "__main__":
    main()

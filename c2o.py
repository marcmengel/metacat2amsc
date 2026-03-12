import argparse
import configparser
from convert import convert

def main():
    p = argparse.ArgumentParser()
    p.add_argument("-c", help="Config file", default="c2o.ini")

    args = p.parse_args()

    config = configparser.ConfigParser()
    config.read(args.c)
    convert(config)

if __name__ == '__main__':
    main()

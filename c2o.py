import argparse
import configparser

def main():
    p = argparse.ArgumentParser()
    p.add_argument("-c", description="Config file", default="c2o.ini")

    args = p.parse()

    config = configparser.ConfigParser()
    cdata = config.read(args.c)
    convert(cdata)

from configparser import ConfigParser
import argparse
import sys, os

sys.stdout = open(os.devnull, "w")

parser = argparse.ArgumentParser()
config = ConfigParser()

parser.add_argument("--github_access_token", help="Github access token")
parser.add_argument("--aws_access_key_id", help="AWS access key id")
parser.add_argument("--aws_secret_access_key", help="AWS secret access key")
parser.add_argument("-b", "--bucket", help="S3 bucket name")

args = parser.parse_args()

config.add_section("github")
config.add_section("aws")
config.add_section("default")


config.set("github", "access_token", args.github_access_token)
config.set("aws", "aws_access_key_id", args.aws_access_key_id)
config.set("aws", "aws_secret_access_key", args.aws_secret_access_key)
config.set("aws", "bucket", args.bucket)
config.set("default", "file", "voters.csv")


with open(file="test.ini", mode="w+", encoding="utf-8") as f:
    config.write(f)

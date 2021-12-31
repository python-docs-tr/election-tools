import requests
import json
import boto3
import argparse
import sys, os
from configparser import ConfigParser

parser = argparse.ArgumentParser()
parser.add_argument("--no_print", help="Disable printing")
args = parser.parse_args()

if args.no_print:
    sys.stdout = open(os.devnull, "w")

config = ConfigParser()
config.read(".env")
FILE = config.get("default", "file")

session = boto3.Session(
    aws_access_key_id=config.get("aws", "access_key_id"),
    aws_secret_access_key=config.get("aws", "secret_access_key"),
)


def main():
    data = github()
    write_to_csv(data)
    upload_to_s3(FILE)
    print(f"File written to {FILE} and uploaded to S3")


def github():
    github_access_token = config.get("github", "access_token")
    url = "https://api.github.com/orgs/python-docs-tr/members"
    headers = {"Authorization": f"token {github_access_token}"}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def write_to_csv(data):
    with open(FILE, "w") as f:
        for member in range(len(data)):
            f.write(f"github,{data[member]['login']}\n")


def upload_to_s3(csv):
    s3 = session.resource("s3")
    bucket = config.get("aws", "bucket")
    data = open(csv, "rb")
    s3.Bucket(bucket).put_object(Key=csv, Body=data)


if __name__ == "__main__":
    main()

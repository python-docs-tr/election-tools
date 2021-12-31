import requests
import json
import boto3
from configparser import ConfigParser

config = ConfigParser()
config.read(".env")
FILE = config.get("default", "file")


def main():
    data = github()
    write_to_csv(data)
    upload_to_s3(FILE)
    print("File written to voters.csv and uploaded to S3")


def github():
    github_access_token = config.get("github", "access_token")
    url = "https://api.github.com/orgs/python-docs-tr/members"
    headers = {"Authorization": f"token {github_access_token}"}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def write_to_csv(data):
    with open("voters.csv", "w") as f:
        for member in range(len(data)):
            f.write(f"github,{data[member]['login']}\n")


def upload_to_s3(FILE):
    s3 = boto3.resource("s3")
    bucket = config.get("aws", "bucket")
    s3.Bucket(bucket).put_object(Key="voters.csv", Body=FILE)


if __name__ == "__main__":
    main()

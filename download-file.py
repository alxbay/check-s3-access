import boto3
import botocore
import yaml
from yaml.loader import SafeLoader
from os.path import exists

def log(type,message):
    # HEADER = '\033[95m' ; OKBLUE = '\033[94m' ;  OKCYAN = '\033[96m' ; OKGREEN = '\033[92m'
    # WARNING = '\033[93m' ; FAIL = '\033[91m' ; ENDC = '\033[0m' ; BOLD = '\033[1m' ; UNDERLINE = '\033[4m'    
    colors = {
        "head":'\033[4m',
        "info":'\033[0m',
        "warning":'\033[93m',
        "error":'\033[91m',
        "ok":'\033[92m'
    }
    print(colors.get(type) + message)
    return 0

def check_yaml(parameters_file):
    return_code = 0
    if exists(parameters_file):
        log("info","The file with parameters was loaded: "+parameters_file)
    else:
        log("error","The file with parameters is not found: "+parameters_file)
        return None

    try:
        with open(parameters_file) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
    except:
        log("error","Parsing error: syntax error.")
        return None

    try:
        buckets=data["buckets"]
    except:
        log("error","Parsing error: can't load section with buckets.")
        return None
    
    try:
        accounts=data["accounts"]
    except:
        log("error","Parsing error: can't load section with accounts.")
        return None
    check_accesses(buckets,accounts)
    return 0

def check_accesses(buckets,accounts):
    for b in buckets:
        log("info","")
        log("head","Check access to bucket: "+b["name"])
        for a in accounts:
            log("info","USER : "+a["name"])
            check_access_to_bucket(a["id"],a["key"],b["name"],b["folder"])
        log("info","")
    return 0

def check_access_to_bucket(u_id,u_key,bn,folder="*"):
    boto3_s3_client1 = boto3.client(
        's3',
        aws_access_key_id=u_id,
        aws_secret_access_key=u_key
    )
    try:
        result = boto3_s3_client1.list_objects_v2(Bucket = bn,Prefix=folder)
        log("ok","    The bucket is available.")
    except botocore.exceptions.ClientError as error:
        log("error","    The bucket is NOT available.")
        return None
    for o in result.get('Contents'):
        # print(o)
        try:
            data = boto3_s3_client1.get_object(Bucket=bn, Key=o.get('Key'))
        except botocore.exceptions.ClientError as error:        
            log("error","        - "+o.get('Key'))
        else:
            log("ok","        + "+o.get('Key'))
    return 0

parameters_file_yaml="params.yml"
check_yaml(parameters_file_yaml)

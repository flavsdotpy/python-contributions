import boto3


#PATH VARS
SCRIPT_FILE = 'emr_example.py'
BOOTSTRAP_FILE = 'emr_boostrap.sh'
S3_BUCKET = 'package-bucket'
LOCAL_RESOURCES = './resources/'
S3_PREFIX = 'emr/'

#CLUSTER CONFIG
LOG_URI = 's3n://aws-logs-XXXXXXXXXXX-us-east-1/elasticmapreduce/'
SUBNET_ID = 'subnet-XXXXXXXX'
KEY_PAIR = 'key-pair'
MASTER_TYPE = 'm4.large'
SLAVE_TYPE = 'r5.2xlarge'
SLAVE_NODES = 2

## REFER TO https://docs.google.com/spreadsheets/d/1vD_XA5CEbZVhwCgFQbi0yUsbUFHPqv1JDoJhaiIWrHw
SPARK_CONFIG = {
    'spark.executor.instances': '29',
    'spark.yarn.executor.memoryOverhead': '3072',
    'spark.executor.memory': '18G',
    'spark.yarn.driver.memoryOverhead': '3072',
    'spark.driver.memory': '18G',
    'spark.executor.cores': '2',
    'spark.driver.cores': '2',
    'spark.default.parallelism': '116'
}


def lambda_handler(event, context):
    conn = boto3.client('emr')
    s3 = boto3.client('s3')

    s3.upload_file(LOCAL_RESOURCES + SCRIPT_FILE, S3_BUCKET, S3_PREFIX + SCRIPT_FILE)
    s3.upload_file(LOCAL_RESOURCES + BOOTSTRAP_FILE, S3_BUCKET, S3_PREFIX + BOOTSTRAP_FILE)

    cluster_id = conn.run_job_flow(
        Name='Teste weekly',
        ServiceRole='EMR_DefaultRole',
        JobFlowRole='EMR_EC2_DefaultRole',
        VisibleToAllUsers=True,
        LogUri=LOG_URI,
        ReleaseLabel='emr-5.22.0',
        Instances={
            'Ec2SubnetId': SUBNET_ID,
            'InstanceGroups': [
                {
                    'Name': 'Master nodes',
                    'Market': 'ON_DEMAND',
                    'InstanceRole': 'MASTER',
                    'InstanceType': MASTER_TYPE,
                    'InstanceCount': 1,
                },
                {
                    'Name': 'Slave nodes',
                    'Market': 'ON_DEMAND',
                    'InstanceRole': 'CORE',
                    'InstanceType': SLAVE_TYPE,
                    'InstanceCount': SLAVE_NODES
                }
            ],
            'KeepJobFlowAliveWhenNoSteps': False,
            'TerminationProtected': False,
            'Ec2KeyName': KEY_PAIR,
        },
        Applications=[{
            'Name': 'Spark'
        }],
        BootstrapActions=[
            {
                'Name': 'Install python packages',
                'ScriptBootstrapAction': {
                    'Path': 's3://{}/{}'.format(S3_BUCKET, S3_PREFIX + BOOTSTRAP_FILE),
                    'Args': [
                    ]
                }
            },
        ],
        Configurations=[
            {
                'Classification':'spark-env',
                'Properties':{},
                'Configurations': [
                        {
                            'Classification': 'export',
                            'Properties': {
                            'PYSPARK_PYTHON': '/usr/bin/python3'
                            }
                        }
                    ]
                },
            {
                'Classification': 'spark-defaults',
                'Properties': SPARK_CONFIG
            }
        ],
        Steps=[
            {
                'Name': '[SETUP] Copying files',
                'ActionOnFailure': 'TERMINATE_CLUSTER',
                'HadoopJarStep': {
                    'Jar': 'command-runner.jar',
                    'Args': [
                        'aws', 's3', 'cp', 's3://{}/{}'.format(S3_BUCKET, S3_PREFIX + SCRIPT_FILE), '/home/hadoop/'
                    ]
                }
            },
            {
                'Name': 'Sample script',
                'ActionOnFailure': 'TERMINATE_CLUSTER',
                'HadoopJarStep': {
                    'Jar': 'command-runner.jar',
                    'Args': [
                        'spark-submit', 
                        '--deploy-mode', 'cluster',
                        '--master', 'yarn-cluster', 
                        '/home/hadoop/' + SCRIPT_FILE,
                        'arg1',
                        'arg2',
                        'arg3'
                    ]
                }
            }
        ],
        Tags=[
            {
                'Key': 'Key',
                'Value': 'Value'
            }
        ]
    )
    return 'Started cluster {}'.format(cluster_id)

if __name__ == '__main__':
    print(lambda_handler('', ''))
from time import sleep
import boto3
import csv


GLUE_DATABASE = 'ap3xx_datalake'
QUERY_OUTPUT_BUCKET = 'ap3xx-queries'
QUERY_OUTPUT_URI = f's3://{QUERY_OUTPUT_BUCKET}/{GLUE_DATABASE}'


def query_athena(athena_client, query, database, query_output):
    # Sends to AWS the command to start executing a query
    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': database},
        ResultConfiguration={'OutputLocation': query_output})
    return response.get('QueryExecutionId', False)


def athena_check_query_status(athena_client, query_id, wait_time=180, check_step=1):
    count = 0
    try:
        # Waits for the query to finish executing with success
        # The total wait time and the check step are configurable
        # Defaults are wait time of 3 mins and check every second
        while count <= wait_time:
            query_status = athena_client.get_query_execution(QueryExecutionId=query_id)
            state = query_status['QueryExecution']['Status']['State']
            if state == 'SUCCESS':
                return True
                count = wait_time
            elif state == 'FAILED':
                return False
                count = wait_time
            else:
                sleep(check_step)
                count += 1
            return False
    except Exception as e:
        print(e)
        return False

athena_client = boto3.client('athena')
s3_resource = boto3.resource('s3')
query = """SELECT full_name, income, job  
            FROM customers 
            WHERE sex = 'M' """

query_id = query_athena(athena_client, query, GLUE_DATABASE, QUERY_OUTPUT_URI)
if query_id and athena_check_query_status(athena_client, query_id):
    try:
        obj = s3_resource.Object(QUERY_OUTPUT_BUCKET, f'{GLUE_DATABASE}/{query_id}.csv')
        buffer = obj.get()["Body"].read().decode()
        obj_list = buffer.replace('"', '').splitlines()
        result = list(csv.DictWriter(obj_list))
        ## DO
        ## LOGIC
        ## HERE
    except Exception as e:
        print(e)
else:
    print('Something happened and the query was not executed')
    print('It may be still executing in this moment...')


    

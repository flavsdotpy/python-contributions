from urllib.parse import unquote

from aws.s3 import get_email_from_path, make_file_public_for_download
from aws.ses import send_mail
from commons.logger import config_log


def handle(event, context):
    logger = config_log()
    logger.info('Started processing queries...')
    for record in event['Records']:
        try:
            bucket = record['s3']['bucket']['name']
            key = unquote(record['s3']['object']['key'])
            logger.info(f'Processing file {key}')

            logger.info('Looking for destination email...')
            destination_email = get_email_from_path(key)

            logger.info('Looking for file download path...')
            file_download_path = make_file_public_for_download(bucket, key)

            logger.info(f'Sending email t0 {destination_email}')
            send_mail(destination_email, file_download_path)
        except Exception as e:
            logger.error(f'Something happened: ')
            logger.error(str(e))
    logger.info('Finished processing queries!')


if __name__ == '__main__':
    handle({
        'Records': [
            {
                's3': {
                    'object': {
                        'key': 'user@provider.com/torrent_magnets.txt'
                    },
                    'bucket': {
                        'name': 'bucket'
                    }
                }
            }
        ]
    }, None)

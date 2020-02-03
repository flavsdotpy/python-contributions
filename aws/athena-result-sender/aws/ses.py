import boto3

from commons.config import SES


def send_mail(destination_email, file_download_path):
    ses = boto3.client('ses')

    user_name = destination_email.split('@')[0]
    email_text = SES['base_message'].format(
        name=user_name,
        file_path=file_download_path
    )

    ses.send_email(
        Source=SES['email_sender'],
        Destination={
            'ToAddresses': [destination_email]
        },
        Message={
            'Subject': {
                'Data': 'Resultado de query pronto!'
            },
            'Body': {
                'Text': {
                    'Data': email_text
                }
            }
        }
    )

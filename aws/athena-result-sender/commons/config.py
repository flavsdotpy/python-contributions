AWS = {
    'region': 'us-east-2'
}

SES = {
    'base_message': """
        Caro {name},
        
        Your query result is ready to download at: {file_path}
        
        Cheers,
        
        Jarvis
    """,
    'email_sender': 'user@provider.com'
}

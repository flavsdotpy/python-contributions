from datetime import timedelta

# Gets dinamically the time delta based on the time unity name
def get_timedelta(value, unity):
        try:
            return {
                'days': lambda x: timedelta(days=x),
                'hours': lambda x: timedelta(hours=x),
                'minutes': lambda x: timedelta(minutes=x)
            }[unity](value)
        except KeyError:
            raise Exception(f'Time unity {unity} not found...')

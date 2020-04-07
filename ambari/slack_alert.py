#!/usr/bin/env python

import requests
import logging
import json
import sys
from datetime import datetime

SLACK_API_ENDPOINT = ''
LOG_PATH_FILE      = '/var/log/ambari-server/custom_notification.log'
TIMESTAMP          = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# :param definition_name: the alert definition unique ID
# :param definition_label: the human readable alert definition label
# :param service_name: the service that the alert definition belongs to
# :param alert_state: the state of the alert (OK, WARNING, etc)
# :param alert_text: the text of the alert

def main():
    definition_name = sys.argv[1]
    definition_label = sys.argv[2]
    service_name = sys.argv[3]
    alert_state = sys.argv[4]
    alert_text = sys.argv[5]
    send_message_to_slack(definition_name, definition_label, service_name, alert_state, alert_text, set_alert_color(alert_state))

def set_alert_color(alert_state):
    try:
        if alert_state == "OK":
            return "#00FF00"
        elif alert_state == "WARNING":
            return "#FADA5E"
        elif alert_state == "CRITICAL":
            return "#FF0000"
        else:
            return "#808080"
    except Exception as err:
        logging.warning(err)

def send_message_to_slack(definition_name, definition_label, service_name, alert_state, alert_text, color):
    try:
        request_body = {"attachments": [{"title": "AMBARI - {0}".format(TIMESTAMP), "text": "{0} :{1} \n {2} \n {3}".format(service_name, alert_state, definition_label, alert_text), "color": color}]}
        response = requests.post(SLACK_API_ENDPOINT, 
                                 data=json.dumps(request_body), 
                                 headers={'Content-Type': 'application/json'})
        if(response.status_code != 200):
            logging.warning('HTTP request failed! Status code: {0}'.format(str(response.status_code)))
            exit()
        else:
            logging.info('Message successful sent to slack channel - HTTP [200]')
            log_data = "Alert date: {0} \n Service: {1} \n State: {2} \n Text: {3} \n ------------------ \n".format(TIMESTAMP, service_name, alert_state, alert_text)
            save_log(log_data)
    except Exception as err:
        logging.warning(err)
    
def save_log(log_data):
    try:
        file = open(LOG_PATH_FILE, "a+")
        file.write(log_data)
        file.close()
    except Exception as err:
        logging.warning(err)

if __name__ == '__main__':
    main()
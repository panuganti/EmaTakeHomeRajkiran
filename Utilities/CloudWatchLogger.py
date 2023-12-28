import time
import boto3
import logging

# TODO: Add config for AWS
# TODO: Integrate with the application

class CloudWatchLogger:
    def __init__(self, config):
        self.logger = logging.getLogger('my-logger')
        self.logger.setLevel(logging.INFO)
        self.client = boto3.client('logs', region_name=config['aws']['aws_region'])
        self.log_group_name = config['aws']['log_group_name']
        self.log_stream_name = config['aws']['log_stream_name']
        self.use_aws = config['aws']['use_aws']

        if self.use_aws:
            # Create the log group if it doesn't exist
            try:
                self.client.create_log_group(logGroupName=self.log_group_name)
            except self.client.exceptions.ResourceAlreadyExistsException:
                pass

            # Create the log stream if it doesn't exist
            try:
                self.client.create_log_stream(logGroupName=self.log_group_name, logStreamName=self.log_stream_name)
            except self.client.exceptions.ResourceAlreadyExistsException:
                pass

    def info(self, message):
        if self.use_aws:
            response = self.client.put_log_events(
                logGroupName=self.log_group_name,
                logStreamName=self.log_stream_name,
                logEvents=[
                    {
                        'timestamp': int(time.time() * 1000),
                        'message': message
                    }
                ]
            )
            return response
        else:
            print(f"""INFO: """ + message)
            return None
    
    def error(self, message):
        if self.use_aws:
            response = self.client.put_log_events(
                logGroupName=self.log_group_name,
                logStreamName=self.log_stream_name,
                logEvents=[
                    {
                        'timestamp': int(time.time() * 1000),
                        'message': message
                    }
                ]
            )
            return response
        else:
            print(f"""ERROR: """ + message)
            return None

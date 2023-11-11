
import boto3

aws_access_key_id = 'AKIAXII2BKO7PPH2CJMQ'
aws_secret_access_key = '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'

sqs = boto3.client(
    'sqs',
    region_name='us-east-1',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)
queue_url = 'https://sqs.us-east-1.amazonaws.com/498807690174/transacciones_banco'
# Lista para guardar los mensajes procesados

processed_messages = []
message_counter = 0

def process_messages():
   global message_counter
   while True:
       response = sqs.receive_message( 
           QueueUrl=queue_url,
           AttributeNames=['All'],
           MessageAttributeNames=['All'],
           MaxNumberOfMessages=1,
           VisibilityTimeout=30,
           WaitTimeSeconds=20
       )

       if 'Messages' in response:
           receipt_handles = [message['ReceiptHandle'] for message in response['Messages']]
           if receipt_handles:
               sqs.delete_message_batch(
                  QueueUrl=queue_url,
                  Entries=[{'Id': str(i), 'ReceiptHandle': receipt_handle} for i, receipt_handle in enumerate(receipt_handles)]
               )
               message = response['Messages']
               processed_message = f"Mensaje Procesado: {message[0]['ReceiptHandle']}"
               processed_messages.append(processed_message)
               message_counter += 1
               print(f"Total messages processed: {message_counter}")

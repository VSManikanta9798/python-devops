from boto3.session import Session

ACCESS_KEY='AKIAQED72P2QPAMQ4CFW'
SECRET_KEY='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'

session = Session(aws_access_key_id=ACCESS_KEY,
                  aws_secret_access_key=SECRET_KEY)

s3 = session.resource('s3')

for bucket in s3.buckets.all():
        print(bucket.name)
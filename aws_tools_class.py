import datetime
import boto3

class aws_tools:
    
    def get_cost():
        #9月から合計金額を取得（請求書を見ると9月以前は請求無しだったので）
        start = datetime.datetime(2022, 9, 1).strftime('%Y-%m-%d')
        end = datetime.date.today().strftime('%Y-%m-%d')
        ce = boto3.client('ce')
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start,
                'End' :  end,
            },
            Granularity='MONTHLY',
            Metrics=[
                'UnblendedCost'
            ]
        )

        #月ごとに別れているのでトータルで表示できるように足し算する
        #理想は最初からトータルを取得したいところだがAWSのAPIでは出来ないぽい
        total_list = []
        for i in range( len( response['ResultsByTime'] ) ):
            total_list.append(float(response['ResultsByTime'][i]['Total']['UnblendedCost']['Amount']))

        #表示している通貨の情報を取得、もしJPYに変更しても自動反映されるようにちゃんとAPIから取ってくる
        total = "金額 " + str( round( sum(total_list), 2 ) ) + " " + response['ResultsByTime'][i]['Total']['UnblendedCost']['Unit']

        msg = {
        "time": "期間 " + start + " ~ " + end,
        "cost": total
        }
        #return response['ResultsByTime']
        return msg

    def get_pass():
        #https://dev.classmethod.jp/articles/secure-string-with-lambda-using-parameter-store/
        #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_parameter
        ssm = boto3.client('ssm')
        response = ssm.get_parameter(
            Name='lambda-passwd',
            WithDecryption=True
        )
        return response['Parameter']['Value']

    def s3_upload(S3_BUCKET_NAME, File_dir):
        s3 = boto3.client('s3')
        s3.upload_file(Filename=File_dir, Bucket=S3_BUCKET_NAME, Key=File_dir)

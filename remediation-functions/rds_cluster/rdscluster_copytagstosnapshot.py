'''
Copyright (c) Cloudneeti. All rights reserved.
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is  furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Enable Copy Tags to snapshot feature for AWS RDS database clusters
'''
import time
from botocore.exceptions import ClientError

def run_remediation(rds, RDSIdentifier):
    print("Executing RDS Cluster remediation")  
    copytagflag = False
    #Verify current cluster copy tags to snapshot config.
    try:
        response = rds.describe_db_clusters(DBClusterIdentifier = RDSIdentifier)['DBClusters']
        copytagflag = response[0]['CopyTagsToSnapshot']
    except ClientError as e:
        responseCode = 400
        output = "Unexpected error: " + str(e)
        print(output)
    except Exception as e:
        responseCode = 400
        output = "Unexpected error: " + str(e)
        print(output)

    if not copytagflag:
        #verify cluster state
        while response[0]['Status'] not in ['available', 'stopped']:
            try:
                response = rds.describe_db_clusters(DBClusterIdentifier = RDSIdentifier)['DBClusters']
                time.sleep(10)
            except ClientError as e:
                responseCode = 400
                output = "Unexpected error: " + str(e)
            except Exception as e:
                responseCode = 400
                output = "Unexpected error: " + str(e)
                
        #Update current value for copy tags to snapshot                   
        try:
            result = rds.modify_db_cluster(
                DBClusterIdentifier = RDSIdentifier,
                BackupRetentionPeriod = response[0]['BackupRetentionPeriod'],
                ApplyImmediately = False,
                CopyTagsToSnapshot = True
            )

            responseCode = result['ResponseMetadata']['HTTPStatusCode']
            if responseCode >= 400:
                output = "Unexpected error: %s \n" % str(result)
            else:
                output = "Copy tags to snapshot enabled for cluster : %s \n" % RDSIdentifier
                    
        except ClientError as e:
            responseCode = 400
            output = "Unexpected error: " + str(e)
            print(output)
        except Exception as e:
            responseCode = 400
            output = "Unexpected error: " + str(e)
            print(output)

        print(str(responseCode)+'-'+output)
    else:
        responseCode = 200
        output = 'Copy tags to snapshot already enabled for cluster : '+ RDSIdentifier
        print(output)

    return responseCode,output
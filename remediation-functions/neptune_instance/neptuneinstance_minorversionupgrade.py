'''
neptune auto version upgrade
'''

from botocore.exceptions import ClientError
import time

def run_remediation(neptune, instance_name):
    print("Executing remediation")            
    versionupgrade='' 
    #Verify current value for auto minor version upgrade 
    try:
        response = neptune.describe_db_instances(DBInstanceIdentifier = instance_name)['DBInstances']
        versionupgrade = response[0]['AutoMinorVersionUpgrade']
    except ClientError as e:
        responseCode = 400
        output = "Unexpected error: " + str(e)
    except Exception as e:
        responseCode = 400
        output = "Unexpected error: " + str(e)

    if not versionupgrade:
        #verify instance state  
        while response[0]['DBInstanceStatus'] not in ['available', 'stopped']:
            try:
                response = neptune.describe_db_instances(DBInstanceIdentifier = instance_name)['DBInstances']
                time.sleep(10)
            except ClientError as e:
                responseCode = 400
                output = "Unexpected error: " + str(e)
            except Exception as e:
                responseCode = 400
                output = "Unexpected error: " + str(e)
                
        #Update auto-minor version upgrade for neptune db-instance        
        try:
            result = neptune.modify_db_instance(
                        DBInstanceIdentifier = instance_name,
                        AutoMinorVersionUpgrade = True,
                        ApplyImmediately = True
                    )

            responseCode = result['ResponseMetadata']['HTTPStatusCode']
            if responseCode >= 400:
                output = "Unexpected error: %s \n" % str(result)
            else:
                output = "Auto version upgrade is now enabled for neptune instance : %s \n" % instance_name
                    
        except ClientError as e:
            responseCode = 400
            output = "Unexpected error: " + str(e)
            print(output)
        except Exception as e:
            responseCode = 400
            output = "Unexpected error: " + str(e)
            print(output)
    else:
        responseCode = 200
        output='Auto version upgrade is already enabled for neptune-instance : '+ instance_name
        print(output)

    print(str(responseCode)+'-'+output)
    return responseCode,output


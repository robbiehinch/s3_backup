import boto.ec2.autoscale


TIMESTAMP='20130627-170813'

AWS_USER_ID='1ZYHV1JJAENV48WK1202'
AWS_SECRET_KEY='1nlNFrxC2DZmZPGao7yhxnUBdnr9sKTOk5chE/+K'
#AWS_SDK_PATH='"C:\Program Files\AWS SDK for .NET\\bin\AWSSDK.dll"'
#BINARY_BUCKET='bin_1zyhv1jjaenv48wk1202'
#BINARY_KEY='mosaic_processor/' + TIMESTAMP + '.zip'
#EXECUTABLE='mosaic_processor.exe'
#EXEC_ARGS='MASTER'
#INSTANCE_TYPE='t1.micro'
#INSTANCE_PROFILE_NAME='mosaic_worker2'
#KEY_NAME='winrdp'
#SECURITY_GROUPS=['quicklaunch-1']
AUTO_SCALING_GROUP='mosaic_worker_group_win' + TIMESTAMP

#UD = windows_user_data.Create(BINARY_BUCKET, BINARY_KEY, EXECUTABLE, EXEC_ARGS, AWS_SDK_PATH)

#print UD

def main():

  conn = boto.ec2.autoscale.AutoScaleConnection(AWS_USER_ID, AWS_SECRET_KEY)


  policy_name = 'mosaic_worker_micro_scale_5'
  scale_policy = boto.ec2.autoscale.policy.ScalingPolicy(name=policy_name
                                  , adjustment_type='ExactCapacity'
                                  , as_name=AUTO_SCALING_GROUP
                                  , scaling_adjustment=5
                                  , cooldown=10)

  conn.create_scaling_policy(scale_policy)

  scale_policy = conn.get_all_policies(as_group=AUTO_SCALING_GROUP, policy_names=[policy_name])[0]


  print policy_name, ':', scale_policy



main()


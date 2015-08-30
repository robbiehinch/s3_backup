

import photo_backup

folder = "C:/Photos/"
filepathpattern = 'C:/Photos/{0}.zip'

AWS_USER_ID='AWS_UID'
AWS_SECRET_KEY='AWS_SECRETY_KEY'
BUCKET_NAME='BUCKET_NAME'#.s3.amazonaws.com'


photo_backup.run(folder, filepathpattern, AWS_USER_ID, AWS_SECRET_KEY, BUCKET_NAME, )



import datetime
import os
import zipfile
import boto
import boto.s3.connection
import logging
import multipart_upload
import traceback
import math



import hashlib
def hashfile(afile, hasher, blocksize=65536):
    print 'hashing', afile
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    d = hasher.digest()
    print 'hash:', d
    return d

  
def zipdir(path, zipDict):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for f in files:
            flocation = os.path.join(root, f)
            t = datetime.datetime.fromtimestamp( os.path.getmtime(flocation) )
            fileYear = t.year
            zipFile = zipDict.get(fileYear)
            if zipFile:
                zipFile.write(flocation)
                print f
            else:
                logging.error('No zipfile for year %d of file %s', fileYear, f)


def percent_cb(complete, total):
  print complete, '/', total

    
def upload(path, AWS_USER_ID, AWS_SECRET_KEY, BUCKET_NAME, ):
#  multipart_upload.main(path, BUCKET_NAME, s3_key_name='LeoniesPhotos.zip', use_rr=True,
#         make_public=False, AWS_USER_ID=AWS_USER_ID, AWS_SECRET_KEY=AWS_SECRET_KEY)
#  conn = boto.connect_s3(AWS_USER_ID, AWS_SECRET_KEY, calling_format=boto.s3.connection.OrdinaryCallingFormat())
#  bucket = conn.get_bucket(BUCKET_NAME, validate=False)
#  k = boto.s3.key.Key(bucket)
#  k.key = 
#  logging.info('uploading %s', k.key)
#  k.set_contents_from_filename(path, cb=percent_cb, num_cb=10)

  from filechunkio import FileChunkIO

# Connect to S3
  c = boto.connect_s3(AWS_USER_ID, AWS_SECRET_KEY)
  b = c.get_bucket(BUCKET_NAME)

# Get file info
  source_path = path
  source_size = os.stat(source_path).st_size

# Create a multipart upload request
  mp = b.initiate_multipart_upload(os.path.basename(source_path))

# Use a chunk size of 50 MiB (feel free to change this)
  chunk_size = 52428800
  chunk_count = int(math.ceil(source_size / float(chunk_size)))

  print 'source_size is', source_size
  print 'chunk_size is', chunk_size
  print 'chunk_count is', chunk_count

# Send the file parts, using FileChunkIO to create a file-like object
# that points to a certain byte range within the original file. We
# set bytes to never exceed the original file size.
  for i in range(chunk_count):

      print 'uploading chunk', i
      offset = chunk_size * i
      bytes = min(chunk_size, source_size - offset)
      with FileChunkIO(source_path, 'r', offset=offset,
                         bytes=bytes) as fp:
          mp.upload_part_from_file(fp, part_num=i + 1)
  print 'upload complete'
# Finish the upload
  mp.complete_upload()


def uploadIfHashDifferent(filepath, AWS_USER_ID, AWS_SECRET_KEY, BUCKET_NAME, ):
    logging.info('Checking if upload needed for %s...', filepath)

    if os.path.getsize(filepath) < 1:
        logging.info('%s is empty', filepath)
        return

    hash_path = filepath + '.md5'
    if os.path.exists(hash_path):
        with open(hash_path, 'rb') as hashf:
            existingHash = hashf.read()
    else:
        existingHash = ''

    logging.info('hash for [%s] is [%s]', filepath, existingHash)
    with open(filepath, 'rb') as f:
        h = hashfile(f, hashlib.md5())

    if h != existingHash:
        logging.info("hash doesn't match")
        logging.info('%s', existingHash)
        logging.info('%s', h)
        upload(filepath, AWS_USER_ID, AWS_SECRET_KEY, BUCKET_NAME, )
        with open(hash_path, 'wb') as hashf:
            hashf.write(h)


def run(srcFolder, filepathpattern, AWS_USER_ID, AWS_SECRET_KEY, BUCKET_NAME, ):
    filepathsAndYears = [ (filepathpattern.format(x), x) for x in xrange(2000, datetime.date.today().year + 1) ]
    zipFiles = {}
    for filepath, year in filepathsAndYears:
        zipf = zipfile.ZipFile(filepath, 'w', zipfile.ZIP_STORED, True)
        zipFiles[year] = zipf
    zipdir(srcFolder, zipFiles)

    for v in zipFiles.values():
        v.close()

    for filepath, _ in filepathsAndYears:
        uploadIfHashDifferent(filepath, AWS_USER_ID, AWS_SECRET_KEY, BUCKET_NAME, )


    #try:
    #    upload(filepath)
    #except Exception as e:
    #    logging.error('Upload failed %s', e)
    #    traceback.print_exc()




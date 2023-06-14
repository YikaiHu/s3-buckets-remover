# s3-buckets-remover
A powerful tool for parallel deletion of S3 buckets, including the removal of versioned objects.

## Key Features

- Batch deletion: Easily remove multiple S3 buckets in one go, saving time and effort.
- Concurrent processing: The tool is designed to delete buckets concurrently, maximizing efficiency and minimizing processing time.
- Versioned object removal: Along with the buckets, the tool can delete all versioned objects associated with them, ensuring a complete cleanup.
- Simple usage: Users only need to provide a list of bucket names, and the tool takes care of the rest.


Whether you need to clean up your S3 storage after a project or streamline your AWS resources, s3-bucket-remover is your go-to solution for fast and hassle-free bucket deletion with support for versioned objects.

## How to use

1. Configure the AWS CLI with credentials.
2. Configure the `remove-bucket-list.txt` file. Each line should contain the name of a bucket.
3. Run `python3 ./s3_buckets_remover.py`.
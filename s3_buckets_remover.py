import boto3
import concurrent.futures
import datetime

s3_resource = boto3.resource('s3')
s3 = boto3.client('s3')


def read_bucket_names_from_config(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]


def delete_bucket_new(each_bucket, region_info):
    try:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(
            f"[{current_time}] - Starting removal of bucket {each_bucket} in region {region_info}")

        s3_new = boto3.client('s3', region_name=region_info,
                              endpoint_url=f'https://s3.{region_info}.amazonaws.com')
        s3_resource_new = boto3.resource('s3', region_name=region_info)
        bucket_new = s3_resource_new.Bucket(each_bucket)

        current_object = 0
        objects_batch_size = 1000

        # Delete objects in the bucket
        for obj in bucket_new.objects.all():
            obj.delete()
            current_object += 1

            if current_object % objects_batch_size == 0:
                print(
                    f"Thread: {each_bucket} - Deleted objects count: {current_object}")

        current_version = 0
        versions_batch_size = 1000

        for obj_version in bucket_new.object_versions.all():
            obj_version.delete()
            current_version += 1

            if current_version % versions_batch_size == 0:
                print(
                    f"Thread: {each_bucket} - Deleted versions count: {current_version}")

        # Delete the bucket
        s3_new.delete_bucket(Bucket=each_bucket)
        print(f"[{current_time}] - Bucket {each_bucket} deleted successfully")
    except Exception as e:
        if 'NoSuchBucket' in str(e):
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(
                f"[{current_time}] - Bucket {each_bucket} no longer exists, already deleted")
        else:
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(
                f"[{current_time}] - Failed to delete bucket {each_bucket}. Error: {str(e)}")


if __name__ == '__main__':
    buckets = read_bucket_names_from_config('./remove-bucket-list.txt')

    # Process the list of buckets and objects to be deleted in parallel using multiple threads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        params = []
        for each_bucket in buckets:
            try:
                region_info = s3.get_bucket_location(Bucket=each_bucket)[
                    'LocationConstraint'] or 'us-east-1'
                params.append((each_bucket, region_info))
            except Exception as err:
                print(
                    f'Failed to get region info for bucket {each_bucket}. Error: {err}')
                continue
        print('Bucket collection complete!')

        # Submit tasks to the thread pool
        results = [executor.submit(lambda args: delete_bucket_new(
            *args), param) for param in params]

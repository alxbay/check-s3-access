the input is a yaml with a list of buckets and users.

buckets:
  - name   : "arn:aws:s3:region:account_id:accesspoint/access_s3_point_name_01"
    folder : "*"
  - name   : "arn:aws:s3:region:account_id:accesspoint/access_s3_point_name_02"
    folder : "folder_01"
  - name   : "arn:aws:s3:region:account_id:accesspoint/access_s3_point_name_03"
    folder : "folder_02"

accounts:
  - name   : "user-01"
    id     : "AKIA_chahge_for_user_01"
    key    : "key_chahge_for_user_01"
  - name   : "user-02"
    id     : "AKIA_chahge_for_user_02"
    key    : "key_chahge_for_user_02"

from assistant.ftp_upload import (
    upload_file
)

url = upload_file(
    "cat.png"
)

print(
    "UPLOADED:"
)

print(
    url
)

input("ENTER...")
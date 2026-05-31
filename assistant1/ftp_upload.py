from ftplib import FTP
from datetime import datetime
import os


FTP_HOST = "rufree53.hostiman.ru"
FTP_USER = "s273644"
FTP_PASS = "wB2fpWl118"
FTP_DIR  = "/www/102procenta.ru/Upload_Bot"
PUBLIC_URL = "https://102procenta.ru/Upload_Bot/"

PUBLIC_URL = (
    "https://102procenta.ru/Upload_Bot/"
)


def upload_file(path):

    ext = os.path.splitext(path)[1]

    filename = (
        datetime.now()
        .strftime(
            "img_%Y%m%d_%H%M%S"
        )
        + ext
    )

    ftp = FTP(
        FTP_HOST
    )

    ftp.login(
        FTP_USER,
        FTP_PASS
    )

    ftp.cwd(
        FTP_DIR
    )

    with open(
        path,
        "rb"
    ) as f:

        ftp.storbinary(
            f"STOR {filename}",
            f
        )

    ftp.quit()

    return (
        PUBLIC_URL
        + filename
    )
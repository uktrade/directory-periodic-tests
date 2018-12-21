#!/usr/bin/env python3
import os
from mohawk import Sender


IP_RESTRICTOR_SKIP_CHECK_SENDER_ID = os.environ["IP_RESTRICTOR_SKIP_CHECK_SENDER_ID"]
IP_RESTRICTOR_SKIP_CHECK_SECRET = os.environ["IP_RESTRICTOR_SKIP_CHECK_SECRET"]


def hawk_cookie():
    sender = Sender(
        credentials={
            'id': IP_RESTRICTOR_SKIP_CHECK_SENDER_ID,
            'key': IP_RESTRICTOR_SKIP_CHECK_SECRET,
            'algorithm': 'sha256'
        },
        url='/',
        method='',
        always_hash_content=False
    )
    return f"ip-restrict-signature={sender.request_header}"


if __name__ == "__main__":
    print(hawk_cookie())

import logging

from bidms import bidms
import json

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

if __name__ == '__main__':
    cred_json = {}
    with open('credential.json') as f:
        cred_json = json.load(f)

    b = bidms.Bidms(cred_json['username'], cred_json['password'])
    # data = b.get_tong_feng_kong_tiao()
    # for d in data:
    #     print d
    data = b.get_electric_meter()
import salt.config
import salt.utils.event
import requests
import fnmatch
import json


def main():
    opts = salt.config.client_config('/etc/salt/master')
    event = salt.utils.event.get_event(
        'master',
        sock_dir=opts['sock_dir'],
        transport=opts['transport'],
        opts=opts)

    while True:
        ret = event.get_event(full=True)
        if ret is None:
            print('*')
            continue
        if fnmatch.fnmatch(ret['tag'], 'salt/job/*/ret/*'):
            print(ret)
            payload = ret['data']
            r = requests.post('http://manager/events', data=json.dumps(payload))
            print(r.status_code)


if __name__ == '__main__':
    main()

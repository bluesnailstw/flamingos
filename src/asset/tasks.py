from salt.salt_api import Pepper
from asset.models import Host
from manager.celery_app import app


def sync_all_disk_info():
    p = Pepper().login()
    res = p.local(tgt='*', fun='status.diskstats')
    for minion in res['return']:
        for minion_id in minion:
            data = minion[minion_id]
            print(data)


@app.task()
def sync_all_host_info():
    p = Pepper().login()
    res = p.local(tgt='*', fun='grains.items')
    for minion in res['return']:
        for minion_id in minion:
            data = minion[minion_id]
            if isinstance(data, dict):
                Host.objects.update_or_create(minion_id=minion_id,
                                              defaults={'host_name': data.get('host'),
                                                        'machine_id': data.get('machine_id'),
                                                        'manufacturer': data.get('manufacturer'),
                                                        'serialnumber': data.get('serialnumber'),
                                                        'oscodename': data.get('oscodename'),
                                                        'osrelease': data.get('osrelease'),
                                                        'cpu_model': data.get('cpu_model'),
                                                        'disks': data.get('disks'),
                                                        'mem_total': data.get('mem_total'),
                                                        'swap_total': data.get('swap_total'),
                                                        'num_cpus': data.get('num_cpus'),
                                                        'virtual': data.get('virtual'),
                                                        'virtual_subtype': data.get('virtual_subtype'),
                                                        'ip4_interfaces': data.get('ip4_interfaces'),
                                                        'salt_raw': data}
                                              )
            else:
                pass

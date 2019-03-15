openresty-repo:
  pkgrepo.managed:
    - humanname: openresty-repo
    - baseurl: https://openresty.org/package/centos/$releasever/$basearch
    - gpgcheck: 1
    - gpgkey: https://openresty.org/package/pubkey.gpg


openresty:
  pkg:
    - installed
    - require:
      - pkgrepo: openresty-repo


openresty-resty:
  pkg:
    - installed
    - require:
      - pkgrepo: openresty-repo


/usr/local/openresty/nginx/conf/nginx.conf:
  file:
    - managed
    - source: salt://test2/files/nginx.conf
    - template: jinja
    - require:
      - pkg: openresty

openresty-absent:
  process.absent:
    - name: openresty


run_openresty:
  cmd.run:
    - name: openresty
    - require:
      - pkg: openresty
      - file: /usr/local/openresty/nginx/conf/nginx.conf
      - process: openresty-absent

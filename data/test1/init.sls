vim:
  pkg.installed:
    - name: {{ pillar.redis_pillar['vim_name']  }}
passwd:
  pkg.installed
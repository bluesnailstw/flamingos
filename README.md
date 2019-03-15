curl -k http://127.0.0.1/login -H "Accept: application/x-yaml" -d username='flamingos' -d password='flamingos' -d eauth='pam'
 
    
curl -k http://127.0.0.1 -H "Accept: application/x-yaml" -H "X-Auth-Token: 2a99fd9fd52793e70c93b1affb29b00276d7a4c2"  -d client="local"  -d tgt='*' -d fun='test.ping'
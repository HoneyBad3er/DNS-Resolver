# DNS-Resolver
Simple DNS-resolver server. Works with type-A records locally (from static bind file) also can forward queries to remote DNS (1.1.1.1 by default) and cache result for ttl
## DNS Performance Testing Tool Results:
  * Run time (s):         10.003238
  * Queries per second:   16062.59893

## Ho to run:
* Requires: python 3.10+
* `python dns_resolver/manage.py` - run dns-resolver on localhost:1053

## How to test:
* `dig @localhost -p 1053 example.com +noedns`

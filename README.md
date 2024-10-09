# DNS-Resolver
Simple DNS-resolver server. Works with type-A records locally (from static bind file) also can forward queries to remote DNS (1.1.1.1 by default) and cache result for ttl
## DNS Performance Testing Tool Results:
### Statistics:
  * Queries sent:         11438196
  * Queries completed:    11438096 (100.00%)
  * Queries lost:         100 (0.00%)
  * Run time (s):         360.002450
  * Queries per second:   31772.272661

## Ho to run:
* Requires: python 3.10+
* `python dns_resolver/manage.py` - run dns-resolver on localhost:1053

## How to test:
* `dig @localhost -p 1053 example.com +noedns`

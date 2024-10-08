# DNS-Resolver
Simple DNS-resolver server. Works with type-A records locally (from static bind file) also can forward queries to remote DNS (1.1.1.1 by default)
## Ho to run:
* Requires: python 3.10+
* `python dns_resolver/manage.py` - run dns-resolver on localhost:1053

## How to test:
* `dig @localhost -p 1053 example.com +noedns`

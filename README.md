# DNSnitch
Uses viewdns.info to perform a reverse NS lookup on a specified nameserver and attempts zone transfers on all the discovered domains.

### Usage:
-n NAMESERVER, --nameserver NAMESERVER (Name server e.g. ns1.target.com)  <br />
-zt, --zonetransfer (Attempt zone transfers on discovered domains)  <br />
-o OUTPUT, --output OUTPUT (Destination output file)  <br />

### Example:
$ DNSnitch.py -n nameserver.target.com -zt

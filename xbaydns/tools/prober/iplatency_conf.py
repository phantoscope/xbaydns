PING_CMD = "ping -c5 -q %s"
PING_RE = ".* min/avg/max/\D+ = ([0-9.]+)/([0-9.]+)/([0-9.]+).* ms"
DIG_CMD = "dig +noanswer +noquestion @%s . NS"
DIG_RE = "Query time: (\d+) msec"
TRACERT_CMD = "traceroute -w1 %s 2>&1"
TRACERT_RE = "(\(\d+.\d+.\d+.\d+\))"
MAXQUERIES = 5
QUERY_INTERVAL = 5
MAX_TESTING = 5

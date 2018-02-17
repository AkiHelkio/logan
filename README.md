# logan
Log analyzer for monitoring and alerting

### Features
- Continuous log file monitoring
- Configurable data sets and data set thresholds
- Alert notifications via email and webhooks

# Specs
makerows.py will generate our test data that includes a full datetime on every row,
and will print out ids of nodes and the 'current' usage percentages of the nodes.

Example:
```
2017-10-17 17:23:45 Node 307 usage is 81
2017-10-17 17:23:47 Node 309 usage is 36
2017-10-17 17:23:47 Node 309 usage is 45
2017-10-17 17:23:47 Node 307 usage is 78
```

The monitoring software should then start with a configuration that determines
what events to search and to use either a secondary value within the row or to
use a ocurrence threshold.

Call example: Search for nodes and the usage percentage over 85
```bash
python logan.py --search 'Node {id}' --threshold 85 --rowvalue 'usage is {v}'
``` 

Call example: Search for nodes and alert on nodes that have more than 5 changes
within a period of 10 seconds.
```bash
python logan.py --search 'Node {id}' --threshold 5 --changes 10
``` 


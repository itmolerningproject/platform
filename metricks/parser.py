import re

output = """
NAMES                STATUS
odoo16               Up 49 minutes
postgres             Up 49 minutes
platform_pgadmin_1   Up 49 minutes
maildev              Up 49 minutes (healthy)
"""

service_output = """
NAME                 CPU %     MEM USAGE / LIMIT / MEM %    NET I/O           BLOCK I/O
odoo16               0.01%     133.7MiB / 30.6GiB / 0.43%   2.03MB / 1.36MB   101MB / 0B
postgres             0.00%     81.95MiB / 30.6GiB / 0.26%   1.39MB / 2MB      118MB / 13.5MB
platform_pgadmin_1   0.03%     158.7MiB / 30.6GiB / 0.51%   32.3kB / 0B       62.1MB / 4.24MB
maildev              0.00%     44.66MiB / 30.6GiB / 0.14%   32.4kB / 0B       59.1MB / 0B
"""

# Parse service output
service_lines = service_output.strip().split('\n')
service_header = re.split(r'\s{2,}', service_lines[0].strip())
services = []

for line in service_lines[1:]:
    values = re.split(r'\s{2,}', line.strip())
    service_data = dict(zip(service_header, values))
    services.append(service_data)

# Parse status output
status_lines = output.strip().split('\n')
status_header = status_lines[0].split()
status_data = []

for line in status_lines[1:]:
    values = line.split()
    status_data.append(dict(zip(status_header, values)))

# Combine the data
for service in services:
    for status in status_data:
        if service['NAME'] == status['NAMES']:
            service['STATUS'] = status['STATUS']

print(services)

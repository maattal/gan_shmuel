import os

PORTS = {
    'PORT_CI':'8085',
    'WEIGHT_PORT_STAGING':'8082',
    'WEIGHT_PORT_MAIN':'8080',
    'BILLING_PORT_STAGING':'8081',
    'BILLING_PORT_MAIN':'8086',
    }


for port in PORTS:
    os.environ[port] = PORTS[port]
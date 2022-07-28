```
>>> DOCKER_SCAN_SUGGEST=false DOMAIN=DOMAIN IDENTITY=IDENTITY  DEBUG=DEBUG  docker compose up --build

${DOMAIN}:8080/help/?format=json

with filter:
${DOMAIN}:8080/help/?format=json&filter=auth
```

#!/bin/bash
curl -X POST \
    -H "content-type:application/json" -d '{"swaggerUrl":"https://finnhub.io/static/swagger.json","lang": "python","options":{"packageName":"finnhub_swagger_api","projectName":"finnhub_swagger_api"}}' https://generator.swagger.io/api/gen/clients/python

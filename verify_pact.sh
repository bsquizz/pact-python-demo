#!/bin/bash
VERSION=$1
if [ -x $VERSION ]; then
    echo "ERROR: You must specify a provider version"
    exit
fi

pipenv run pact-verifier --provider-base-url=http://localhost:5001 \
  --pact-url="http://127.0.0.1/pacts/provider/UserService/consumer/UserServiceClient/latest" \
  --provider-states-setup-url=http://localhost:5001/_pact/provider_states \
  --provider-app-version $VERSION \
  --pact-broker-username pactbroker \
  --pact-broker-password pactbroker \
  --publish-verification-results

# OffRisk UI
OffRisk UI is running with the server OffRisk, and both need to be on the same network
To create the network:
~~~
docker network create off-risk-net
~~~

# Build the docker:
The docker can be build from the server repo using docker-compose. both repo needs to be on the same directory:

root
    -OffRisk
    -OffRisk-ui

More instruction can be found in the documentation and in repo OffRisk
# Run locally with pycharm
~~~
streamlit run main.py
~~~

## go to the browser at:
http://localhost:8501/

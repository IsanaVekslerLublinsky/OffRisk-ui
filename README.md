# OffRisk UI


# build
~~~
docker build -t off-risk-ui ./ -f Dockerfile
~~~

# Run with Docker

Iy you wish to run the ui with crispr-il (gogenome) please run the following command: 
~~~
docker run --network host off-risk-ui
~~~
Else you can run the following:
~~~
docker run -p8501:8501 off-risk-ui
~~~

If you are running with off-risk server as well you need to connect them to the same network.
To create the network and then connect the docker to it:
~~~
docker network create off-risk-net
docker run -p8501:8501 --net off-risk-net off-risk-ui
~~~


# Run localy with pycharm
~~~
streamlit run main.py
~~~

## go to the browser at:
http://localhost:8501/

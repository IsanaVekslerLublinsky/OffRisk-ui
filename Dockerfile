FROM python:3.8
EXPOSE 8501

RUN apt-get update && apt-get install --no-install-recommends -y r-base && \
    R -e "install.packages('tools',dependencies=TRUE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('rjson',dependencies=TRUE, repos='http://cran.rstudio.com/')"

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY /app /app
COPY /images /images
# COPY /scripts /scripts

RUN mkdir -p /output/ && \
    mkdir -p /log/

WORKDIR /app
CMD streamlit run home.py

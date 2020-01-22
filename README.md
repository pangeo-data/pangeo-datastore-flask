# Pangeo Cloud Datastore

Dynamic implementation of Pangeo Cloud Datastore using Flask, deployed through Google App Engine.

[https://catalog.pangeo.io/](https://catalog.pangeo.io/)

![Cloud Build](https://storage.googleapis.com/pangeo-181919-badges/builds/pangeo-datastore-flask/branches/master.svg)

To deploy locally:

```
git clone https://github.com/pangeo-data/pangeo-datastore-flask.git
cd pangeo-datastore-flask
conda create -n pangeo-datastore-flask python=3.7
conda activate pangeo-datastore-flask
pip install -r requirements.txt
python main.py
```

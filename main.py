# [START gae_python37_render_template]
import intake
import xarray as xr

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

xr.set_options(display_style="html")

catalog_dir = "https://raw.githubusercontent.com/pangeo-data/pangeo-datastore/master/intake-catalogs/"
master = intake.open_catalog(catalog_dir + "master.yaml")

@app.route('/')
def root():
    crumbs = ['<li class="active">master</li>']
    return render_template("catalog.html", cat=master,
                                           url=request.base_url.rstrip("/"),
                                           crumbs=crumbs)

@app.route('/<path:path>')
def parse(path):
    url = request.url_root.rstrip("/")
    cat = master
    crumbs = [f'<li><a href="{url}">master</a></li>']
    for item in path.rstrip("/").split("/"):
        url += f"/{item}"
        if url != request.base_url:
            crumbs.append(f'<li><a href="{url}">{item}</a></li>')
        else:
            crumbs.append(f'<li class="active">{item}</li>')
        parent = cat
        cat = cat[item]

    if cat.container == "catalog": # only render Intake catalogs
        return render_template("catalog.html", cat=cat,
                                               url=request.base_url.rstrip("/"),
                                               crumbs=crumbs)
    elif cat.container == "xarray":
        return render_template("xarray.html", cat=cat,
                                              parent=parent, item=item,
                                              url=request.base_url.rstrip("/"),
                                              crumbs=crumbs)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [START gae_python37_render_template]

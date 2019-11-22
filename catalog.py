import intake
import xarray as xr

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)

xr.set_options(display_style="text")

catalog_dir = "https://raw.githubusercontent.com/pangeo-data/pangeo-datastore/master/intake-catalogs/"
master = intake.open_catalog(catalog_dir + "master.yaml")

@app.route('/')
def index():
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
        cat = cat[item]

    if cat.container != "catalog": # only render Intake catalogs
        return "<p>Only Intake catalogs will be rendered.</p>"

    return render_template("catalog.html", cat=cat,
                                           url=request.base_url.rstrip("/"),
                                           crumbs=crumbs)


@app.route('/test_bootstrap')
def test_bootstrap():
    cat = master["ocean"]
    return render_template("xarray.html", cat=cat)

if __name__ == "__main__":
    app.run(debug=True)

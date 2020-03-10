# [START gae_python37_render_template]
import intake
import os
import requests
import sys
import xarray as xr

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_caching import Cache
from flask_seasurf import SeaSurf
from flask_talisman import Talisman

app = Flask(__name__)
app.secret_key = os.urandom(16)
csrf = SeaSurf(app)

csp = {"style-src": ["'self'",
                     "https://cdnjs.cloudflare.com",
                     "https://cdn.datatables.net",
                     "https://unpkg.com",
                     "https://fonts.googleapis.com",
                     "'unsafe-inline'"],
       "script-src": ["'self'",
                      "https://cdnjs.cloudflare.com",
                      "https://unpkg.com",
                      "'unsafe-inline'"],
       "font-src": ["'self'",
                    "data:",
                    "https://cdnjs.cloudflare.com",
                    "https://fonts.gstatic.com"]}
Talisman(app, content_security_policy=csp)

cache = Cache(config={'CACHE_TYPE': 'simple',
                      'CACHE_DEFAULT_TIMEOUT': 1800})

cache.init_app(app)
Bootstrap(app)

xr.set_options(display_style="html")

catalog_dir = "https://raw.githubusercontent.com/pangeo-data/pangeo-datastore/master/intake-catalogs/"
master = intake.open_catalog(catalog_dir + "master.yaml")


@app.route('/')
@cache.cached()
def root():
    crumbs = ['<li class="active">master</li>']
    return render_template("catalog.html", cat=master,
                           url=request.base_url.rstrip("/"),
                           crumbs=crumbs)


@app.route('/<path:path>')
@cache.cached()
def parse(path):
    try:
        # collect crumbs and search for entry
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
        # intake catalogs
        if cat.container == "catalog":
            return render_template("catalog.html", cat=cat,
                                   url=request.base_url.rstrip("/"),
                                   crumbs=crumbs)
        # intake-esm collections
        elif cat._driver == "intake_esm.esm_datastore":
            r = requests.get(cat.esmcol_path)
            return render_template("esmcol.html", cat=cat,
                                   parent=parent, item=item,
                                   url=request.base_url.rstrip("/"),
                                   crumbs=crumbs, json=r.json())
        # anything that can be handled with `to_dask()`
        elif cat.container in ["dataframe", "xarray"]:
            return render_template("dask.html", cat=cat,
                                   parent=parent, item=item,
                                   url=request.base_url.rstrip("/"),
                                   crumbs=crumbs)
        # generic error for anything else
        else:
            raise NotImplementedError(f"This type of dataset isn't recognized: \
                                      {cat.container}, {cat._driver}")
    except:
        type, value = sys.exc_info()[:2]
        return render_template("error.html", type=type, value=value), 500

      
@app.route('/favicon.ico')
@cache.cached()
def favicon():
  return redirect(url_for('static', filename='favicon.ico'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
# [START gae_python37_render_template]

# [START gae_python37_render_template]
import intake
import os
import requests
import sys
import xarray as xr

from flask import Flask, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_caching import Cache
from flask_seasurf import SeaSurf
from flask_talisman import Talisman

app = Flask(__name__)
app.secret_key = os.urandom(16)
csrf = SeaSurf(app)

csp = {'style-src': ["'self'",
                     'https://cdnjs.cloudflare.com',
                     'https://cdn.datatables.net',
                     'https://unpkg.com',
                     'https://fonts.googleapis.com',
                     "'unsafe-inline'"],
       'script-src': ["'self'",
                      'https://cdnjs.cloudflare.com',
                      'https://unpkg.com',
                      "'unsafe-inline'"],
       'font-src': ["'self'",
                    'data:',
                    'https://cdnjs.cloudflare.com',
                    'https://fonts.gstatic.com']}
Talisman(app, content_security_policy=csp)

cache = Cache(config={'CACHE_TYPE': 'simple',
                      'CACHE_DEFAULT_TIMEOUT': 1800})

cache.init_app(app)
Bootstrap(app)

xr.set_options(display_style='html')

catalog_dir = 'https://raw.githubusercontent.com/pangeo-data/pangeo-datastore/master/intake-catalogs/master.yaml'
master = intake.open_catalog(catalog_dir)


@app.route('/')
@cache.cached()
def index():
    return render_template('index.html')


@app.route('/browse/<path:path>/')
@cache.cached()
def browse(path):
    try:
        # check if entry is in pangeo catalog or remote catalog
        items = path.split('/')
        if items[0] == 'master':
            cat = master
        else:
            raise NotImplementedError('Remote catalogs not currrently supported')
        # create breadcrumbs for root catalog
        if len(items) == 1:
            crumbs = ['<li class="active">%s</li>' % cat.name]
            return render_template('catalog.html', cat=cat, crumbs=crumbs, path=path,
                                   catalogs=any([cat[item]._container == 'catalog' for item in cat]),
                                   datasets=any([cat[item]._container in ['dataframe', 'xarray'] for item in cat]))
        else:
            crumbs = ['<li><a href="%s">%s</a></li>' %
                    (url_for('browse', path='/'.join(items[0:1])), cat.name)]
        # generate other breadcrumbs and search for entry
        for i, item in enumerate(items[1:]):
            cat = cat[item]
            if items[0:i+2] != items:
                crumbs.append('<li><a href="%s">%s</a></li>' %
                    (url_for('browse', path='/'.join(items[0:i+2])), item))
            else:
                crumbs.append('<li class="active">%s</li>' % item)
        # intake catalogs
        if cat._container == 'catalog':
            return render_template('catalog.html', cat=cat, crumbs=crumbs, path=path,
                                   catalogs=any([cat[item]._container == 'catalog' for item in cat]),
                                   datasets=any([cat[item]._container in ['dataframe', 'xarray'] for item in cat]))
        # intake-esm collections
        elif cat._driver == 'intake_esm.esm_datastore':
            r = requests.get(cat._captured_init_kwargs['args']['esmcol_obj'])
            return render_template('esmcol.html', cat=cat, crumbs=crumbs, json=r.json())
        # anything that can be handled with `to_dask()`
        elif cat._container in ['dataframe', 'xarray']:
            return render_template('dask.html', cat=cat, crumbs=crumbs)
        # generic error for anything else
        else:
            raise NotImplementedError('This type of dataset is not recognized: %s, %s' %
                                     (cat._container, cat._driver))
    except:
        type, value = sys.exc_info()[:2]
        return render_template('error.html', type=type, value=value), 500


@app.route('/favicon.ico')
@cache.cached()
def favicon():
  return redirect(url_for('static', filename='favicon.ico'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
# [START gae_python37_render_template]

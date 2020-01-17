# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_render_template]
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
        cat = cat[item]

    if cat.container != "catalog": # only render Intake catalogs
        return "<p>Only Intake catalogs will be rendered.</p>"

    return render_template("catalog.html", cat=cat,
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

# API Docs

The API docs are writtten in [API Blueprint](https://apiblueprint.org/) and compiled to HTML with [aglio](https://github.com/danielgtaylor/aglio/).

To update docs:

* Make changes to API Blueprints in `polling_stations/templates/api_docs/blueprints/`
* Install aglio: `npm install -g aglio`
* Recompile docs: `sudo npm install -g aglio and then to compile the docs to html we run aglio --theme-variables polling_stations/templates/api_docs/theme/dc.less -i polling_stations/templates/api_docs/blueprints/wheredoivote.apibp -o polling_stations/templates/api_docs/html/docs.html`
* Commit both the APIBP source the complied HTML to the repo.

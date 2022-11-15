# Installation

1. copy the zip file to `/usr/lib/ckan/default/src`
2. open ckan configuration file, development.ini or production.ini and add sergai_theme in ckan.plugins, so that your line should look like `ckan.plugins=plugin1 plugin2 sergai_theme`
3. cd `/usr/lib/ckan/default/src`
4. run `python setup.py install`
5. After this has completed successfully, add `sergai_theme` to ckan.plugins in ckan configuration file.




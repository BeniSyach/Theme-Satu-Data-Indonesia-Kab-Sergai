
![](./sergai-header.PNG)
# ckanext-sergai_theme



### Datasets Page
![](./sergai-datasets.PNG)

### Topics on front Page
![](./sergai-topics.PNG)

# Installation:
- copy the zip file to `/usr/lib/ckan/default/src`
- cd `/usr/lib/ckan/default/src`
- run ``` python setup.py install ```
- After this has completed successfully, add `sergai_theme` to ckan.plugins in ckan configuration file.

## Manually generating main.css
----------------------------

Run `sass ckanext/sergai_theme/public/css/sass/main.scss ckanext/sergai_theme/public/css/main.css`


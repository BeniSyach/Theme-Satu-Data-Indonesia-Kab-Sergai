from collections import OrderedDict

from ckan.common import config

import ckan.plugins as plugins
import ckan.plugins.toolkit as tk

# from ckan.lib.activity_streams import activity_stream_string_functions as activity_streams


def most_recent_datasets(num=3):
    """Return a list of recent datasets."""
    datasets = tk.get_action('package_search')({}, {
        'sort': 'metadata_modified desc',
        'fq': 'private:false',
        'rows': num
    })
    return datasets.get('results', [])


def most_popular_groups():
    '''Return a sorted list of the groups with the most datasets.'''
    # Get a list of all the site's groups from KP OpenData Portal, sorted by number of
    # datasets.
    groups = tk.get_action('group_list')(data_dict={'sort': 'package_count desc', 'all_fields': True})
    # Truncate the list to the 5 most popular groups only.
    groups = groups[:5]

    return groups


def dataset_count():
    """Return a count of all datasets"""
    result = tk.get_action('package_search')({}, {'rows': 1})
    return result['count']


def groups():
    """Return a list of groups"""
    return tk.get_action('group_list')({}, {'all_fields': True})


def groups_count():
    """Return a list of groups"""
    result = tk.get_action('package_search')({}, {'rows': 1})
    return result['count']

# def package_showcase_list(context):
#     return tk.get_action('ckanext_package_showcase_list')({}, {'package_id': context.pkg_dict['id']})

def ckan_site_url():
    return config.get('ckan.site_url', '').rstrip('/')

# monkeypatch activity streams to rename 'group' to 'topic'
# activity_streams['changed group'] = (
#     lambda c, a: tk._("{actor} updated the topic {group}")
# )
# activity_streams['deleted group'] = (
#     lambda c, a: tk._("{actor} deleted the topic {group}")
# )
# activity_streams['new group'] = (
#     lambda c, a: tk._("{actor} created the topic {group}")
# )

# # Add back activity types removed in the 'related'->'showcase' upgrade.
# # They'll be generic, but at least they won't crash.
# activity_streams['changed related item'] = (
#     lambda c, a: tk._("{actor} updated a related item.")
# )
# activity_streams['deleted related item'] = (
#     lambda c, a: tk._("{actor} deleted a related item.")
# )
# activity_streams['new related item'] = (
#     lambda c, a: tk._("{actor} created a related item.")
# )

class SergaiThemePlugin(plugins.SingletonPlugin):
    """OpenDataPhilly theme plugin."""
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.IRoutes)

    def dataset_facets(self, facets_dict, package_type):
        """Rename 'Groups' to 'Topics' in the list of facets shown on the search page"""
        new_facets_dict = OrderedDict()
        for key, value in facets_dict.items():
            new_facets_dict[key] = value
        if 'groups' in new_facets_dict:
            new_facets_dict['groups'] = tk._('Topics')
        return new_facets_dict

    def group_facets(self, facets_dict, group_type, package_type):
        if 'groups' in facets_dict:
            facets_dict['groups'] = tk._('Topics')
        return facets_dict

    def organization_facets(self, facets_dict, organization_type,
                            package_type):
        if 'groups' in facets_dict:
            facets_dict['groups'] = tk._('Topics')
        return facets_dict

    def update_config(self, config):
        """Register this plugin's template dir"""

        tk.add_template_directory(config, 'templates')

        # this adds directories to make public so we can include custom CSS
        # and javascript.
        # see http://docs.ckan.org/en/latest/theming/fanstatic.html
        tk.add_public_directory(config, 'public')
        tk.add_resource('fanstatic', 'sergai_theme')

    def get_helpers(self):
        """Register sergai_theme_* helper functions"""

        return {'sergai_theme_most_recent_datasets': most_recent_datasets,
                'sergai_theme_dataset_count': dataset_count,
                'sergai_theme_groups_count': groups_count,
                'sergai_theme_groups': groups,
                'ckan_site_url': ckan_site_url,
                'top_groups':most_popular_groups}

    def before_map(self, map):
        return map

    def after_map(self, map):
        return map

# This file is a part of MediaCoreSEO, Copyright 2010 Simple Station Inc.
#
# MediaCore is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MediaCore is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pylons import app_globals, tmpl_context
from tw.forms import ListFieldSet, TextField

from mediacore.lib.helpers import url_for
from mediacore.lib.i18n import N_, _
from mediacore.model import Media
from mediacore.model.meta import DBSession
from mediacore.model.settings import insert_settings
from mediacore.plugin import events
from mediacore.plugin.events import observes

SEO_SETTINGS = [
    u'seo_general_meta_description',
    u'seo_general_meta_keywords',
    u'seo_explore_page_title',
    u'seo_explore_meta_description',
    u'seo_explore_meta_keywords',
    u'seo_podcast_page_title',
    u'seo_podcast_meta_description',
    u'seo_podcast_meta_keywords',
    u'seo_category_page_title',
    u'seo_category_meta_description',
    u'seo_category_meta_keywords',
    u'seo_upload_page_title',
    u'seo_upload_meta_description',
    u'seo_upload_meta_keywords',
    u'seo_options_noindex_categories',
    u'seo_options_noindex_rss',
]

@observes(events.plugin_settings_links)
def add_settings_link():
    """Generate new links for the admin Settings menu.

    The :data:`mediacore.plugin.events.plugin_settings_links` event
    is defined as a :class:`mediacore.plugin.events.GeneratorEvent`
    which expects all observers to yield their content for use.

    """
    yield (_('Search Engine Optimization', domain='mediacore_seo'),
           url_for(controller='/seo/admin/settings'))

@observes(events.Environment.init_model)
def create_settings():
    """Insert plugin settings into the DataBase.

    By observing :attr:`mediacore.plugin.events.Environment.init_model`
    we can insert any settings we need for our plugin at model
    initialization time ensuring they will be available in the app.

    """
    insert_settings([(x, u'') for x in SEO_SETTINGS])

@observes(events.Admin.MediaForm)
def append_fields(form):
    """Append SEO fields to the Media form.

    :param form: An instance of :class:`~mediacore.forms.admin.MediaForm`

    A post_init method in the form class registers it as a
    :class:`~mediacore.plugin.events.admin.MediaForm` event. When the event
    is triggered all observers are notified and passed in the Media form.
    At this point, we can append any fields we like to the form.

    In this case we will be adding options to set the page title,
    meta description and meta keywords for the given media item.

    """
    f = ListFieldSet('seo', suppress_label=True, legend=N_('Media Specifc SEO', domain='mediacore_seo'),
        css_classes=['details_fieldset'],
        children=[
            TextField('page_title', label_text=N_('Page Title', domain='mediacore_seo')),
            TextField('meta_description', label_text=N_('Meta Description', domain='mediacore_seo')),
            TextField('meta_keywords', label_text=N_('Meta Keywords', domain='mediacore_seo')),
        ]
    )
    form.children.append(f)

@observes(events.Admin.MediaController.edit)
def populate_fields(**result):
    """Populate SEO fields on Edit Media form.

    When the :attr:`mediacore.plugin.events.Admin.MediaController.edit` event
    is triggered it receives the dict of values returned to the Edit Media form
    from :meth:`mediacore.controlers.admin.media.MediaController.edit`.
    We then load up all SEO values from the DB, and insert them into the
    media_values dict under the same fieldset name we defined in :meth:`append_fields`.

    :param result: A dict containing form values for the Media form
    :param type: dict
    :returns: An updated dict with our SEO form values
    :rtype: dict

    """
    media = result['media']
    seo = result['media_values'].setdefault('seo', {})
    seo.setdefault('page_title', media.meta.get('seo_page_title', None))
    seo.setdefault('meta_description', media.meta.get('seo_meta_description', None))
    seo.setdefault('meta_keywords', media.meta.get('seo_meta_keywords', None))
    return result

@observes(events.Admin.MediaController.save)
def save_fields(**result):
    """Save SEO settings to the database on a Media item save.

    When the :attr:`mediacore.plugin.events.Admin.MediaController.save`
    event is triggered it receives the dict of values returned by
    :meth:`mediacore.controllers.admin.media.MediaController.save`.

    The SEO values are extracted from tmpl_context.form_values and if
    a value was entered it is saved. If a valid setting was found, but
    it does not have a value, we remove it form the given media item.

    :param result: A dict of form values for the Media item
    :param type: dict
    :returns: A dict of form values for the Media item
    :rtpye: dict

    """

    media = Media.query.get(result['media_id'])
    for key, value in tmpl_context.form_values['seo'].iteritems():
        meta_key = u'seo_%s' % key
        if value:
            media.meta[meta_key] = value
        elif meta_key in media.meta:
            DBSession.delete(media._meta[meta_key])
    return result

@observes(events.page_title, appendleft=True)
def seo_title(category=None, media=None, podcast=None, upload=None, **kwargs):
    """Return SEO modified title for a given page.

    By observing the page_title event and appending to the left, we ensure
    our results take precedence over the standard MediaCore
    :func:`mediacore.lib.helpers.page_title` event observers that append
    to the right side of the observer deque.

    Based on how the page_title event was called, we will return the correct
    setting from the SEO settings if one exists. Otherwise we return None
    and the default value supplied to page_title will be used.

    :param category: Optional value that when set to 'all' will return the
        SEO setting for the category page.
    :type category: string or None

    :param media: Optional value that when set to 'all' will return the
        SEO setting for the Explore page. If, however a
        :class:`~mediacore.model.media.Media` instance is passed in, then
        the specific SEO value for that item will be returned.
    :type media: string or None

    :param podcast: Optional value that when set to 'all' will return the
        SEO setting for the Podcast page.
    :type media: string or None

    :param upload: Optional value that when set to 'all' will return the
        SEO setting for the Upload page.
    :type media: string or None

    :rtype: String or None

    """
    settings = app_globals.settings

    if category == 'all':
        setting = settings.get('seo_category_page_title', None)
    elif media == 'all':
        setting = settings.get('seo_explore_page_title', None)
    elif media:
        setting = media.meta.get('seo_page_title', None)
    elif podcast == 'all':
        setting = settings.get('seo_podcast_page_title', None)
    elif upload == 'all':
        setting = settings.get('seo_upload_page_title', None)
    else:
        return None

    if setting:
        return setting
    return None

@observes(events.meta_keywords, appendleft=True)
def seo_meta_keywords(category=None, media=None,
                      podcast=None, upload=None, **kwargs):
    """Return SEO modified meta keywords information for a page.

    Based on how the meta_keywords event was called, we will return the correct
    setting from the SEO settings if one exists. Otherwise we return None
    and the default value supplied to metakeywords will be used.

    We also have a General Meta Keywords SEO setting that will be used as a
    fallback if there is no specified Meta Keyword information passed into
    the meta_keywords event. If that value does not exist, we fallback to None.

    :param category: Optional value that when set to 'all' will return the
        SEO setting for the category page.
    :type category: string or None

    :param media: Optional value that when set to 'all' will return the
        SEO setting for the Explore page. If, however a
        :class:`~mediacore.model.media.Media` instance is passed in, then
        the specific SEO value for that item will be returned.
    :type media: string or None

    :param podcast: Optional value that when set to 'all' will return the
        SEO setting for the Podcast page.
    :type media: string or None

    :param upload: Optional value that when set to 'all' will return the
        SEO setting for the Upload page.
    :type media: string or None

    :rtype: String or None

    """
    settings = app_globals.settings
    general_meta = settings.get('seo_general_meta_keywords', None)
    if not general_meta:
        general_meta = None

    if category == 'all':
        setting = settings.get('seo_category_meta_keywords', general_meta)
    elif media == 'all':
        setting = settings.get('seo_explore_meta_keywords', general_meta)
    elif media:
        setting = media.meta.get('seo_meta_keywords', general_meta)
    elif podcast == 'all':
        setting = settings.get('seo_podcast_meta_keywords', general_meta)
    elif upload == 'all':
        setting = settings.get('seo_upload_meta_keywords', general_meta)
    else:
        return None

    if setting:
        return setting
    return None

@observes(events.meta_description, appendleft=True)
def seo_meta_description(category=None, media=None,
                         podcast=None, upload=None, **kwargs):
    """Return SEO modified meta description information for a page.

    Based on how the meta_description event was called, we will return the
    correct setting from the SEO settings if one exists. Otherwise we return
    None and the default value supplied to meta_description will be used.

    We also have a General Meta Description SEO setting that will be used as a
    fallback if there is no specified Meta Description information passed into
    the meta_keywords event. If that value does not exist, we fallback to None.

    :param category: Optional value that when set to 'all' will return the
        SEO setting for the category page.
    :type category: string or None

    :param media: Optional value that when set to 'all' will return the
        SEO setting for the Explore page. If, however a
        :class:`~mediacore.model.media.Media` instance is passed in, then
        the specific SEO value for that item will be returned.
    :type media: string or None

    :param podcast: Optional value that when set to 'all' will return the
        SEO setting for the Podcast page.
    :type media: string or None

    :param upload: Optional value that when set to 'all' will return the
        SEO setting for the Upload page.
    :type media: string or None

    :rtype: String or None

    """
    settings = app_globals.settings
    general_desc = settings.get('seo_general_meta_description', None)
    if not general_desc:
        general_desc = None

    if category == 'all':
        setting = settings.get('seo_category_meta_description', general_desc)
    elif media == 'all':
        setting = settings.get('seo_explore_meta_description', general_desc)
    elif media:
        setting = media.meta.get('seo_meta_description', general_desc)
    elif podcast == 'all':
        setting = settings.get('seo_podcast_meta_description', general_desc)
    elif upload == 'all':
        setting = settings.get('seo_upload_meta_description', general_desc)
    else:
        return None

    if setting:
        return setting
    return None

@observes(events.meta_robots_noindex, appendleft=True)
def seo_meta_robots(category=None, rss=None, **kwargs):
    """Return SEO modified Meta Robots information.

    We use inverse logic here, as the <meta robots> tag in our template
    contains a py:strip attribute so returning True will remove the tag,
    while returning False will display it.

    :param category: Optional value that when set to 'all' will return the
        inverse of the SEO setting in the database.

    :param rss: Optional value that when set to 'all' will return the
        inverse of the RSS NOSEO setting in the database.

    :rtype: Bool

    """
    settings = app_globals.settings

    if category == 'all':
        return not settings.get('seo_options_noindex_categories')
    elif rss:
        return not settings.get('seo_options_noindex_rss')
    else:
        return False

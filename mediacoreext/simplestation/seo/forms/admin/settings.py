# This file is a part of the SEO plugin for MediaCore CE, http://mediacorecommunity.org
# Copyright 2010-2013 MediaCore Inc., Felix Schwarz and other contributors.
# For the exact contribution history, see the git revision log.
# The source code contained in this file is licensed under the GPLv3 or
# (at your option) any later version.
# See LICENSE.txt in the main project directory, for more information.

from tw.forms import CheckBox, HiddenField
from tw.forms.validators import Bool

from mediacore.forms import ListFieldSet, ListForm, SubmitButton, TextField
from mediacore.lib.i18n import N_

class SEOSettingsForm(ListForm):
    template = 'admin/box-form.html'
    id = 'settings-form'
    css_class = 'form'
    submit_text = None
    fields = [
        ListFieldSet('general', suppress_label=True, legend=N_('General', domain='mediacore_seo'),
            css_classes=['details_fieldset'],
            children=[
                TextField('seo_general_meta_description',
                    label_text=N_('Site Meta Description', domain='mediacore_seo'),
                ),
                TextField('seo_general_meta_keywords',
                    label_text=N_('Site Meta Keywords', domain='mediacore_seo'),
                    help_text=N_('Comma Separated)', domain='mediacore_seo'),
                ),
            ],
        ),
        ListFieldSet('explore', suppress_label=True, legend=N_('Explore Page', domain='mediacore_seo'),
            css_classes=['details_fieldset'],
            children=[
                TextField('seo_explore_page_title',
                    label_text=N_('Page Title', domain='mediacore_seo'),
                ),
                TextField('seo_explore_meta_description',
                    label_text=N_('Meta Description', domain='mediacore_seo'),
                ),
                TextField('seo_explore_meta_keywords',
                    label_text=N_('Meta Keywords', domain='mediacore_seo'),
                    help_text=N_('(Comma Separated)', domain='mediacore_seo'),
                )
            ],
        ),
        ListFieldSet('podcast', suppress_label=True, legend=N_('Podcast Page', domain='mediacore_seo'),
            css_classes=['details_fieldset'],
            children=[
                TextField('seo_podcast_page_title',
                    label_text=N_('Page Title', domain='mediacore_seo'),
                ),
                TextField('seo_podcast_meta_description',
                    label_text=N_('Meta Description', domain='mediacore_seo'),
                ),
                TextField('seo_podcast_meta_keywords',
                    label_text=N_('Meta Keywords', domain='mediacore_seo'),
                    help_text=N_('(Comma Separated)', domain='mediacore_seo'),
                )
            ],
        ),
        ListFieldSet('category', suppress_label=True, legend=N_('Category Page', domain='mediacore_seo'),
            css_classes=['details_fieldset'],
            children=[
                TextField('seo_category_page_title',
                    label_text=N_('Page Title', domain='mediacore_seo'),
                ),
                TextField('seo_category_meta_description',
                    label_text=N_('Meta Description', domain='mediacore_seo'),
                ),
                TextField('seo_category_meta_keywords',
                    label_text=N_('Meta Keywords', domain='mediacore_seo'),
                    help_text=N_('(Comma Separated)', domain='mediacore_seo'),
                )
            ],
        ),
        ListFieldSet('upload', suppress_label=True, legend=N_('Upload Page', domain='mediacore_seo'),
            css_classes=['details_fieldset'],
            children=[
                TextField('seo_upload_page_title',
                    label_text=N_('Page Title', domain='mediacore_seo'),
                ),
                TextField('seo_upload_meta_description',
                    label_text=N_('Meta Description', domain='mediacore_seo'),
                ),
                TextField('seo_upload_meta_keywords',
                    label_text=N_('Meta Keywords', domain='mediacore_seo'),
                    help_text=N_('(Comma Separated)', domain='mediacore_seo'),
                )
            ],
        ),
        ListFieldSet('options', suppress_label=True, legend=N_('Options', domain='mediacore_seo'),
            css_classes=['details_fieldset'],
            children=[
                CheckBox('seo_options_noindex_categories',
                    label_text=N_('Enable NOINDEX for Categories', domain='mediacore_seo'),
                    validator=Bool(if_missing=''),
                ),
                CheckBox('seo_options_noindex_rss',
                    label_text=N_('Enable NOINDEX for RSS', domain='mediacore_seo'),
                    validator=Bool(if_missing=''),
                ),
                # XXX: Argh toscawidgets will mark the fieldset as invalid (missing)
                #      when neither of the above checkboxes are checked, unless
                #      we ensure some 'options' value is always passed.
                HiddenField('dummy_field', default='1'),
            ],
        ),
        SubmitButton('save', default=N_('Save', domain='mediacore_seo'), named_button=True,
            suppress_label=True, css_classes=['btn', 'btn-save']
        ),
    ]

# This file is a part of the SEO plugin for MediaCore CE, http://mediacorecommunity.org
# Copyright 2010-2013 MediaCore Inc., Felix Schwarz and other contributors.
# For the exact contribution history, see the git revision log.
# The source code contained in this file is licensed under the GPLv3 or
# (at your option) any later version.
# See LICENSE.txt in the main project directory, for more information.

from mediacore.lib.base import BaseSettingsController
from mediacore.lib.decorators import autocommit, expose, validate
from mediacore.lib.helpers import url_for

from mediacoreext.simplestation.seo.forms.admin.settings import SEOSettingsForm

seo_settings_form = SEOSettingsForm()

class SettingsController(BaseSettingsController):
    @expose('seo/admin/settings.html')
    def index(self, **kwargs):
        return self._display(form=seo_settings_form,
                             action=url_for(action='save'),
                             values=kwargs)

    @expose()
    @validate(seo_settings_form, error_handler=index)
    @autocommit
    def save(self, **kwargs):
        self._save(seo_settings_form, 'index', values=kwargs)

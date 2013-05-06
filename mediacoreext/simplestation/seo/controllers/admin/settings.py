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

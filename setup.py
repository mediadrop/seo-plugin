# This file is a part of the SEO plugin for MediaCore CE, http://mediacorecommunity.org
# Copyright 2010-2013 MediaCore Inc., Felix Schwarz and other contributors.
# For the exact contribution history, see the git revision log.
# The source code contained in this file is licensed under the GPLv3 or
# (at your option) any later version.
# See LICENSE.txt in the main project directory, for more information.

from setuptools import setup, find_packages

setup(
    name = 'MediaCore-SEO',
    version = '0.11dev',
    author = 'Simple Station Inc.',
    author_email = 'info@simplestation.com',
    description = 'A MediaCore plugin for SEO optimization through page Metadata.',
    
    packages=find_packages(),
    namespace_packages = ['mediacoreext'],
    include_package_data=True,    
    zip_safe = False,

    install_requires = [
        'MediaCore >= 0.11dev',
    ],
    entry_points = {
        'mediacore.plugin': ['seo = mediacoreext.simplestation.seo.mediacore_plugin'],
    },
    message_extractors = {'mediacoreext/simplestation/seo': [
        ('**.py', 'python', None),
        ('templates/**.html', 'genshi', {'template_class': 'genshi.template.markup:MarkupTemplate'}),
        ('public/**', 'ignore', None),
        ('tests/**', 'ignore', None),
    ]},
)

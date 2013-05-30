# This file is a part of the SEO plugin for MediaCore CE, http://mediacorecommunity.org
# Copyright 2010-2013 MediaCore Inc., Felix Schwarz and other contributors.
# For the exact contribution history, see the git revision log.
# The source code contained in this file is licensed under the GPLv3 or
# (at your option) any later version.
# See LICENSE.txt in the main project directory, for more information.
"""insert additional settings

The migration is a bit more complicated because older versions of the SEO plugin
just inserted the settings without any kind of DB versioning. If the settings
are already present in the database this migration just stamps an alembic
revision into the db.

This migration can not be run offline.

added: 2013-05-30 (v0.11dev)

Revision ID: 342f38dce484
Revises: None
Create Date: 2013-05-30 10:12:45.065149
"""

# revision identifiers, used by Alembic.
revision = '342f38dce484'
down_revision = None

from alembic import context
from alembic.op import execute, inline_literal
from sqlalchemy import Integer, Unicode, UnicodeText
from sqlalchemy import Column, MetaData,  Table

# -- table definition ---------------------------------------------------------
metadata = MetaData()
settings = Table('settings', metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('key', Unicode(255), nullable=False, unique=True),
    Column('value', UnicodeText),
    mysql_engine='InnoDB',
    mysql_charset='utf8',
)

# -- helpers ------------------------------------------------------------------
def insert_setting(key, value):
    execute(
        settings.insert().\
            values({
                'key': inline_literal(key),
                'value': inline_literal(value),
            })
    )

def delete_setting(key):
    execute(
        settings.delete().\
            where(settings.c.key==inline_literal(key))
    )
# -----------------------------------------------------------------------------


SEO_SETTINGS = [
    (u'seo_general_meta_description', u''),
    (u'seo_general_meta_keywords', u''),
    (u'seo_explore_page_title', u''),
    (u'seo_explore_meta_description', u''),
    (u'seo_explore_meta_keywords', u''),
    (u'seo_podcast_page_title', u''),
    (u'seo_podcast_meta_description', u''),
    (u'seo_podcast_meta_keywords', u''),
    (u'seo_category_page_title', u''),
    (u'seo_category_meta_description', u''),
    (u'seo_category_meta_keywords', u''),
    (u'seo_upload_page_title', u''),
    (u'seo_upload_meta_description', u''),
    (u'seo_upload_meta_keywords', u''),
    (u'seo_options_noindex_categories', u''),
    (u'seo_options_noindex_rss', u''),
]

def upgrade():
    if context.is_offline_mode():
        raise AssertionError('This migration can not be run in offline mode.')
    connection = context.get_context().connection
    
    for key, value in SEO_SETTINGS:
        query = settings.select(settings.c.key == key)
        result = connection.execute(query).first()
        if result is None:
            insert_setting(key, value)

def downgrade():
    for key, value in SEO_SETTINGS:
        delete_setting(key)

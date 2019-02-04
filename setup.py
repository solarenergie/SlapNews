#!/usr/bin/python3
# -*- encoding: utf-8 -*-
from setuptools import setup

setup(
	name='SlapNews',
	version='2.1',
	description='self learning news aggregator',
	url='https://github.com/solarenergie/SlapNews',
	license='GNU General Public License v3 (GPLv3)',
	install_requires=['feedparser', 'scikit-learn'],
	zip_safe=False,
	packages=['SlapNews'],
	entry_points={'console_scripts': ['read_news = SlapNews.read_news:main']},
	include_package_data=True
)

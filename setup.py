#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
import sys
import warnings
import subprocess

import gaefpdf
package_dir = 'gaefpdf'

# convert the README and format in restructured text (only when registering)
long_desc = ""
if os.path.exists("README.md"):
    try:
        cmd = ['pandoc', '--from=markdown', '--to=rst', 'README.md']
        long_desc = subprocess.check_output(cmd).decode("utf8")
    except Exception as e:
        warnings.warn("Exception when converting the README format: %s" % e)

setup(name='gaefpdf',
      version=gaefpdf.__version__,
      description='Simple PDF generation for Google App Engine.',
      long_description=long_desc,
      author='Olivier PLATHEY ported by Max. Modified by Lighthouse.',
      author_email='foss@lighthouseuk.net',
      maintainer = "Lighthouse",
      maintainer_email = "foss@lighthouseuk.net",
      url='https://github.com/LighthouseUK/gaepyfpdf',
      license='LGPLv3+',
      download_url="https://github.com/LighthouseUK/gaepyfpdf/tarball/%s" % gaefpdf.__version__,
      packages=['gaefpdf', ],
      package_dir={'gaefpdf': package_dir},
      package_data={'gaefpdf': ['font/*.ttf', 'font/*.txt']},
      classifiers = [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.5",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.2",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Operating System :: Other OS",
            "Topic :: Software Development :: Libraries :: PHP Classes",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Multimedia :: Graphics",
      ],
      keywords=["pdf", "unicode", "png", "jpg", "ttf", "gae", "google app engine"],
      )


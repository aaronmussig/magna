import os
import re
import sys

# Restrict to Python 3.8+
# scipy doesn't work on 3.11+
if sys.version_info < (3, 8) or sys.version_info >= (3, 11):
    sys.exit('Only Python [3.8, 3.11) is supported')

# Check setuptools is installed
try:
    from setuptools import setup, find_packages
except ImportError:
    sys.exit('Please install setuptools before installing this package.')

# Check setuptools_rust is installed
try:
    from setuptools_rust import Binding, RustExtension
except ImportError:
    sys.exit('Please install setuptools-rust before installing this package.')


# Read the long description from the README file
def readme():
    with open('README.md', encoding='utf-8') as f:
        return f.read()


def read_meta():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'magna/__init__.py')
    with open(path) as fh:
        hits = re.findall(r'__(\w+)__ ?= ?["\'](.+)["\']\n', fh.read())
    return {k: v for k, v in hits}


meta = read_meta()
setup(name=meta['title'],
      version=meta['version'],
      description=meta['description'],
      long_description=readme(),
      long_description_content_type='text/markdown',
      author=meta['author'],
      author_email=meta['author_email'],
      url=meta['url'],
      license=meta['license'],
      project_urls={
          'Bug Tracker': meta['bug_url'],
          'Documentation': meta['doc_url'],
          'Source Code': meta['src_url'],
      },
      entry_points={
          'console_scripts': [
              'magna = magna.__main__:app'
          ]
      },
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          'Natural Language :: English',
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Topic :: Scientific/Engineering :: Bio-Informatics",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      packages=find_packages(),
      include_package_data=True,
      install_requires=['tqdm', 'pandas>=1.1.0', 'pyarrow', 'numpy',
                        'dendropy', 'biopython', 'scipy', 'typer[all]',
                        'rq', 'redis'],
      setup_requires=['setuptools-rust', 'setuptools', 'wheel'],
      python_requires='>=3.8',
      rust_extensions=[RustExtension("magna.magna", binding=Binding.PyO3, debug=False)],
      data_files=[("", ["LICENSE"])],
      zip_safe=False,
      )

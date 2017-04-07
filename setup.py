from setuptools import find_packages, setup

# PyPI only supports nicely-formatted README files in reStructuredText.
# Newsapps seems to prefer Markdown.  Use a version of the pattern from
# https://coderwall.com/p/qawuyq/use-markdown-readme-s-in-python-modules
# to convert the Markdown README to rst if the pypandoc package is
# present.
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError, OSError):
    long_description = open('README.md').read()

# Load the version from the version module
exec(open('represent_statements/version.py').read())

setup(
        name='represent_statements',
        version=__version__,
        author='Geoff Hing',
        author_email='geoffhing@gmail.com',
        url='https://github.com/ghing/scrape-represent-statements',
        description="Scrape congressional statements from ProPublica's Represent app",
        long_description=long_description,
        packages=find_packages(exclude=["tests", "tests.*"]),
        include_package_data=True,
        install_requires=[
            'SQLAlchemy',
            'requests',
            'lxml',
            'cssselect',
            'alembic',
            'psycopg2',
        ],
        tests_require=[
        ],
        test_suite='tests',
        entry_points={
            'console_scripts': [
                'scrape_statements=represent_statements.cli.scrape_statements:main',
                'load_statements=represent_statements.cli.load_statements:main',
                'export_statements=represent_statements.cli.export_statements:main',
                'last_statement_date=represent_statements.cli.last_statement_date:main',
                'last_created_date=represent_statements.cli.last_created_date:main',
            ],
        },
        keywords='propublica congress',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
        ],
)

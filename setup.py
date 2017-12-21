from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='boxel',
    version='0.1.0',
    author='rucas',
    author_email='lucas.rondenet@wk.com',
    packages=find_packages(),
    include_package_data=True,
    license='LICENSE',
    install_requires=required,
    entry_points='''
        [console_scripts]
        boxel=boxel.boxel:cli
    ''',
)

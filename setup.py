from setuptools import setup, find_packages

with open('README.md') as f:
    readme_text = f.read()

with open('LICENSE') as f:
    license_text = f.read()

setup(
    name='GeCO',
    version='0.0.1',
    description='Generator for Combinatorial Optimization',
    long_description=readme_text,
    url='https://github.com/CharJon/GeCO',
    license=license_text,
    packages=find_packages(exclude=('tests', 'docs', 'data', 'notebooks')),
)

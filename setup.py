from setuptools import setup, find_packages

setup(
    name='splunk-soar-rest',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
    ],
    python_requires='>=3.7',
)

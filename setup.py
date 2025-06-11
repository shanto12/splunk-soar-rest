
---

### File 5: `setup.py`

This file is the build script for `setuptools`. It tells `setuptools` about your package (such as the name and version) as well as which code files to include.

```python
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="splunk-soar-rest",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python client for the Splunk SOAR REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/splunk-soar-rest",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests>=2.20.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.6',
)

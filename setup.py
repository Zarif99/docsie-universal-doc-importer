import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="docsie_universal_importer",
    version="0.0.1",
    author="Likalo Limited",
    author_email="hello@docsie.io",
    description="This is an open source implementation of docsie_universal_importer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LikaloLLC/docsie-universal-doc-importer",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.5, <4",
    install_requires=[
        'swag_auth',
    ],
    include_package_data=True,
    setup_requires=["wheel"]
)

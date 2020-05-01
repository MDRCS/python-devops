from setuptools import setup, find_packages

setup(
    name="hello-world",
    version="0.0.1",
    author="Example Author",
    author_email="author@example.com",
    url="example.com",
    description="A hello-world example package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
"""
    The newly created tar.gz file is an installable package!
    This package can now be uploaded to PyPI for others to install directly from it.
    By following the version schema, it allows installers to ask for a specific version (0.0.1 in this case),
    and the extra metadata passed into the setup() function enables other tools to discover it and show information about it,
    such as the author, description, and version.”

"""
if __name__ == "__main__":
    print("my name is mamadou")

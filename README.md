# python-devops

### - Command-line:
    + ps -eo pcpu,pid,user,args | sort -r | head -10 (CPU Utility)
    - htop - an interactive process viewer
    + brew install htop
    + htop (launch command)
    + h (for help) s (for setup) > (for sorting) t (show as a tree)
    + pip list --format=json (display dict of packages and versions)

### - Version Control - Compatibility
    + pip install setuptools twine
    + python3 setup.py sdist (Create a dist folder to manage Versions [major].[minor].[patch])

    --> The newly created tar.gz file is an installable package!
    This package can now be uploaded to PyPI for others to install directly from it.
    By following the version schema, it allows installers to ask for a specific version (0.0.1 in this case),
    and the extra metadata passed into the setup() function enables other tools to discover it and show information about it,
    such as the author, description, and version.”

    + pip install dist/hello-world-0.0.1.tar.gz

    - Upload Package to PyPI:
    + login
    + twine upload --repository-url https://test.pypi.org/legacy/ \
        dist/hello-world-0.0.1.tar.gz

    - Install the package from the source:
    + python3 -m pip install --index-url https://test.pypi.org/simple/hello-world

    - Automate Upload package to PyPI:
    + make deploy-pypi

    +  Changelog (linux only)
    - sudo apt-get install devscripts
    -  $ export DEBEMAIL="alfredo@example.com"
       $ export DEBFULLNAME="Alfredo Deza”
    -  dch --package "hello-world" --create -v "0.0.1" \
       -D stable "New upstream release” (Produce Changelog)


### - Naming Convention
    + {region}.{prod|staging|dev}.{server_name}
    Ex: us-west2.dev.server1

### - Testing:
    + pytest testing_params.py

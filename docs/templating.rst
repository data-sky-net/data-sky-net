.. _ds_project_deploy_wizard_templating_ref:

Project Wizard templating
-------------------------

Wizard uses `Cookiecutter <https://github.com/cookiecutter/cookiecutter>`_ Python tool for building new projects.

Cookiecutter template is located in wizard repository, ``data-sky/project_template`` directory and contains:

- Files and directories used by Cookiecutter directly, such as ``cookiecutter.json`` and ``hooks`` (read more in `Cookiecutter documentation <https://cookiecutter.readthedocs.io/>`_);
- ``{{cookiecutter.project_name}}`` - a template directory for your projects. Files from here will be added to project automatically.

Basic cookiecutter template for data-sky project contains:

.. code-block:: none

    .
    ├── configs                - configuration files for data-sky services;
    ├── docker_volumes         - Docker volumes which are used by services, e.g. for saving logs;
    ├── modules                - Python toolkits used in project;
    ├── .env                   - .env file used as template for project .env;
    ├── .gitignore             - standard .gitignore file;
    ├── docker-compose         - compose for starting project services.

Back to :ref:`installation and configuration page <ds_project_deploy_wizard_install_ref>`.


After changing any settings in template you should rebuild and install data-sky package with:

.. code-block:: bash

    poetry install --no-root --no-dev
    poetry build
    pip install dist/data-sky-0.1.0.tar.gz

Installation
------------


Wizard is a Python-package which is built with `Poetry <https://python-poetry.org/>`_ packaging manager. This repo contains ``pyproject.toml`` and ``poetry.lock`` files for installing necessary Python-dependencies.

For build package locally, run:

.. code-block:: bash

    poetry install --no-root --no-dev
    poetry build
    pip install dist/data-sky-0.1.0.tar.gz


Check if data-sky package is built successfully and see a list of data-sky available commands:

.. code-block:: bash

    data-sky --help


For installing ang starting development environment:

.. code-block:: bash

    poetry install --no-root
    poetry shell

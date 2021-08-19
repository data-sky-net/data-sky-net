ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}

RUN pip install --upgrade pip
RUN pip install poetry
COPY pyproject.toml /ds_project_deploy_wizard/
COPY poetry.lock /ds_project_deploy_wizard/

WORKDIR /ds_project_deploy_wizard
RUN poetry install --no-root

COPY ./ /ds_project_deploy_wizard

RUN poetry build
RUN pip install dist/data-sky-0.1.0.tar.gz
CMD ["/bin/bash"]

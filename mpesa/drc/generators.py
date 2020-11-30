"""Handle Generation of rendered XML Content from Jinja2 Templates."""
from jinja2 import Environment, PackageLoader
import jinja2.meta

import logging

LOGGER = logging.getLogger(__name__)

Loader = PackageLoader(package_name="mpesa", package_path="drc/templates")
environment = Environment(loader=Loader)


def get_variables(template_name, logger=LOGGER):
    """Return all undeclared variables in template."""
    template_source = environment.loader.get_source(
        environment, template_name)[0]
    parsed_content_ast = environment.parse(template_source)
    variables = jinja2.meta.find_undeclared_variables(parsed_content_ast)
    logger.debug(f"{__name__}.get_variables({template_name}) = {variables}.")
    return list(variables)


def generate_login(context: dict) -> str:
    """Return generated template string using context."""
    template = environment.get_template("login_request.xml")
    content = template.render(context)
    print(content)
    return content


def generate_c2b(context: dict) -> str:
    """Return generated template string using context."""
    template = environment.get_template("c2b_request.xml")
    content = template.render(context)
    print(content)
    return content


def generate_b2c(context: dict) -> str:
    """Return generated template string using context."""
    template = environment.get_template("b2c_request.xml")
    content = template.render(context)
    print(content)
    return content


def generate_c2b_ack(context: dict) -> str:
    """Return generated template string using context."""
    template = environment.get_template("c2b_ack_response.xml")
    content = template.render(context)
    print(content)
    return content


def generate_b2c_ack(context: dict) -> str:
    """Return generated template string using context."""
    template = environment.get_template("b2c_ack_response.xml")
    content = template.render(context)
    print(content)
    return content


def generate_w2b(context: dict) -> str:
    """Return generated template string using context."""
    template = environment.get_template("w2b_request.xml")
    content = template.render(context)
    print(content)
    return content


if __name__ == "__main__":
    print(environment.list_templates())
    print()
    for template in environment.list_templates():
        print(f"{template} Variables.")
        print("\n".join(get_variables(template)))
        print()

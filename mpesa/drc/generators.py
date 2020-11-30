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


if __name__ == "__main__":
    print(environment.list_templates())
    print()
    for template in environment.list_templates():
        print(f"{template} Variables.")
        print("\n".join(get_variables(template)))
        print()

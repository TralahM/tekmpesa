"""Portalsdk subpackage.

.. note::
    This module provides an abstraction over the API mechanisms of three submodules.
    Namely:

    - :mod:`mpesa.tanzania`

    - :mod:`mpesa.ghana`

    - :mod:`mpesa.mozambique`

    It Provides the following classes which are used internally in the
    implementation of the respective API classes.

    - :class:`mpesa.portalsdk.APIContext`

    - :class:`mpesa.portalsdk.APIMethodType`

    - :class:`mpesa.portalsdk.APIRequest`

    - :class:`mpesa.portalsdk.APIResponse`

"""
from mpesa.portalsdk.api import APIContext
from mpesa.portalsdk.api import APIMethodType
from mpesa.portalsdk.api import APIRequest
from mpesa.portalsdk.api import APIResponse

__all__ = [
    "APIContext",
    "APIMethodType",
    "APIRequest",
    "APIResponse",
]

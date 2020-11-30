"""Mozambique MPESA SDK Implementation."""
from mpesa.portalsdk import (
    APIContext,
    APIMethodType,
    APIRequest,
)


class API:
    """Mozambique Market API.

    :param public_key: Public key from developers portal.
    :type public_key: str.
    :param api_key: API key from developers portal.
    :type api_key: str.
    :param env: Environment either ``"sandbox"`` or ``"production"``, defaults ``"sandbox"``.
    :type env: str, optional.

    **Attributes.**

    .. attribute:: sandbox_host

        The sandbox api host ``"api.sandbox.vm.co.mz"``.

    .. attribute:: live_host

        The live/openapi api host ``"api.vm.co.mz"``.


    **Methods.**


    """

    def __init__(
        self,
        public_key: str,
        api_key: str,
        env: str = "sandbox",
    ):
        """Initialize API."""
        self.public_key = public_key
        self.api_key = api_key
        self.env = env
        self.sandbox_host = "api.sandbox.vm.co.mz"
        self.live_host = "api.vm.co.mz"

    def _pretty(self, body: dict) -> dict:
        """Return new dict from body with output_ key prefix trimmed."""
        pretty = {k.replace("output_", ""): v for k, v in body.items()}
        return pretty

    def _create_context(
        self,
        path: str = "",
        method_type: APIMethodType = APIMethodType.GET,
        port: int = 80,
        headers: dict = {"Origin": "*"},
        params: dict = {},
    ):
        """Return APIContext."""
        api_context = APIContext()
        api_context.public_key = self.public_key
        api_context.api_key = self.api_key
        if self.env == "production":
            api_context.address = self.live_host
        else:
            api_context.address = self.sandbox_host
        api_context.ssl = True
        api_context.port = port
        api_context.path = path
        api_context.method_type = method_type
        [api_context.add_header(k, v) for k, v in headers.items()]
        [api_context.add_parameter(k, v) for k, v in params.items()]
        return api_context

    def _execute(self, context: APIContext):
        """Return result.body after makiing request with `context`.

        :raises: ``Exception``.
        :return: API Response body.
        :rtype: ``APIResponse``.
        """
        api_request = APIRequest(context)
        result = None
        try:
            result = api_request.execute()
        except Exception as e:
            raise e
        if not result:
            raise Exception("API Call Failed to get Result. Please Check.")
        # print(result.body)  # , type(result.body))-->dict
        return result.body

    @property
    def bearer_token(self):
        """Return Bearer Token."""
        api_request = APIRequest(self._create_context())
        return api_request.create_bearer_token()

    def c2b(
        self,
        Amount: str,
        CustomerMSISDN: str,
        ServiceProviderCode: str,
        TransactionReference: str,
        ThirdPartyReference: str,
        **kwargs,
    ):
        """C2B Single Stage.

        :param Amount: Amount.
        :type Amount: str.
        :param CustomerMSISDN: Customer MSISDN.
        :type CustomerMSISDN: str.
        :param ServiceProviderCode: Service Provider Code.
        :type ServiceProviderCode: str.
        :param ThirdPartyReference: Third Party Reference.
        :type ThirdPartyReference: str.
        :param TransactionReference: Transaction Reference.
        :type TransactionReference: str.

        :returns: A dictionary object from the C2B API.
        :rtype: dict.

        :Example:

        .. code-block:: json

            {
              "ConversationID": "d3502e5958774f7ba228d83d0d689761",
              "ResponseCode": "INS-0",
              "ResponseDesc": "Request processed successfully",
              "TransactionID": "49XCD123F6",
              "ThirdPartyReference": "asv02e5958774f7ba228d83d0d689761"
            }
        """
        path = "/ipg/v1x/c2bPayment/singleStage/"
        port = 18352
        method_type = APIMethodType.POST
        params = {
            "input_Amount": Amount,
            "input_CustomerMSISDN": CustomerMSISDN,
            "input_ServiceProviderCode": ServiceProviderCode,
            "input_ThirdPartyReference": ThirdPartyReference,
            "input_TransactionReference": TransactionReference,
        }
        context = self._create_context(
            path,
            method_type,
            port=port,
            params=params,
        )
        body = self._execute(context)
        return self._pretty(body)

    def b2c(
        self,
        Amount: str,
        CustomerMSISDN: str,
        ServiceProviderCode: str,
        TransactionReference: str,
        ThirdPartyReference: str,
        **kwargs,
    ):
        """B2C Single Stage.

        :param Amount: Amount.
        :type Amount: str.
        :param CustomerMSISDN: Customer MSISDN.
        :type CustomerMSISDN: str.
        :param ServiceProviderCode: Service Provider Code.
        :type ServiceProviderCode: str.
        :param ThirdPartyReference: Third Party Reference.
        :type ThirdPartyReference: str.
        :param TransactionReference: Transaction Reference.
        :type TransactionReference: str.

        :returns: A dictionary object from the C2B API.
        :rtype: dict.

        :Example:

        .. code-block:: json

            {
              "ConversationID": "d3502e5958774f7ba228d83d0d689761",
              "ResponseCode": "INS-0",
              "ResponseDesc": "Request processed successfully",
              "TransactionID": "49XCD123F6",
              "ThirdPartyReference": "asv02e5958774f7ba228d83d0d689761"
            }
        """
        path = "/ipg/v1x/b2cPaymemt/"
        port = 18345
        method_type = APIMethodType.POST
        params = {
            "input_Amount": Amount,
            "input_CustomerMSISDN": CustomerMSISDN,
            "input_ServiceProviderCode": ServiceProviderCode,
            "input_ThirdPartyReference": ThirdPartyReference,
            "input_TransactionReference": TransactionReference,
        }
        context = self._create_context(
            path,
            method_type,
            port=port,
            params=params,
        )
        body = self._execute(context)
        return self._pretty(body)

    def b2b(
        self,
        Amount: str,
        PrimaryPartyCode: str,
        ReceiverPartyCode: str,
        ThirdPartyReference: str,
        TransactionReference: str,
        **kwargs,
    ):
        """B2B Single Stage.

        :param Amount: Amount.
        :type Amount: str.
        :param ReceiverPartyCode: Receiver Party Code.
        :type ReceiverPartyCode: str.
        :param PrimaryPartyCode: Primary Party Code.
        :type PrimaryPartyCode: str.
        :param ThirdPartyReference: Third Party Reference.
        :type ThirdPartyReference: str.
        :param TransactionReference: Transaction Reference.
        :type TransactionReference: str.

        :returns: A dictionary object from the B2B API.
        :rtype: dict.

        :Example:

        .. code-block:: json

            {
              "ConversationID": "d3502e5958774f7ba228d83d0d689761",
              "ResponseCode": "INS-0",
              "ResponseDesc": "Request processed successfully",
              "TransactionID": "49XCD123F6",
              "ThirdPartyReference": "asv02e5958774f7ba228d83d0d689761"
            }

        """
        path = "/ipg/v1x/b2bPayment/"
        port = 18349
        method_type = APIMethodType.POST
        params = {
            "input_Amount": Amount,
            "input_PrimaryPartyCode": PrimaryPartyCode,
            "input_ReceiverPartyCode": ReceiverPartyCode,
            "input_ThirdPartyReference": ThirdPartyReference,
            "input_TransactionReference": TransactionReference,
        }
        context = self._create_context(
            path,
            method_type,
            port=port,
            params=params,
        )
        body = self._execute(context)
        return self._pretty(body)

    def reverse(
        self,
        ReversalAmount: str,
        TransactionID: str,
        ServiceProviderCode: str,
        SecurityCredential: str,
        InitiatorIdentifier: str,
        ThirdPartyReference: str,
        **kwargs,
    ):
        """Reversal API.

        The Reversal API is used to reverse a successful transaction.
        Using the Transaction ID of a previously successful transaction, the OpenAPI will withdraw the funds from the recipient party’s mobile money wallet and revert the funds to the mobile money wallet of the initiating party of the original transaction.

        :param ReversalAmount: Reversal Amount.
        :type ReversalAmount: str.
        :param ServiceProviderCode: Service Provider Code.
        :type ServiceProviderCode: str.
        :param SecurityCredential: Security Credentials.
        :type SecurityCredential: str.
        :param InitiatorIdentifier: Initiator Identifier.
        :type InitiatorIdentifier: str.
        :param ThirdPartyReference: Third Party Reference.
        :type ThirdPartyReference: str.
        :param TransactionID: Transaction ID.
        :type TransactionID: str.

        :returns: A dictionary object from the Reversal API.
        :rtype: dict.

        :Example:

        .. code-block:: json

            {
              "ResponseCode": "INS-0",
              "ResponseDesc": "Request processed successfully",
              "TransactionID": "49XCD123F6",
              "ConversationID": "d3502e5958774f7ba228d83d0d689761",
              "ThirdPartyReference": "asv02e5958774f7ba228d83d0d689761"
            }
        """
        path = "/ipg/v1x/reversal/"
        port = 18354
        method_type = APIMethodType.PUT
        params = {
            "input_InitiatorIdentifier": InitiatorIdentifier,
            "input_ReversalAmount": ReversalAmount,
            "input_ServiceProviderCode": ServiceProviderCode,
            "input_SecurityCredential": SecurityCredential,
            "input_ThirdPartyReference": ThirdPartyReference,
            "input_TransactionID": TransactionID,
        }
        context = self._create_context(
            path,
            method_type,
            port=port,
            params=params,
        )
        body = self._execute(context)
        return self._pretty(body)

    def transaction_status(
        self,
        QueryReference: str,
        ServiceProviderCode: str,
        ThirdPartyReference: str,
        **kwargs,
    ):
        """Query Transaction Status.

        The Query Transaction Status API call is used to query the status of the transaction that has been initiated.

        :param QueryReference: Query Reference.
        :type QueryReference: str.
        :param ServiceProviderCode: Service Provider Code.
        :type ServiceProviderCode: str.
        :param ThirdPartyReference: Third Party Reference.
        :type ThirdPartyReference: str.

        :returns: A dictionary object from the QueryTransactionStatus API.
        :rtype: dict.

        :Example:

        .. code-block:: json

            {
              "ConversationID": "d3502e5958774f7ba228d83d0d689761",
              "ResponseCode": "INS-0",
              "ResponseDesc": "Request processed successfully",
              "ResponseTransactionStatus": "Completed",
              "ThirdPartyReference": "asv02e5958774f7ba228d83d0d689761"
            }
        """
        path = "/ipg/v1x/queryTransactionStatus/"
        port = 18353
        method_type = APIMethodType.GET
        params = {
            "input_QueryReference": QueryReference,
            "input_ServiceProviderCode": ServiceProviderCode,
            "input_ThirdPartyReference": ThirdPartyReference,
        }
        context = self._create_context(
            path,
            method_type,
            port=port,
            params=params,
        )
        body = self._execute(context)
        return self._pretty(body)

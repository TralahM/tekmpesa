"""Tanzania MPESA SDK Implementation."""
from time import sleep
from mpesa.portalsdk import (
    APIContext,
    APIMethodType,
    APIRequest,
)


class API:
    """Tanzania Market API.

    :param public_key: Public key from developers portal.
    :type public_key: str.
    :param api_key: API key from developers portal.
    :type api_key: str.
    :param env: Environment either ``"sandbox"`` or ``"production"``, defaults ``"sandbox"``.
    :type env: str, optional.

    **Attributes.**

    .. attribute:: sandbox_path

        The sandbox prefix path ``"/sandbox/ipg/v2/vodacomTZN/"``.

    .. attribute:: live_path

        The live/openapi prefix path ``"/openapi/ipg/v2/vodacomTZN/"``.

    .. attribute:: Currency

        The Currency used for this API. default ``"TZS"``.

    .. attribute:: Country

        The Country used for this API. default ``"TZN"``.

    **Methods.**


    """

    def __init__(
        self,
        public_key: str,
        api_key: str,
        env: str = "sandbox",
    ):
        """Initialize API.

        **Arguments.**

        :param public_key: Public key from developers portal.
        :type public_key: str.
        :param api_key: API key from developers portal.
        :type api_key: str.
        :param env: Environment either **sandbox** or **production**, defaults **sandbox**.
        :type env: str, optional.
        """
        self.public_key = public_key
        self.api_key = api_key
        self.env = env
        self.sandbox_path = "/sandbox/ipg/v2/vodacomTZN/"
        self.live_path = "/openapi/ipg/v2/vodacomTZN/"
        self.Country = "TZN"
        self.Currency = "TZS"

    def _pretty(self, body: dict) -> dict:
        """Return new dict from body with output_ key prefix trimmed."""
        pretty = {k.replace("output_", ""): v for k, v in body.items()}
        return pretty

    def _create_context(
        self,
        path: str,
        method_type: APIMethodType,
        api_key: str,
        headers: dict = {"Origin": "*"},
        params: dict = {},
    ):
        """Return APIContext."""
        api_context = APIContext()
        api_context.public_key = self.public_key
        api_context.address = "openapi.m-pesa.com"
        api_context.ssl = True
        api_context.port = 443
        api_context.api_key = api_key
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
    def session_id(self) -> str:
        """Return session_id.

        :return: The sessionID to be used in subsequent requests.
        :rtype: str.
        """
        endpoint = "getSession/"
        method_type = APIMethodType.GET
        api_key = self.api_key
        if self.env == "production":
            path = self.live_path + endpoint
        else:
            path = self.sandbox_path + endpoint
        body = self._execute(
            self._create_context(
                path,
                method_type,
                api_key=api_key,
            )
        )
        return self._pretty(body)["SessionID"]

    def c2b(
        self,
        Amount: str,
        CustomerMSISDN: str,
        ServiceProviderCode: str,
        ThirdPartyConversationID: str,
        TransactionReference: str,
        PurchasedItemsDesc: str,
        **kwargs,
    ):
        """C2B Single Stage.

        :param Amount: Amount.
        :type Amount: str.
        :param CustomerMSISDN: Customer MSISDN.
        :type CustomerMSISDN: str.
        :param ServiceProviderCode: Service Provider Code.
        :type ServiceProviderCode: str.
        :param ThirdPartyConversationID: Third Party Conversation ID.
        :type ThirdPartyConversationID: str.
        :param TransactionReference: Transaction Reference.
        :type TransactionReference: str.
        :param PurchasedItemsDesc: Purchased Items Description.
        :type PurchasedItemsDesc: str.


        :returns: A dictionary object from the C2B API.
        :rtype: dict.

        :Example:

        .. code-block:: json

            {
              "ConversationID": "d3502e5958774f7ba228d83d0d689761",
              "ResponseCode": "INS-0",
              "ResponseDesc": "Request processed successfully",
              "TransactionID": "49XCD123F6",
              "ThirdPartyConversationID": "asv02e5958774f7ba228d83d0d689761"
            }
        """
        method_type = APIMethodType.POST
        endpoint = "c2bPayment/singleStage/"
        params = {
            "input_Amount": Amount,
            "input_Country": self.Country,
            "input_Currency": self.Currency,
            "input_CustomerMSISDN": CustomerMSISDN,
            "input_ServiceProviderCode": ServiceProviderCode,
            "input_ThirdPartyConversationID": ThirdPartyConversationID,
            "input_TransactionReference": TransactionReference,
            "input_PurchasedItemsDesc": PurchasedItemsDesc,
        }
        if self.env == "production":
            path = self.live_path + endpoint
        else:
            path = self.sandbox_path + endpoint
        context = self._create_context(
            path,
            method_type,
            api_key=self.session_id,
            params=params,
        )
        # SessionID can take up to 30 seconds to become 'live' in the system
        # and will be invalid until it is
        sleep(30)
        body = self._execute(context)
        return self._pretty(body)

    def b2c(
        self,
        Amount: str,
        CustomerMSISDN: str,
        ServiceProviderCode: str,
        ThirdPartyConversationID: str,
        TransactionReference: str,
        PaymentItemsDesc: str,
        **kwargs,
    ):
        """B2C Single Stage.

        The B2C API Call is used as a standard business-to-customer funds disbursement.

        Funds from the business account's wallet will be deducted and paid to the mobile money wallet of the customer.

        Use cases for the B2C includes:

        - Salary payments

        - Funds transfers from business

        - Charity pay-out

        :param Amount: Amount.
        :type Amount: str.
        :param CustomerMSISDN: Customer MSISDN.
        :type CustomerMSISDN: str.
        :param ServiceProviderCode: Service Provider Code.
        :type ServiceProviderCode: str.
        :param ThirdPartyConversationID: Third Party Conversation ID.
        :type ThirdPartyConversationID: str.
        :param TransactionReference: Transaction Reference.
        :type TransactionReference: str.
        :param PaymentItemsDesc: Payment Items Description.
        :type PaymentItemsDesc: str.

        :returns: A dictionary object from the B2C API.
        :rtype: dict.

        :Example:

        .. code-block:: json

            {
              "ConversationID": "d3502e5958774f7ba228d83d0d689761",
              "ResponseCode": "INS-0",
              "ResponseDesc": "Request processed successfully",
              "TransactionID": "49XCD123F6",
              "ThirdPartyConversationID": "asv02e5958774f7ba228d83d0d689761"
            }
        """
        params = {
            "input_Amount": Amount,
            "input_Country": self.Country,
            "input_Currency": self.Currency,
            "input_CustomerMSISDN": CustomerMSISDN,
            "input_ServiceProviderCode": ServiceProviderCode,
            "input_ThirdPartyConversationID": ThirdPartyConversationID,
            "input_TransactionReference": TransactionReference,
            "input_PaymentItemsDesc": PaymentItemsDesc,
        }
        endpoint = "b2cPayment/"
        method_type = APIMethodType.POST
        if self.env == "production":
            path = self.live_path + endpoint
        else:
            path = self.sandbox_path + endpoint
        context = self._create_context(
            path,
            method_type,
            api_key=self.session_id,
            params=params,
        )
        # SessionID can take up to 30 seconds to become 'live' in the system
        # and will be invalid until it is
        sleep(30)
        body = self._execute(context)
        return self._pretty(body)

    def b2b(
        self,
        Amount: str,
        PrimaryPartyCode: str,
        ReceiverPartyCode: str,
        ThirdPartyConversationID: str,
        TransactionReference: str,
        PurchasedItemsDesc: str,
        **kwargs,
    ):
        """B2B Single Stage.

        The B2B API Call is used for business-to-business transactions.

        Funds from the business' mobile money wallet will be deducted and transferred to the mobile money wallet of the other business.

        Use cases for the B2B includes:

        - Stock purchases

        - Bill payment

        - Adhoc payment

        :param Amount: Amount.
        :type Amount: str.
        :param ReceiverPartyCode: Receiver Party Code.
        :type ReceiverPartyCode: str.
        :param PrimaryPartyCode: Primary Party Code.
        :type PrimaryPartyCode: str.
        :param ThirdPartyConversationID: Third Party Conversation ID.
        :type ThirdPartyConversationID: str.
        :param TransactionReference: Transaction Reference.
        :type TransactionReference: str.
        :param PurchasedItemsDesc: Purchased Items Description.
        :type PurchasedItemsDesc: str.

        :returns: A dictionary object from the B2B API.
        :rtype: dict.

        :Example:

        .. code-block:: json

            {
              "ConversationID": "d3502e5958774f7ba228d83d0d689761",
              "ResponseCode": "INS-0",
              "ResponseDesc": "Request processed successfully",
              "TransactionID": "49XCD123F6",
              "ThirdPartyConversationID": "asv02e5958774f7ba228d83d0d689761"
            }

        """
        endpoint = "b2bPayment/"
        method_type = APIMethodType.POST
        params = {
            "input_Amount": Amount,
            "input_Country": self.Country,
            "input_Currency": self.Currency,
            "input_PrimaryPartyCode": PrimaryPartyCode,
            "input_ReceiverPartyCode": ReceiverPartyCode,
            "input_ThirdPartyConversationID": ThirdPartyConversationID,
            "input_TransactionReference": TransactionReference,
            "input_PurchasedItemsDesc": PurchasedItemsDesc,
        }
        if self.env == "production":
            path = self.live_path + endpoint
        else:
            path = self.sandbox_path + endpoint
        context = self._create_context(
            path,
            method_type,
            api_key=self.session_id,
            params=params,
        )
        # SessionID can take up to 30 seconds to become 'live' in the system
        # and will be invalid until it is
        sleep(30)
        body = self._execute(context)
        return self._pretty(body)

    def reverse(
        self,
        ReversalAmount: str,
        ServiceProviderCode: str,
        ThirdPartyConversationID: str,
        TransactionID: str,
        **kwargs,
    ):
        """Reversal API.

        The Reversal API is used to reverse a successful transaction.
        Using the Transaction ID of a previously successful transaction, the OpenAPI will withdraw the funds from the recipient party’s mobile money wallet and revert the funds to the mobile money wallet of the initiating party of the original transaction.

        :param ReversalAmount: Reversal Amount.
        :type ReversalAmount: str.
        :param ServiceProviderCode: Service Provider Code.
        :type ServiceProviderCode: str.
        :param ThirdPartyConversationID: Third Party Conversation ID.
        :type ThirdPartyConversationID: str.
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
              "ThirdPartyConversationID": "asv02e5958774f7ba228d83d0d689761"
            }
        """
        endpoint = "reversal/"
        method_type = APIMethodType.PUT
        params = {
            "input_Country": self.Country,
            "input_ReversalAmount": ReversalAmount,
            "input_ServiceProviderCode": ServiceProviderCode,
            "input_ThirdPartyConversationID": ThirdPartyConversationID,
            "input_TransactionID": TransactionID,
        }
        if self.env == "production":
            path = self.live_path + endpoint
        else:
            path = self.sandbox_path + endpoint
        context = self._create_context(
            path,
            method_type,
            api_key=self.session_id,
            params=params,
        )
        # SessionID can take up to 30 seconds to become 'live' in the system
        # and will be invalid until it is
        sleep(30)
        body = self._execute(context)
        return self._pretty(body)

    def transaction_status(
        self,
        QueryReference: str,
        ServiceProviderCode: str,
        ThirdPartyConversationID: str,
        **kwargs,
    ):
        """Query Transaction Status.

        The Query Transaction Status API call is used to query the status of the transaction that has been initiated.

        :param ServiceProviderCode: Service Provider Code.
        :type ServiceProviderCode: str.
        :param ThirdPartyConversationID: Third Party Conversation ID.
        :type ThirdPartyConversationID: str.
        :param QueryReference: Query Reference.
        :type QueryReference: str.

        :returns: A dictionary object from the QueryTransactionStatus API.
        :rtype: dict.

        :Example:

        .. code-block:: json

            {
              "ConversationID": "d3502e5958774f7ba228d83d0d689761",
              "ResponseCode": "INS-0",
              "ResponseDesc": "Request processed successfully",
              "ResponseTransactionStatus": "Completed",
              "ThirdPartyConversationID": "asv02e5958774f7ba228d83d0d689761"
            }
        """
        endpoint = "queryTransactionStatus/"
        method_type = APIMethodType.GET
        params = {
            "input_QueryReference": QueryReference,
            "input_ServiceProviderCode": ServiceProviderCode,
            "input_ThirdPartyConversationID": ThirdPartyConversationID,
            "input_Country": self.Country,
        }
        if self.env == "production":
            path = self.live_path + endpoint
        else:
            path = self.sandbox_path + endpoint
        context = self._create_context(
            path,
            method_type,
            api_key=self.session_id,
            params=params,
        )
        # SessionID can take up to 30 seconds to become 'live' in the system
        # and will be invalid until it is
        sleep(30)
        body = self._execute(context)
        return self._pretty(body)

    def direct_debit_create(
        self,
        AgreedTC: str,
        CustomerMSISDN: str,
        ServiceProviderCode: str,
        ThirdPartyConversationID: str,
        ThirdPartyReference: str,
        StartRangeOfDays: str,
        EndRangeOfDays: str,
        ExpiryDate: str,
        FirstPaymentDate: str,
        Frequency: str,
        **kwargs,
    ):
        """Direct Debit Create API.

        Direct Debits are payments in M-Pesa that are initiated by the Payee alone without any Payer interaction, but permission must first be granted by the Payer.

        The granted permission from the Payer to Payee is commonly termed a ‘Mandate’, and M-Pesa must hold details of this Mandate.

        The Direct Debit API set allows an organisation to get the initial consent of their customers to create the Mandate that allows the organisation to debit customer's account at an agreed frequency and amount for services rendered.

        After the initial consent, the debit of the account will not involve any customer interaction.

        The Direct Debit feature makes use of the following API calls:

        - Create a Direct Debit mandate

        - Pay a mandate

        The customer is able to view and cancel the Direct Debit mandate from G2 menu accessible via USSD menu or the Smartphone Application.

        :param AgreedTC: The customer agreed to the terms and conditions.
            Can only use 1 or 0.
        :type AgreedTC: str.
        :param CustomerMSISDN: Customer MSISDN.
        :type CustomerMSISDN: str.
        :param ServiceProviderCode: Service Provider Code.
        :type ServiceProviderCode: str.
        :param ThirdPartyConversationID: Third Party Conversation ID.
        :type ThirdPartyConversationID: str.
        :param ThirdPartyReference: Third Party Reference.
        :type ThirdPartyReference: str.
        :param StartRangeOfDays: The start range of days in the month.
        :type StartRangeOfDays: str, optional.
        :param EndRangeOfDays: The end range of days in the month.
        :type EndRangeOfDays: str, optional.
        :param ExpiryDate: The expiry date of the Mandate.
        :type ExpiryDate: str, optional.
        :param FirstPaymentDate: The Start date of the Mandate.
        :type FirstPaymentDate: str, optional.
        :param Frequency: The frequency of the payments.
        :type Frequency: str, optional.

        .. csv-table:: List of Possible Frequency Values.
            :header: "Frequency", "Description"
            :widths: 12, 25

                "01", "Once off"
                "02", "Daily"
                "03", "Weekly"
                "04", "Monthly"
                "05", "Quarterly"
                "06", "Half Yearly"
                "07", "Yearly"
                "08", "On Demand"

        :returns: A dictionary object from the DirectDebitCreation API.
        :rtype: dict.

        :Example:

        .. code-block:: json

            {
              "ResponseCode": "INS-0",
              "ResponseDesc": "Request processed successfully",
              "TransactionReference": "vgisfyn4b22w6tmqjftatq75lyuie6vc",
              "ConversationID": "51a1d9191acc4674ab1dfd321a24ba20",
              "ThirdPartyConversationID": "AAA6d1f9391a0052de0b5334a912jbsj1j2kk"
            }
        """
        endpoint = "directDebitCreation/"
        method_type = APIMethodType.POST
        params = {
            "input_AgreedTC": AgreedTC,
            "input_Country": self.Country,
            "input_CustomerMSISDN": CustomerMSISDN,
            "input_EndRangeOfDays": EndRangeOfDays,
            "input_ExpiryDate": ExpiryDate,
            "input_FirstPaymentDate": FirstPaymentDate,
            "input_Frequency": Frequency,
            "input_ServiceProviderCode": ServiceProviderCode,
            "input_StartRangeOfDays": StartRangeOfDays,
            "input_ThirdPartyConversationID": ThirdPartyConversationID,
            "input_ThirdPartyReference": ThirdPartyReference,
        }
        if self.env == "production":
            path = self.live_path + endpoint
        else:
            path = self.sandbox_path + endpoint
        context = self._create_context(
            path,
            method_type,
            api_key=self.session_id,
            params=params,
        )
        # SessionID can take up to 30 seconds to become 'live' in the system
        # and will be invalid until it is
        sleep(30)
        body = self._execute(context)
        return self._pretty(body)

    def direct_debit_payment(
        self,
        Amount: str,
        CustomerMSISDN: str,
        ServiceProviderCode: str,
        ThirdPartyConversationID: str,
        ThirdPartyReference: str,
        **kwargs,
    ):
        """Direct Debit Payment.

        The Direct Debit API set allows an organisation to get the initial consent of their customers to create the Mandate that allows the organisation to debit customer's account at an agreed frequency and amount for services rendered.

        After the initial consent, the debit of the account will not involve any customer interaction.

        The Direct Debit feature makes use of the following API calls:

        - Create a Direct Debit mandate

        - Pay a mandate

        The customer is able to view and cancel the Direct Debit mandate from G2 menu accessible via USSD menu or the Smartphone Application.

        :param Amount: Amount.
        :type Amount: str.
        :param CustomerMSISDN: Customer MSISDN.
        :type CustomerMSISDN: str.
        :param ServiceProviderCode: Service Provider Code.
        :type ServiceProviderCode: str.
        :param ThirdPartyConversationID: Third Party Conversation ID.
        :type ThirdPartyConversationID: str.
        :param ThirdPartyReference: Third Party Reference.
        :type ThirdPartyReference: str.

        :returns: A dictionary object from the DirectDebitPayment API.
        :rtype: dict.

        :Example:

        .. code-block:: json

            {
              "ResponseCode": "INS-0",
              "ResponseDesc": "Request processed successfully",
              "TransactionReference": "vgisfyn4b22w6tmqjftatq75lyuie6vc",
              "ConversationID": "51a1d9191acc4674ab1dfd321a24ba20",
              "ThirdPartyConversationID": "AAA6d1f9391a0052de0b5334a912jbsj1j2kk"

            }

        """
        endpoint = "directDebitPayment/"
        method_type = APIMethodType.POST
        params = {
            "input_Amount": Amount,
            "input_Country": self.Country,
            "input_Currency": self.Currency,
            "input_CustomerMSISDN": CustomerMSISDN,
            "input_ServiceProviderCode": ServiceProviderCode,
            "input_ThirdPartyConversationID": ThirdPartyConversationID,
            "input_ThirdPartyReference": ThirdPartyReference,
        }
        if self.env == "production":
            path = self.live_path + endpoint
        else:
            path = self.sandbox_path + endpoint
        context = self._create_context(
            path,
            method_type,
            api_key=self.session_id,
            params=params,
        )
        # SessionID can take up to 30 seconds to become 'live' in the system
        # and will be invalid until it is
        sleep(30)
        body = self._execute(context)
        return self._pretty(body)

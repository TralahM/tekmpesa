"""Ghana MPESA API."""
from time import sleep
from mpesa.portalsdk import (
    APIContext,
    APIMethodType,
    APIRequest,
)


class API:
    """Ghana Openapi Market API."""

    def __init__(
        self,
        public_key: str,
        api_key: str,
        env: str = "sandbox",
    ):
        """Initialize API.

        Arguments.
        -----------

        :param `public_key`: Public key from developers portal.
        :param `api_key`: API key from developers portal.
        :param `env`: Environment either **sandbox** or **production**.
        """
        self.public_key = public_key
        self.api_key = api_key
        self.env = env
        self.sandbox_path = "/sandbox/ipg/v2/vodafoneGHA/"
        self.live_path = "/openapi/ipg/v2/vodafoneGHA/"

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
        """Return result.body after makiing request with `context`."""
        api_request = APIRequest(context)
        result = None
        try:
            result = api_request.execute()
        except Exception as e:
            raise e
        if not result:
            raise Exception("API Call Failed to get Result. Please Check.")
        print(result.status_code)
        # print(result.body)  # , type(result.body))-->dict
        return result.body

    @property
    def session_id(self):
        """Return session_id."""
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
        return body["output_SessionID"]

    def c2b(
        self,
        Amount: str,
        CustomerMSISDN: str,
        ServiceProviderCode: str,
        ThirdPartyConversationID: str,
        TransactionReference: str,
        PurchasedItemsDesc: str,
        Country: str = "GHA",
        Currency: str = "GHS",
    ):
        """C2B Single Stage.

        .. code-block:: json

            {
              "output_ConversationID": "d3502e5958774f7ba228d83d0d689761",
              "output_ResponseCode": "INS-0",
              "output_ResponseDesc": "Request processed successfully",
              "output_TransactionID": "49XCD123F6",
              "output_ThirdPartyConversationID": "asv02e5958774f7ba228d83d0d689761"
            }
        """
        method_type = APIMethodType.POST
        endpoint = "c2bPayment/singleStage/"
        params = {
            "input_Amount": Amount,
            "input_Country": Country,
            "input_Currency": Currency,
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
        return body

    def b2c(
        self,
        Amount: str,
        CustomerMSISDN: str,
        ServiceProviderCode: str,
        ThirdPartyConversationID: str,
        TransactionReference: str,
        PaymentItemsDesc: str,
        Country: str = "GHA",
        Currency: str = "GHS",
    ):
        """B2C Single Stage.

        .. code-block:: json

            {
              "output_ConversationID": "d3502e5958774f7ba228d83d0d689761",
              "output_ResponseCode": "INS-0",
              "output_ResponseDesc": "Request processed successfully",
              "output_TransactionID": "49XCD123F6",
              "output_ThirdPartyConversationID": "asv02e5958774f7ba228d83d0d689761"
            }
        """
        params = {
            "input_Amount": Amount,
            "input_Country": Country,
            "input_Currency": Currency,
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
        return body

    def b2b(
        self,
        Amount: str,
        PrimaryPartyCode: str,
        ReceiverPartyCode: str,
        ThirdPartyConversationID: str,
        TransactionReference: str,
        PurchasedItemsDesc: str,
        Country: str = "GHA",
        Currency: str = "GHS",
    ):
        """B2B Single Stage.

        .. code-block:: json

            {
              "output_ConversationID": "d3502e5958774f7ba228d83d0d689761",
              "output_ResponseCode": "INS-0",
              "output_ResponseDesc": "Request processed successfully",
              "output_TransactionID": "49XCD123F6",
              "output_ThirdPartyConversationID": "asv02e5958774f7ba228d83d0d689761"
            }

        """
        endpoint = "b2bPayment/"
        method_type = APIMethodType.POST
        params = {
            "input_Amount": Amount,
            "input_Country": Country,
            "input_Currency": Currency,
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
        return body

    def reversal(
        self,
        ReversalAmount: str,
        ServiceProviderCode: str,
        ThirdPartyConversationID: str,
        TransactionID: str,
        Country: str = "GHA",
    ):
        """Reversal API.

        .. code-block:: json

            {
              "output_ResponseCode": "INS-0",
              "output_ResponseDesc": "Request processed successfully",
              "output_TransactionID": "49XCD123F6",
              "output_ConversationID": "d3502e5958774f7ba228d83d0d689761",
              "output_ThirdPartyConversationID": "asv02e5958774f7ba228d83d0d689761"
            }
        """
        endpoint = "reversal/"
        method_type = APIMethodType.PUT
        params = {
            "input_Country": Country,
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
        return body

    def transaction_status(
        self,
        QueryReference: str,
        ServiceProviderCode: str,
        ThirdPartyConversationID: str,
        Country: str = "GHA",
    ):
        """Query Transaction Status.

        .. code-block:: json

            {
              "output_ConversationID": "d3502e5958774f7ba228d83d0d689761",
              "output_ResponseCode": "INS-0",
              "output_ResponseDesc": "Request processed successfully",
              "output_ResponseTransactionStatus": "Completed",
              "output_ThirdPartyConversationID": "asv02e5958774f7ba228d83d0d689761"
            }
        """
        endpoint = "queryTransactionStatus/"
        method_type = APIMethodType.GET
        params = {
            "input_QueryReference": QueryReference,
            "input_ServiceProviderCode": ServiceProviderCode,
            "input_ThirdPartyConversationID": ThirdPartyConversationID,
            "input_Country": Country,
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
        return body

    def direct_debit_create(
        self,
        AgreedTC: str,
        CustomerMSISDN: str,
        EndRangeOfDays: str,
        ExpiryDate: str,
        FirstPaymentDate: str,
        Frequency: str,
        ServiceProviderCode: str,
        StartRangeOfDays: str,
        ThirdPartyConversationID: str,
        ThirdPartyReference: str,
        Country: str = "GHS",
    ):
        """Direct Debit Create API.

        .. code-block::json

            {
              "output_ResponseCode": "INS-0",
              "output_ResponseDesc": "Request processed successfully",
              "output_TransactionReference": "vgisfyn4b22w6tmqjftatq75lyuie6vc",
              "output_ConversationID": "51a1d9191acc4674ab1dfd321a24ba20",
              "output_ThirdPartyConversationID": "AAA6d1f9391a0052de0b5334a912jbsj1j2kk"
            }
        """
        endpoint = "directDebitCreation/"
        method_type = APIMethodType.POST
        params = {
            "input_AgreedTC": AgreedTC,
            "input_Country": Country,
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
        return body

    def direct_debit_payment(
        self,
        Amount: str,
        CustomerMSISDN: str,
        ServiceProviderCode: str,
        ThirdPartyConversationID: str,
        ThirdPartyReference: str,
        Country: str = "GHA",
        Currency: str = "GHS",
    ):
        """Direct Debit Payment.

        .. code-block:: json

            {
              "output_ResponseCode": "INS-0",
              "output_ResponseDesc": "Request processed successfully",
              "output_TransactionReference": "vgisfyn4b22w6tmqjftatq75lyuie6vc",
              "output_ConversationID": "51a1d9191acc4674ab1dfd321a24ba20",
              "output_ThirdPartyConversationID": "AAA6d1f9391a0052de0b5334a912jbsj1j2kk"

            }

        """
        endpoint = "directDebitPayment/"
        method_type = APIMethodType.POST
        params = {
            "input_Amount": Amount,
            "input_Country": Country,
            "input_Currency": Currency,
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
        return body

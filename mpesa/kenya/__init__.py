"""Kenya MPESA SDK Implementation."""

import datetime
import base64
import requests
from requests.auth import HTTPBasicAuth

__all__ = [
    "API",
]

__author__ = "Tralah M Brian"
__email__ = "musyoki.brian@tralahtek.com"
__github__ = "https://github.com/TralahM"


class API:
    """Kenya's Daraja MPESA API.

    :param env:  The target environment defaults ``"sandbox"`` ``"sandbox"`` or ``"production"``.
    :type env: str
    :param app_key: The *app_key* from developers portal.
    :type app_key: str
    :param app_secret: The *app_secret* from developers portal.
    :type app_secret: str

    **Attributes**

    .. attribute:: sandbox_url

        The sandbox environment host url "https://sandbox.safaricom.co.ke"

    .. attribute:: live_url

        The live/production environment host url "https://api.safaricom.co.ke"


    **Methods.**


    """

    def __init__(
        self,
        env: str = "sandbox",
        app_key: str = None,
        app_secret: str = None,
    ):
        """Initialize API.

        :param env:  The target environment. *sandbox* or *production*.
        :type env: str
        :param app_key: The *app_key* from developers portal.
        :type app_key: str
        :param app_secret: The *app_secret* from developers portal.
        :type app_secret: str
        """
        self.env = env
        self.app_key = app_key
        self.app_secret = app_secret
        self.sandbox_url = "https://sandbox.safaricom.co.ke"
        self.live_url = "https://api.safaricom.co.ke"

    @property
    def authentication_token(self):
        """Return Authentication Token."""
        return self.authenticate()

    def authenticate(self):
        """To make Mpesa API calls, you will need to authenticate your app.

        This method is used to fetch the access token required by Mpesa.
        Mpesa supports client_credentials grant type.

        To authorize your API calls to Mpesa, you will need a Basic Auth over HTTPS authorization token.

        The Basic Auth string is a base64 encoded string of your app's client key and client secret.


        :return: `access_token`  This token is to be used with the Bearer header for further API calls to Mpesa.
        :rtype: str

        """
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        authenticate_uri = "/oauth/v1/generate?grant_type=client_credentials"
        authenticate_url = "{0}{1}".format(
            base_safaricom_url, authenticate_uri)
        try:
            r = requests.get(
                authenticate_url, auth=HTTPBasicAuth(
                    self.app_key, self.app_secret)
            )
        except Exception:
            r = requests.get(
                authenticate_url,
                auth=HTTPBasicAuth(self.app_key, self.app_secret),
                verify=False,
            )
        return r.json()["access_token"]

    def b2b(
        self,
        initiator: str = None,
        security_credential: str = None,
        command_id: str = None,
        sender_identifier_type: str = None,
        receiver_identifier_type: str = None,
        amount: str = None,
        party_a: str = None,
        party_b: str = None,
        remarks: str = None,
        account_reference: str = None,
        queue_timeout_url: str = None,
        result_url: str = None,
    ):
        """Uses the B2B API to transact from one company to another.


        :param initiator: Username used to authenticate the transaction.
        :type initiator: str

        :param security_credential: Generate from developer portal
        :type security_credential: str

        :param command_id: Options:

            - BusinessPayBill,

            - BusinessBuyGoods,

            - DisburseFundsToBusiness,

            - BusinessToBusinessTransfer,

            - BusinessTransferFromMMFToUtility,

            - BusinessTransferFromUtilityToMMF,

            - MerchantToMerchantTransfer,

            - MerchantTransferFromMerchantToWorking,

            - MerchantServicesMMFAccountTransfer,

            - AgencyFloatAdvance

        :type command_id: str

        :param sender_identifier_type: ``2`` for Till Number,
            ``4`` for organization shortcode.
        :type sender_identifier_type: str

        :param receiver_identifier_type: ``2`` for Till Number,
            ``4`` for organization shortcode.
        :type receiver_identifier_type: str

        :param amount: Amount.
        :type amount: str

        :param party_a: Sender shortcode.
        :type party_a: str

        :param party_b: Receiver shortcode.
        :type party_b: str

        :param remarks: Remarks.
        :type remarks: str

        :param account_reference: Use if doing paybill to banks etc.
        :type account_reference: str

        :param queue_timeout_url: The url that handles information of timed out
            transactions.
        :type queue_timeout_url: str

        :param result_url: The url that receives results from M-Pesa api call.
        :type result_url: str


        :return: Dict object of

            - OriginatorConverstionID (str): The unique request ID for tracking a transaction.

            - ConversationID (str): The unique request ID returned by mpesa for each request made

            - ResponseDescription (str): Response Description message

        :rtype: dict

        """

        payload = {
            "Initiator": initiator,
            "SecurityCredential": security_credential,
            "CommandID": command_id,
            "SenderIdentifierType": sender_identifier_type,
            "RecieverIdentifierType": receiver_identifier_type,
            "Amount": amount,
            "PartyA": party_a,
            "PartyB": party_b,
            "Remarks": remarks,
            "AccountReference": account_reference,
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url,
        }
        headers = {
            "Authorization": "Bearer {0}".format(self.authentication_token),
            "Content-Type": "application/json",
        }
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(
            base_safaricom_url, "/mpesa/b2b/v1/paymentrequest")
        try:
            r = requests.post(saf_url, headers=headers, json=payload)
        except Exception:
            r = requests.post(saf_url, headers=headers,
                              json=payload, verify=False)
        return r.json()

    def b2c(
        self,
        initiator_name: str = None,
        security_credential: str = None,
        command_id: str = None,
        amount: str = None,
        party_a: str = None,
        party_b: str = None,
        remarks: str = None,
        queue_timeout_url: str = None,
        result_url: str = None,
        occassion: str = None,
    ):
        """This method uses Mpesa's B2C API to transact between an M-Pesa short code to a phone number registered on M-Pesa..

        :param initiator_name: Username used to authenticate the transaction.
        :param security_credential: Generate from developer portal
        :param command_id: Options:

            - SalaryPayment,

            - BusinessPayment,

            - PromotionPayment.

        :param amount: Amount.
        :param party_a: Organization/MSISDN making the transaction

            - Shortcode (6 digits)

            - MSISDN (12 digits).

        :param party_b: MSISDN receiving the transaction (12 digits).
        :param remarks: Comments that are sent along with the
            transaction(maximum 100 characters).
        :param account_reference: Use if doing paybill to banks etc.
        :param queue_timeout_url: The url that handles information of timed
            out transactions.
        :param result_url: The url that receives results from M-Pesa api call.
        :param ocassion: occasion.
        :type initiator_name: str
        :type security_credential: str
        :type command_id: str
        :type amount: str
        :type party_a: str
        :type party_b: str
        :type remarks: str
        :type account_reference: str
        :type queue_timeout_url: str
        :type result_url: str
        :type ocassion: str


        :return: Dict object of

            - `OriginatorConverstionID` (str): The unique request ID for tracking a transaction.

            - `ConversationID` (str): The unique request ID returned by mpesa for each request made

            - `ResponseDescription` (str): Response Description message
        :rtype: dict

        :Example:

        .. code-block:: json

            {
            "ConversationID": "AG_20180326_00005ca7f7c21d608166",
            "OriginatorConversationID": "12363-1328499-6",
            "ResponseCode": "0",
            "ResponseDescription": "Accept the service request successfully."
            }

        """

        payload = {
            "InitiatorName": initiator_name,
            "SecurityCredential": security_credential,
            "CommandID": command_id,
            "Amount": amount,
            "PartyA": party_a,
            "PartyB": party_b,
            "Remarks": remarks,
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url,
            "Occassion": occassion,
        }
        headers = {
            "Authorization": "Bearer {0}".format(self.authentication_token),
            "Content-Type": "application/json",
        }
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(
            base_safaricom_url, "/mpesa/b2c/v1/paymentrequest")
        try:
            r = requests.post(saf_url, headers=headers, json=payload)
        except Exception:
            r = requests.post(saf_url, headers=headers,
                              json=payload, verify=False)
        return r.json()

    def balance(
        self,
        initiator: str = None,
        security_credential: str = None,
        command_id: str = None,
        party_a: str = None,
        identifier_type: str = None,
        remarks: str = None,
        queue_timeout_url: str = None,
        result_url: str = None,
    ):
        """This method uses Mpesa's Account Balance API to to enquire the balance on an M-Pesa BuyGoods (Till Number).


        :param initiator: Username used to authenticate the transaction.
        :param security_credential: Generate from developer portal.
        :param command_id: AccountBalance.
        :param party_a: Till number being queried.
        :param identifier_type: Type of organization receiving the transaction.

            .. csv-table:: Identifier Type sOptions
                :header: "identifier_type", "description"
                :widths: 15, 35

                1 , "MSISDN"
                2 , "Till Number"
                4 , "Organization short code"

        :param remarks: Comments that are sent along with the transaction(maximum 100 characters).
        :param queue_timeout_url: The url that handles information of timed out transactions.
        :param result_url: The url that receives results from M-Pesa api call.
        :type initiator: str
        :type security_credential: str
        :type command_id: str
        :type party_a: str
        :type identifier_type: str
        :type remarks: str
        :type queue_timeout_url: str
        :type result_url: str



        :return: Dict object of

            - `OriginatorConverstionID` (str): The unique request ID for tracking a transaction.

            - `ConversationID` (str): The unique request ID returned by mpesa for each request made

            - `ResponseDescription` (str): Response Description message
        :rtype: dict


        """

        payload = {
            "Initiator": initiator,
            "SecurityCredential": security_credential,
            "CommandID": command_id,
            "PartyA": party_a,
            "IdentifierType": identifier_type,
            "Remarks": remarks,
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url,
        }
        headers = {
            "Authorization": "Bearer {0}".format(self.authentication_token),
            "Content-Type": "application/json",
        }
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(
            base_safaricom_url, "/mpesa/accountbalance/v1/query")
        try:
            r = requests.post(saf_url, headers=headers, json=payload)
        except Exception:
            r = requests.post(saf_url, headers=headers,
                              json=payload, verify=False)
        return r.json()

    def c2b_register_url(
        self,
        shortcode: str = None,
        response_type: str = None,
        confirmation_url: str = None,
        validation_url: str = None,
    ):
        """This method uses Mpesa's C2B API to register validation and confirmation URLs on M-Pesa.


        :param shortcode: The short code of the organization.
        :param response_type: Default response type for timeout.
            Incase a tranaction times out, Mpesa will by default ``"Complete"`` or ``"Cancel"`` the transaction.
        :param confirmation_url: Confirmation URL for the client.
        :param validation_url: Validation URL for the client.
        :type shortcode: str
        :type response_type: str
        :type confirmation_url: str
        :type validation_url: str



        :return: Dict object of

            - `OriginatorConversationID` (str): The unique request ID for tracking a transaction.

            - `ConversationID` (str): The unique request ID returned by mpesa for each request made

            - `ResponseDescription` (str): Response Description message
        :rtype: dict

        :Example:

        .. code-block:: json

            {
              "ConversationID": "",
              "OriginatorCoversationID": "",
              "ResponseDescription": "success"
            }

        """

        payload = {
            "ShortCode": shortcode,
            "ResponseType": response_type,
            "ConfirmationURL": confirmation_url,
            "ValidationURL": validation_url,
        }
        headers = {
            "Authorization": "Bearer {0}".format(self.authentication_token),
            "Content-Type": "application/json",
        }
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(
            base_safaricom_url, "/mpesa/c2b/v1/registerurl")
        try:
            r = requests.post(saf_url, headers=headers, json=payload)
        except Exception:
            r = requests.post(saf_url, headers=headers,
                              json=payload, verify=False)
        return r.json()

    def c2b_simulate(
        self,
        shortcode: str = None,
        command_id: str = None,
        amount: str = None,
        msisdn: str = None,
        bill_ref_number: str = None,
    ):
        """This method uses Mpesa's C2B API to simulate a C2B transaction.

        :param shortcode: The short code of the organization.
        :param command_id: Unique command for each transaction type.

            - CustomerPayBillOnline

            - CustomerBuyGoodsOnline.

        :param amount: The amount being transacted
        :param msisdn: Phone number (msisdn) initiating the transaction MSISDN(12 digits)
        :param bill_ref_number: Optional
        :type shortcode: str
        :type command_id: str
        :type amount: str
        :type msisdn: str
        :type bill_ref_number: str

        :return: Dict object of

            - `OriginatorConverstionID` (str): The unique request ID for tracking a transaction.

            - `ConversationID` (str): The unique request ID returned by mpesa for each request made

            - `ResponseDescription` (str): Response Description message
        :rtype: dict
        :Example:

        .. code-block:: json

            {
              "ConversationID": "AG_20180324_000066530b914eee3f85",
              "OriginatorCoversationID": "25344-885903-1",
              "ResponseDescription": "Accept the service request successfully."
            }


        """

        payload = {
            "ShortCode": shortcode,
            "CommandID": command_id,
            "Amount": amount,
            "Msisdn": msisdn,
            "BillRefNumber": bill_ref_number,
        }
        headers = {
            "Authorization": "Bearer {0}".format(self.authentication_token),
            "Content-Type": "application/json",
        }
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(base_safaricom_url, "/mpesa/c2b/v1/simulate")
        try:
            r = requests.post(saf_url, headers=headers, json=payload)
        except Exception:
            r = requests.post(saf_url, headers=headers,
                              json=payload, verify=False)
        return r.json()

    def lnmo_stkpush(
        self,
        business_shortcode: str = None,
        passcode: str = None,
        amount: str = None,
        callback_url: str = None,
        reference_code: str = None,
        phone_number: str = None,
        description: str = None,
    ):
        """This method uses Mpesa's Express API to initiate online payment on behalf of a customer..


        :param business_shortcode: The short code of the organization.
        :param passcode: Get from developer portal
        :param amount: The amount being transacted
        :param callback_url: A CallBack URL is a valid secure URL that is used to receive notifications from M-Pesa API.
        :param reference_code: Account Reference: This is an Alpha-Numeric parameter that is defined by your system as an Identifier of the transaction for CustomerPayBillOnline transaction type.
        :param phone_number: The Mobile Number to receive the STK Pin Prompt.
        :param description: This is any additional information/comment that can be sent along with the request from your system. MAX 13 characters
        :type business_shortcode: str
        :type passcode: str
        :type amount: str
        :type callback_url: str
        :type reference_code: str
        :type phone_number: str
        :type description: str

        :return: Dict object of

            - `CustomerMessage` (str):

            - `CheckoutRequestID` (str):

            - `ResponseDescription` (str):

            - `MerchantRequestID` (str):

            - `ResponseCode` (str):
        :rtype: dict
        :Example:

        .. code-block:: json

            {
               "MerchantRequestID": "25353-1377561-4",
               "CheckoutRequestID": "ws_CO_26032018185226297",
               "ResponseCode": "0",
               "ResponseDescription": "Success. Request accepted for processing",
               "CustomerMessage": "Success. Request accepted for processing"
            }

        """

        time = (
            str(datetime.datetime.now())
            .split(".")[0]
            .replace("-", "")
            .replace(" ", "")
            .replace(":", "")
        )
        password = "{0}{1}{2}".format(
            str(business_shortcode), str(passcode), time)
        encoded = base64.b64encode(bytes(password, encoding="utf8"))
        payload = {
            "BusinessShortCode": business_shortcode,
            "Password": encoded.decode("utf-8"),
            "Timestamp": time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": int(phone_number),
            "PartyB": business_shortcode,
            "PhoneNumber": int(phone_number),
            "CallBackURL": callback_url,
            "AccountReference": reference_code,
            "TransactionDesc": description,
        }
        headers = {
            "Authorization": "Bearer {0}".format(self.authentication_token),
            "Content-Type": "application/json",
        }
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(
            base_safaricom_url, "/mpesa/stkpush/v1/processrequest"
        )
        try:
            r = requests.post(saf_url, headers=headers, json=payload)
        except Exception:
            r = requests.post(saf_url, headers=headers,
                              json=payload, verify=False)
        return r.json()

    def lnmo_status(
        self,
        business_shortcode: str = None,
        checkout_request_id: str = None,
        passcode: str = None,
    ):
        """This method uses Mpesa's Express API to check the status of a Lipa Na M-Pesa Online Payment..


        :param business_shortcode: This is organizations shortcode (Paybill or Buygoods - A 5 to 6 digit account number) used to identify an organization and receive the transaction.
        :param checkout_request_id: This is a global unique identifier of the processed checkout transaction request.
        :param passcode: Get from developer portal
        :type business_shortcode: str
        :type checkout_request_id: str
        :type passcode: str


        :return: Dict object of

            - `CustomerMessage` (str):

            - `CheckoutRequestID` (str):

            - `ResponseDescription` (str):

            - `MerchantRequestID` (str):

            - `ResponseCode` (str):
        :rtype: dict
        """

        time = (
            str(datetime.datetime.now())
            .split(".")[0]
            .replace("-", "")
            .replace(" ", "")
            .replace(":", "")
        )
        password = "{0}{1}{2}".format(
            str(business_shortcode), str(passcode), time)
        encoded = base64.b64encode(bytes(password, encoding="utf8"))
        payload = {
            "BusinessShortCode": business_shortcode,
            "Password": encoded.decode("utf-8"),
            "Timestamp": time,
            "CheckoutRequestID": checkout_request_id,
        }
        headers = {
            "Authorization": "Bearer {0}".format(self.authentication_token),
            "Content-Type": "application/json",
        }
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(
            base_safaricom_url, "/mpesa/stkpushquery/v1/query")
        try:
            r = requests.post(saf_url, headers=headers, json=payload)
        except Exception:
            r = requests.post(saf_url, headers=headers,
                              json=payload, verify=False)
        return r.json()

    def reverse(
        self,
        initiator: str = None,
        security_credential: str = None,
        command_id="TransactionReversal",
        transaction_id: str = None,
        amount: str = None,
        receiver_party: str = None,
        receiver_identifier_type: str = None,
        queue_timeout_url: str = None,
        result_url: str = None,
        remarks: str = None,
        occassion: str = None,
    ):
        """This method uses Mpesa's Transaction Reversal API to reverse a M-Pesa transaction.

        :param initiator: Username used to authenticate the transaction.
        :param security_credential: Generate from developer portal
        :param command_id: TransactionReversal
        :param transaction_id: Unique identifier to identify a transaction on M-Pesa.
        :param amount: The amount being transacted
        :param receiver_party: Organization/MSISDN making the transaction

            - Shortcode (6 digits)

            - MSISDN (12 digits).

        :param receiver_identifier_type: MSISDN receiving the transaction (12 digits).
        :param queue_timeout_url: The url that handles information of timed out transactions.
        :param result_url: The url that receives results from M-Pesa api call.
        :param remarks: Comments that are sent along with the transaction(maximum 100 characters)
        :param occassion: Occassion
        :type initiator: str
        :type security_credential: str
        :type command_id: str
        :type transaction_id: str
        :type amount: str
        :type receiver_party: str
        :type receiver_identifier_type: str
        :type queue_timeout_url: str
        :type result_url: str
        :type remarks: str
        :type occassion: str

        :return: Dict object of

            - `OriginatorConverstionID` (str): The unique request ID for tracking a transaction.

            - `ConversationID` (str): The unique request ID returned by mpesa for each request made

            - `ResponseDescription` (str): Response Description message
        :rtype: dict
        :Example:

        .. code-block:: json

            {
               "Result":
               {
                "ResultType":0,
                "ResultCode":0,
                "ResultDesc":"The service request has been accepted successfully.",
                "OriginatorConversationID":"10819-695089-1",
                "ConversationID":"AG_20170727_00004efadacd98a01d15",
                "TransactionID":"LGR019G3J2",
                "ReferenceData":
                {
                 "ReferenceItem":
                 {
                   "Key":"QueueTimeoutURL",
                   "Value":"https://internalsandbox.safaricom.co.ke/mpesa/reversalresults/v1/submit"
                 }
                }
               }
             }

        """

        payload = {
            "Initiator": initiator,
            "SecurityCredential": security_credential,
            "CommandID": command_id,
            "TransactionID": transaction_id,
            "Amount": amount,
            "ReceiverParty": receiver_party,
            "ReceiverIdentifierType": receiver_identifier_type,
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url,
            "Remarks": remarks,
            "Occassion": occassion,
        }
        headers = {
            "Authorization": "Bearer {0}".format(self.authentication_token),
            "Content-Type": "application/json",
        }
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(
            base_safaricom_url, "/mpesa/reversal/v1/request")
        try:
            r = requests.post(saf_url, headers=headers, json=payload)
        except Exception:
            r = requests.post(saf_url, headers=headers,
                              json=payload, verify=False)
        return r.json()

    def transaction_status(
        self,
        party_a: str = None,
        identifier_type: str = None,
        remarks: str = None,
        initiator: str = None,
        passcode: str = None,
        result_url: str = None,
        queue_timeout_url: str = None,
        transaction_id: str = None,
        occassion: str = None,
        shortcode: str = None,
    ):
        """This method uses Mpesa's Transaction Status API to check the status of a transaction.


        :param party_a: Organization/MSISDN receiving the transaction

            - MSISDN or

            - shortcode.

        :param identifier_type: Type of organization receiving the transaction

            .. csv-table:: identifier types
                :header: "identifier_type","description"
                :widths: 15,30

                1,"MSISDN"
                2,"Till Number"
                3,"Shortcode"

        :param remarks: Comments that are sent along with the transaction(maximum 100 characters).
        :param initiator: This is the credential/username used to authenticate the transaction request.
        :param passcode: Get from developer portal
        :param result_url: The url that handles information from the mpesa API call.
        :param transaction_id: Unique identifier to identify a transaction on M-Pesa.
        :param queue_timeout_url: The url that stores information of timed out transactions.
        :param shortcode: The short code of the organization.
        :param occassion: Occasion
        :type party_a: str
        :type identifier_type: str
        :type remarks: str
        :type initiator: str
        :type passcode: str
        :type transaction_id: str
        :type queue_timeout_url: str
        :type result_url: str
        :type shortcode: str
        :type occassion: str

        :return: Dict object of

            - `ResultDesc`: ,

            - `CheckoutRequestID`: ,

            - `ResponseDescription`: ,

            - `MerchantRequestID`: ,

            - `ResponseCode`: ,

            - `ResultCode`:
        :rtype: dict
        """

        time = (
            str(datetime.datetime.now())
            .split(".")[0]
            .replace("-", "")
            .replace(" ", "")
            .replace(":", "")
        )
        password = "{0}{1}{2}".format(str(shortcode), str(passcode), time)
        encoded = base64.b64encode(bytes(password, encoding="utf-8"))
        payload = {
            "CommandID": "TransactionStatusQuery",
            "PartyA": party_a,
            "IdentifierType": identifier_type,
            "Remarks": remarks,
            "Initiator": initiator,
            "SecurityCredential": encoded.decode("utf-8"),
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url,
            "TransactionID": transaction_id,
            "Occasion": occassion,
        }
        headers = {
            "Authorization": "Bearer {0}".format(self.authentication_token),
            "Content-Type": "application/json",
        }
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(
            base_safaricom_url, "/mpesa/stkpushquery/v1/query")
        try:
            r = requests.post(saf_url, headers=headers, json=payload)
        except Exception:
            r = requests.post(saf_url, headers=headers,
                              json=payload, verify=False)
        return r.json()

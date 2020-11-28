"""
Description: Kenya MPESA Implementation.

Author: Tralah M Brian
Email: musyoki.brian@tralahtek.com
Github: https://github.com/TralahM
"""

import datetime
import base64
import requests
from requests.auth import HTTPBasicAuth

__all__ = [
    "API",
]


class API:
    """Daraja MPESA API.

    Attributes
    -----------
    - *authentication_token* : Property method for returning oauth_token.

    Methods.
    ----------
    - `authenticate()`: Performs Authentication.
    - `b2b()`: Business to Business Transactions.
    - `b2c()`: Business to Customer Transactions.
    - `balance()`: Get Balance of Account.
    - `c2b_register_url()`: Register Url to Receive C2B Transaction Responses.
    - `c2b_simulate()`: Simulate C2B Transactions.
    - `lnmo_status()`: Get status of MPESA Express(LNMO) Transactions.
    - `lnmo_stkpush()`: Initiate MPESA Express(LNMO) Checkouts.
    - `reverse()`: Reverse MPESA Transactions.
    - `transaction_status`: Get status of MPESA Transactions.

    """

    def __init__(
        self,
        env="sandbox",
        app_key=None,
        app_secret=None,
        sandbox_url="https://sandbox.safaricom.co.ke",
        live_url="https://api.safaricom.co.ke",
    ):
        """Initialize API.

        Parameters.
        -------------
        :param `env`:  The target environment. *sandbox* or *production*.
        :param `app_key`: The *app_key* from developers portal.
        :param `app_secret`: The *app_secret* from developers portal.
        :param `sandbox_url`: The *sandbox_url* default <https://sandbox.safaricom.co.ke>.
        :param `live_url`: The *live_url* default <https://api.safaricom.co.ke>.
        """
        self.env = env
        self.app_key = app_key
        self.app_secret = app_secret
        self.sandbox_url = sandbox_url
        self.live_url = live_url

    @property
    def authentication_token(self):
        """Return Authentication Token."""
        return self.authenticate()

    def authenticate(self):
        """To make Mpesa API calls, you will need to authenticate your app.

        This method is used to fetch the access token required by Mpesa.
        Mpesa supports client_credentials grant type.
        To authorize your API calls to Mpesa, you will need a Basic Auth over HTTPS authorization token.
        The Basic Auth string is a base64 encoded string
        of your app's client key and client secret.

        Returns.
        --------------

        - `access_token` (str): This token is to be used with the Bearer header for further API calls to Mpesa.

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
        initiator=None,
        security_credential=None,
        command_id=None,
        sender_identifier_type=None,
        receiver_identifier_type=None,
        amount=None,
        party_a=None,
        party_b=None,
        remarks=None,
        account_reference=None,
        queue_timeout_url=None,
        result_url=None,
    ):
        """This method uses Mpesa's B2B API to transact from one company to another.

        Arguments.
        -----------

        - `initiator` (str): Username used to authenticate the transaction.

        - `security_credential` (str): Generate from developer portal

        - `command_id` (str): Options: BusinessPayBill, BusinessBuyGoods, DisburseFundsToBusiness, BusinessToBusinessTransfer ,BusinessTransferFromMMFToUtility, BusinessTransferFromUtilityToMMF, MerchantToMerchantTransfer, MerchantTransferFromMerchantToWorking, MerchantServicesMMFAccountTransfer, AgencyFloatAdvance

        - `sender_identifier_type` (str): 2 for Till Number, 4 for organization shortcode

        - `receiver_identifier_type` (str): # 2 for Till Number, 4 for organization shortcode

        - `amount` (str): Amount.

        - `party_a` (int): Sender shortcode.

        - `party_b` (int): Receiver shortcode.

        - `remarks` (str): Comments that are sent along with the transaction(maximum 100 characters).

        - `account_reference` (str): Use if doing paybill to banks etc.

        - `queue_timeout_url` (str): The url that handles information of timed out transactions.

        - `result_url` (str): The url that receives results from M-Pesa api call.



        Returns.
        ---------

        - `OriginatorConverstionID` (str): The unique request ID for tracking a transaction.

        - `ConversationID` (str): The unique request ID returned by mpesa for each request made

        - `ResponseDescription` (str): Response Description message



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
        initiator_name=None,
        security_credential=None,
        command_id=None,
        amount=None,
        party_a=None,
        party_b=None,
        remarks=None,
        queue_timeout_url=None,
        result_url=None,
        occassion=None,
    ):
        """This method uses Mpesa's B2C API to transact between an M-Pesa short code to a phone number registered on M-Pesa..

        Args.
        --------------

        - `initiator_name` (str): Username used to authenticate the transaction.

        - `security_credential` (str): Generate from developer portal

        - `command_id` (str): Options: SalaryPayment, BusinessPayment, PromotionPayment

        - `amount`(str): Amount.

        - `party_a` (int): Organization/MSISDN making the transaction - Shortcode (6 digits) - MSISDN (12 digits).

        - `party_b` (int): MSISDN receiving the transaction (12 digits).

        - `remarks` (str): Comments that are sent along with the transaction(maximum 100 characters).

        - `account_reference` (str): Use if doing paybill to banks etc.

        - `queue_timeout_url` (str): The url that handles information of timed out transactions.

        - `result_url` (str): The url that receives results from M-Pesa api call.

        - `ocassion` (str):



        Returns.
        --------------

        - `OriginatorConverstionID` (str): The unique request ID for tracking a transaction.

        - `ConversationID` (str): The unique request ID returned by mpesa for each request made

        - `ResponseDescription` (str): Response Description message

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
        initiator=None,
        security_credential=None,
        command_id=None,
        party_a=None,
        identifier_type=None,
        remarks=None,
        queue_timeout_url=None,
        result_url=None,
    ):
        """This method uses Mpesa's Account Balance API to to enquire the balance on an M-Pesa BuyGoods (Till Number).

        Args.
        --------------

        - `initiator` (str): Username used to authenticate the transaction.

        - `security_credential` (str): Generate from developer portal.

        - `command_id` (str): AccountBalance.

        - `party_a` (int): Till number being queried.

        - `identifier_type` (int): Type of organization receiving the transaction. Options: 1 - MSISDN 2 - Till Number  4 - Organization short code

        - `remarks` (str): Comments that are sent along with the transaction(maximum 100 characters).

        - `queue_timeout_url` (str): The url that handles information of timed out transactions.

        - `result_url` (str): The url that receives results from M-Pesa api call.



        Returns.
        --------------

        - `OriginatorConverstionID` (str): The unique request ID for tracking a transaction.

        - `ConversationID` (str): The unique request ID returned by mpesa for each request made

        - `ResponseDescription` (str): Response Description message


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
        shortcode=None,
        response_type=None,
        confirmation_url=None,
        validation_url=None,
    ):
        """This method uses Mpesa's C2B API to register validation and confirmation URLs on M-Pesa.

        Args.
        --------------

        - `shortcode` (int): The short code of the organization.

        - `response_type` (str): Default response type for timeout. Incase a tranaction times out, Mpesa will by default Complete or Cancel the transaction.

        - `confirmation_url` (str): Confirmation URL for the client.

        - `validation_url` (str): Validation URL for the client.



        Returns.
        --------------

        - `OriginatorConversationID` (str): The unique request ID for tracking a transaction.

        - `ConversationID` (str): The unique request ID returned by mpesa for each request made

        - `ResponseDescription` (str): Response Description message


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
        shortcode=None,
        command_id=None,
        amount=None,
        msisdn=None,
        bill_ref_number=None,
    ):
        """This method uses Mpesa's C2B API to simulate a C2B transaction.

        Args.
        --------------

        - `shortcode` (int): The short code of the organization.

        - `command_id` (str): Unique command for each transaction type. - CustomerPayBillOnline - CustomerBuyGoodsOnline.

        - `amount` (int): The amount being transacted

        - `msisdn` (int): Phone number (msisdn) initiating the transaction MSISDN(12 digits)

        - `bill_ref_number`: Optional



        Returns.
        --------------

        - `OriginatorConverstionID` (str): The unique request ID for tracking a transaction.

        - `ConversationID` (str): The unique request ID returned by mpesa for each request made

        - `ResponseDescription` (str): Response Description message

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
        business_shortcode=None,
        passcode=None,
        amount=None,
        callback_url=None,
        reference_code=None,
        phone_number=None,
        description=None,
    ):
        """This method uses Mpesa's Express API to initiate online payment on behalf of a customer..

        Args.
        --------------

        - `business_shortcode` (int): The short code of the organization.

        - `passcode` (str): Get from developer portal

        - `amount` (int): The amount being transacted

        - `callback_url` (str): A CallBack URL is a valid secure URL that is used to receive notifications from M-Pesa API.

        - `reference_code`: Account Reference: This is an Alpha-Numeric parameter that is defined by your system as an Identifier of the transaction for CustomerPayBillOnline transaction type.

        - `phone_number`: The Mobile Number to receive the STK Pin Prompt.

        - `description`: This is any additional information/comment that can be sent along with the request from your system. MAX 13 characters



        Returns.
        --------------

        - `CustomerMessage` (str):

        - `CheckoutRequestID` (str):

        - `ResponseDescription` (str):

        - `MerchantRequestID` (str):

        - `ResponseCode` (str):

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
        self, business_shortcode=None, checkout_request_id=None, passcode=None
    ):
        """This method uses Mpesa's Express API to check the status of a Lipa Na M-Pesa Online Payment..

        Args.
        --------------

        - `business_shortcode` (int): This is organizations shortcode (Paybill or Buygoods - A 5 to 6 digit account number) used to identify an organization and receive the transaction.

        - `checkout_request_id` (str): This is a global unique identifier of the processed checkout transaction request.

        - `passcode` (str): Get from developer portal


        Returns.
        --------------

        - `CustomerMessage` (str):

        - `CheckoutRequestID` (str):

        - `ResponseDescription` (str):

        - `MerchantRequestID` (str):

        - `ResponseCode` (str):


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
        initiator=None,
        security_credential=None,
        command_id="TransactionReversal",
        transaction_id=None,
        amount=None,
        receiver_party=None,
        receiver_identifier_type=None,
        queue_timeout_url=None,
        result_url=None,
        remarks=None,
        occassion=None,
    ):
        """This method uses Mpesa's Transaction Reversal API to reverse a M-Pesa transaction.

        Args.
        --------------

        - `initiator` (str): Username used to authenticate the transaction.

        - `security_credential` (str): Generate from developer portal

        - `command_id` (str): TransactionReversal

        - `transaction_id` (str): Unique identifier to identify a transaction on M-Pesa.

        - `amount` (int): The amount being transacted

        - `receiver_party` (int): Organization/MSISDN making the transaction - Shortcode (6 digits) - MSISDN (12 digits).

        - `receiver_identifier_type` (int): MSISDN receiving the transaction (12 digits).

        - `queue_timeout_url` (str): The url that handles information of timed out transactions.

        - `result_url` (str): The url that receives results from M-Pesa api call.

        - `remarks` (str): Comments that are sent along with the transaction(maximum 100 characters)

        - `occassion` (str):



        Returns.
        --------------

        - `OriginatorConverstionID` (str): The unique request ID for tracking a transaction.

        - `ConversationID` (str): The unique request ID returned by mpesa for each request made

        - `ResponseDescription` (str): Response Description message

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
        party_a=None,
        identifier_type=None,
        remarks=None,
        initiator=None,
        passcode=None,
        result_url=None,
        queue_timeout_url=None,
        transaction_id=None,
        occassion=None,
        shortcode=None,
    ):
        """This method uses Mpesa's Transaction Status API to check the status of a transaction.

        Args.
        --------------

        - `party_a` (str): Organization/MSISDN receiving the transaction - MSISDN or shortcode.

        - `identifier_type` (str): Type of organization receiving the transaction 1-MSISDN. 2-Till Number, 3-Shortcode.

        - `remarks` (str): Comments that are sent along with the transaction(maximum 100 characters).

        - `initiator` (str): This is the credential/username used to authenticate the transaction request.

        - `passcode` (str): Get from developer portal

        - `result_url` (str): The url that handles information from the mpesa API call.

        - `transaction_id` (str): Unique identifier to identify a transaction on M-Pesa.

        - `queue_timeout_url` (str): The url that stores information of timed out transactions.

        - `result_url` (str): The url that receives results from M-Pesa api call.

        - `shortcode` (int): The short code of the organization.

        - `occassion` (str):



        Returns.
        --------------

        - `ResultDesc`: ,

        - `CheckoutRequestID`: ,

        - `ResponseDescription`: ,

        - `MerchantRequestID`: ,

        - `ResponseCode`: ,

        - `ResultCode`:



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

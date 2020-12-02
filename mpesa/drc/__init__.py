"""Democratic Republic of Congo MPESA SDK Implementation.

.. note::
    This API needs to be called from a Server/Computer whose Public IP Address
    has been WhiteListed by the Vodacom MPESA Team from the DRC.

.. warning::
    Only WhiteListed IPs are able to access the Remote MPESA APIs.

.. note::
    So Ensure your server IP is White Listed before Using this API.
"""
import requests
import typing
from mpesa.drc.generators import (
    generate_login,
    generate_c2b,
    generate_b2c,
)
from mpesa.drc.parsers import (
    parse_c2b_response,
    parse_login_response,
    parse_b2c_response,
)


class API:
    """DRC API.

    :param Username: Username provided by Mpesa Team.
    :param Password: Password provided by Mpesa Team.
    :param env: Environment either ``"sandbox"`` or ``"production"``, defaults ``"sandbox"``.
    :type env: str, optional.

    **Attributes.**

    .. attribute:: sandbox_host

        The sandbox host ``"https://uatipg.m-pesa.vodacom.cd"``.

    .. attribute:: live_host

        The live host ``"https://ipg.m-pesa.vodacom.cd"``.

    .. attribute:: login_path

        The login path ``":8091/insight/SOAPIn"``

    .. attribute:: c2b_path

        The c2b path ``":8091/insight/SOAPIn"``

    .. attribute:: b2c_path

        The b2c path ``":8094/iPG/B2C"``

    """

    def __init__(
        self,
        Username,
        Password,
        env: str = "sandbox",
    ):
        """Construct API object."""
        self.env = env
        self.Username = Username
        self.Password = Password
        self.sandbox_host = "https://uatipg.m-pesa.vodacom.cd"
        self.live_host = "https://ipg.m-pesa.vodacom.cd"
        self.login_path = ":8091/insight/SOAPIn"
        self.c2b_path = ":8091/insight/SOAPIn"
        self.b2c_path = ":8094/iPG/B2C"

    @property
    def _login_url(self):
        """Return Login URL."""
        if self.env == "production":
            return self.live_host + self.login_path
        else:
            return self.sandbox_host + self.login_path

    @property
    def _c2b_url(self):
        """Return Login URL."""
        if self.env == "production":
            return self.live_host + self.c2b_path
        else:
            return self.sandbox_host + self.c2b_path

    @property
    def _b2c_url(self):
        """Return Login URL."""
        if self.env == "production":
            return self.live_host + self.b2c_path
        else:
            return self.sandbox_host + self.b2c_path

    def _post_request(self, url: str, content: str, content_handler: typing.Callable):
        """Execute POST Request to IPG URL with XML content data."""
        response = requests.post(url, data=content)
        result_content = response.content
        return content_handler(result_content)

    def authentication_token(self):
        """Return Authentication Token."""
        content = generate_login(
            {
                "Username": self.Username,
                "Password": self.Password,
            },
        )
        result = self._post_request(
            self._login_url,
            content,
            parse_login_response,
        )
        return result["token"]
        ...

    def b2c(
        self,
        Amount: str,
        CallBackChannel: str,
        CallBackDestination: str,
        CommandID: str,
        Currency: str,
        CustomerMSISDN,
        Language: str,
        ServiceProviderName: str,
        Shortcode: str,
        ThirdPartyReference: str,
        TransactionDateTime: str,
    ):
        """B2C.

        :param ThirdPartyReference: ThirdPartyReference.
        :type ThirdPartyReference: str.
        :param TransactionDateTime: TransactionDateTime.
        :type TransactionDateTime: str.
        :param Token: Token.
        :type Token: str.
        :param Shortcode: Shortcode.
        :type Shortcode: str.
        :param CustomerMSISDN: CustomerMSISDN.
        :type CustomerMSISDN: str.
        :param ServiceProviderName: ServiceProviderName.
        :type ServiceProviderName: str.
        :param Language: Language.
        :type Language: str.
        :param CallBackChannel: CallBackChannel.
        :type CallBackChannel: str.
        :param CallBackDestination: CallBackDestination.
        :type CallBackDestination: str.
        :param Currency: Currency.
        :type Currency: str.
        :param CommandID: CommandID.
        :type CommandID: str.
        :param Amount: Amount.
        :type Amount: str.
        """
        url = self._b2c_url
        params = {
            "Token": self.authentication_token,
            "ThirdPartyReference": ThirdPartyReference,
            "TransactionDateTime": TransactionDateTime,
            "Shortcode": Shortcode,
            "CustomerMSISDN": CustomerMSISDN,
            "ServiceProviderName": ServiceProviderName,
            "Language": Language,
            "CallBackChannel": CallBackChannel,
            "CallBackDestination": CallBackDestination,
            "Currency": Currency,
            "CommandID": CommandID,
            "Amount": Amount,
        }
        content = generate_b2c(params)
        handler = parse_b2c_response
        return self._post_request(url, content, handler)
        ...

    def c2b(
        self,
        Amount: str,
        CallBackChannel: str,
        CallBackDestination: str,
        CommandId: str,
        Currency: str,
        CustomerMSISDN: str,
        Date: str,
        Initials: str,
        Language: str,
        ServiceProviderCode: str,
        Surname: str,
        ThirdPartyReference: str,
    ):
        """C2B.

        :param ThirdPartyReference: ThirdPartyReference.
        :type ThirdPartyReference: str.
        :param Token: Token.
        :type Token: str.
        :param Initials: Initials.
        :type Initials: str.
        :param Date: Date.
        :type Date: str.
        :param CustomerMSISDN: CustomerMSISDN.
        :type CustomerMSISDN: str.
        :param CommandId: CommandId.
        :type CommandId: str.
        :param Language: Language.
        :type Language: str.
        :param CallBackDestination: CallBackDestination.
        :type CallBackDestination: str.
        :param CallBackChannel: CallBackChannel.
        :type CallBackChannel: str.
        :param Currency: Currency.
        :type Currency: str.
        :param Surname: Surname.
        :type Surname: str.
        :param Amount: Amount.
        :type Amount: str.
        :param ServiceProviderCode: ServiceProviderCode.
        :type ServiceProviderCode: str.
        """
        url = self._c2b_url
        params = {
            "Token": self.authentication_token,
            "ThirdPartyReference": ThirdPartyReference,
            "Initials": Initials,
            "Date": Date,
            "CustomerMSISDN": CustomerMSISDN,
            "CommandId": CommandId,
            "Language": Language,
            "CallBackDestination": CallBackDestination,
            "CallBackChannel": CallBackChannel,
            "Currency": Currency,
            "Surname": Surname,
            "Amount": Amount,
            "ServiceProviderCode": ServiceProviderCode,
        }
        content = generate_c2b(params)
        handler = parse_c2b_response
        return self._post_request(url, content, handler)

    def w2b(
        self,
        Amount: str,
        BankShortCode: str,
        Currency: str,
        CustomerAccountNumber: str,
        CustomerMSISDN: str,
        ThirdPartyID: str,
        TransactionDateTime: str,
        TransactionID: str,
        TransactionType: str,
    ):
        """Wallet To Bank.

        .. todo::
            To be Implemented In the Future once the API is documented.
        """
        params = {
            "TransactionDateTime": TransactionDateTime,
            "CustomerAccountNumber": CustomerAccountNumber,
            "ThirdPartyID": ThirdPartyID,
            "TransactionType": TransactionType,
            "CustomerMSISDN": CustomerMSISDN,
            "BankShortCode": BankShortCode,
            "Currency": Currency,
            "TransactionID": TransactionID,
            "Amount": Amount,
        }
        print(params)
        pass
        ...

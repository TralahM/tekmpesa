from mpesa.ghana import API
import yaml
import os

secret_file = os.path.expanduser("~/.openapi_mpesaportal.secrets.yml")
with open(secret_file, "r") as rf:
    secrets = yaml.load(rf, Loader=yaml.Loader)

public_key = secrets.get("sandbox_public_key")
api_key = secrets.get("sandbox_api_key")
env = "sandbox"

api = API(public_key=public_key, api_key=api_key, env=env)
print()
print(f"api.session_id = {api.session_id}")


c2b = {
    "Amount": "10",
    "Country": "GHA",
    "Currency": "GHS",
    "CustomerMSISDN": "000000000001",
    "ServiceProviderCode": "000000",
    "ThirdPartyConversationID": "asv02e5958774f7ba228d83d0d689761",
    "TransactionReference": "T1234C",
    "PurchasedItemsDesc": "Shoes",
}

print(api.c2b(**c2b))

b2c = {
    "Amount": "10",
    "Country": "GHA",
    "Currency": "GHS",
    "CustomerMSISDN": "000000000001",
    "ServiceProviderCode": "000000",
    "ThirdPartyConversationID": "asv02e5958774f7ba228d83d0d689761",
    "TransactionReference": "T12344C",
    "PaymentItemsDesc": "Salary payment",
}
print(api.b2c(**b2c))

b2b = {
    "Amount": "10",
    "Country": "GHA",
    "Currency": "GHS",
    "PrimaryPartyCode": "000000",
    "ReceiverPartyCode": "000001",
    "ThirdPartyConversationID": "asv02e5958774f7ba228d83d0d689761",
    "TransactionReference": "T12344C",
    "PurchasedItemsDesc": "Shoes",
}
print(api.b2b(**b2b))

rv = {
    "Country": "GHA",
    "ReversalAmount": "25",
    "ServiceProviderCode": "000000",
    "ThirdPartyConversationID": "asv02e5958774f7ba228d83d0d689761",
    "TransactionID": "0000000000001",
}
print(api.reversal(**rv))

ts = {
    "QueryReference": "000000000000000000001",
    "ServiceProviderCode": "000000",
    "ThirdPartyConversationID": "asv02e5958774f7ba228d83d0d689761",
    "Country": "GHA",
}
print(api.transaction_status(**ts))


ddc = {
    "AgreedTC": "1",
    "Country": "GHA",
    "CustomerMSISDN": "000000000001",
    "EndRangeOfDays": "22",
    "ExpiryDate": "20161126",
    "FirstPaymentDate": "20160324",
    "Frequency": "06",
    "ServiceProviderCode": "000000",
    "StartRangeOfDays": "01",
    "ThirdPartyConversationID": "AAA6d1f9391a0052de0b5334a912jbsj1j2kk",
    "ThirdPartyReference": "3333",
}
print(api.direct_debit_create(**ddc))


ddp = {
    "Amount": "10",
    "Country": "GHA",
    "Currency": "GHS",
    "CustomerMSISDN": "000000000001",
    "ServiceProviderCode": "000000",
    "ThirdPartyConversationID": "AAA6d1f939c1005v2de053v4912jbasdj1j2kk",
    "ThirdPartyReference": "5db410b459bd433ca8e5",
}
print(api.direct_debit_payment(**ddp))

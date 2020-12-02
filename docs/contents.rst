Getting Started.
=================
The package provides a simple,clean and intuitive interface to enable you to
quickly and consistently use this library in your python application.

Installation
``````````````````
The preferred installation method is directly from pypi:

.. code-block:: shell

   pip install -U tekmpesa

Additionally, if you want to use the built-in test mechanisms, you need to
install some extra requirements:

.. code-block:: shell

   pip install -U tekmpesa[tests]


Usage
``````````````````
The main class you will be working with is the ``API`` class of the respective
submodules.

For example for Mpesa Kenya the class is :class:`mpesa.kenya.API`, and similarly:
:class:`mpesa.ghana.API` for Ghana,
:class:`mpesa.tanzania.API` for Tanzania,
:class:`mpesa.mozambique.API` for Mozambique,
:class:`mpesa.drc.API` for the Democratic Republic of Congo.



.. code-block:: python

    import mpesa

    # There is a corresponding module for each supported country.
    # i.e
    mpesa_ke=mpesa.kenya.API(app_key="<APP_KEY>",app_secret="<APP_SECRET>",env="sandbox")
    # for production,i.e going LIVE use env="production".

    mpesa_gh=mpesa.ghana.API(public_key="<PUBLIC_KEY>",api_key="<API_KEY>",env="sandbox")
    # for production,i.e going LIVE use env="production".

    mpesa_tz=mpesa.tanzania.API(public_key="<PUBLIC_KEY>",api_key="<API_KEY>",env="sandbox")
    # for production,i.e going LIVE use env="production".

    mpesa_mz=mpesa.mozambique.API(public_key="<PUBLIC_KEY>",api_key="<API_KEY>",env="sandbox")
    # for production,i.e going LIVE use env="production".

    mpesa_drc=mpesa.drc.API(Username="<Username>",Password="<Password>",env="sandbox")
    # for production,i.e going LIVE use env="production".


Configuration
``````````````````````````

Examples
````````````````````````````````````````

.. code-block:: python

   # Kenya STK Push.
   stkpush_result=mpesa_ke.lnmo_stkpush(
       business_shortcode="",
       passcode="",
       phonenumber="",
       amount="",
       callback_url="",
       reference_code="",
       description="",
   )
   # Kenya B2C
   ke_b2c_result=mpesa_ke.b2c(
        initiator_name="",
        security_credential="",
        command_id="",
        amount="",
        party_a="",
        party_b="",
        remarks="",
        queue_timeout_url="",
        result_url="",
        occassion="",
   )
   # Kenya B2B
   ke_b2b_result=mpesa_ke.b2b(
        initiator="",
        security_credential="",
        command_id="",
        sender_identifier_type="",
        receiver_identifier_type="",
        amount="",
        party_a="",
        party_b="",
        remarks="",
        account_reference="",
        queue_timeout_url="",
        result_url="",
   )

   # For Ghana, and  Tanzania The API signature is the same for all methods.
   gh_c2b_result=mpesa_gh.c2b(
        Amount="",
        CustomerMSISDN="",
        ServiceProviderCode="",
        ThirdPartyConversationID="",
        TransactionReference="",
        PurchasedItemsDesc="",
   )

   # Ghana/Tanzania b2c
   tz_b2c_result=mpesa_tz.b2c(
        Amount="",
        CustomerMSISDN="",
        ServiceProviderCode="",
        ThirdPartyConversationID="",
        TransactionReference="",
        PaymentItemsDesc="",
   )
   # Ghana/Tanzania b2b
   tz_b2b_result=mpesa_tz.b2b(
        Amount="",
        PrimaryPartyCode="",
        ReceiverPartyCode="",
        ThirdPartyConversationID="",
        TransactionReference="",
        PurchasedItemsDesc="",
   )

   # Mozambique c2b.
   mz_c2b_result=mpesa_mz.c2b(
        Amount="",
        CustomerMSISDN="",
        ServiceProviderCode="",
        ThirdPartyReference="",
        TransactionReference="",
   )
   # Mozambique b2c.
   mz_b2c_result=mpesa_mz.b2c(
        Amount="",
        CustomerMSISDN="",
        ServiceProviderCode="",
        ThirdPartyReference="",
        TransactionReference="",
   )
   # Mozambique b2b.
   mz_b2b_result=mpesa_mz.b2b(
        Amount="",
        PrimaryPartyCode="",
        ReceiverPartyCode="",
        ThirdPartyReference="",
        TransactionReference="",
   )

   # DRC c2b
   drc_c2b_result=mpesa_drc.c2b(
        Amount="",
        CallBackChannel="",
        CallBackDestination="",
        CommandId="",
        Currency="",
        CustomerMSISDN="",
        Date="",
        Initials="",
        Language="",
        ServiceProviderCode="",
        Surname="",
        ThirdPartyReference="",

   )
   # DRC b2c
   drc_b2c_result=mpesa_drc.b2c(
        Amount="",
        CallBackChannel="",
        CallBackDestination="",
        CommandID="",
        Currency="",
        CustomerMSISDN,
        Language="",
        ServiceProviderName="",
        Shortcode="",
        ThirdPartyReference="",
        TransactionDateTime="",
   )



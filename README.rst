python-hipay
============

python-hipay is a tiny package that implements MAPI for hipay secure online
payment (https://www.hipay.com/). The implementation is based on the doc
(https://www.hipay.com/dl/kit_marchand_en.pdf). They also provide a php kit
available at https://www.hipay.com/dl/hipay_mapi_php5_1_0.tgz.

This module is experimental and currently actively developed.

Usage
-----

You will indeed need at least a Merchant test account and a customer test
account to use this package, I haven't figured out a way to put virtual money in
my client test account, all the testing credit cards seems to already bound to
some existing accounts and Hipay don't seem to allow sharing these cards among
test accounts. You'll also need your test client account tight to your mobile
since Hipay will send you a five digits verification number for every payment
you do with your client test account.


SimplePayment
-------------

Code Sample::

        s = hipay.PaymentParams("YOUR_ITEM_ACCOUNT", "YOUR_TAX_ACCOUNT", "YOUR_INSURANCE_ACCOUNT", 
                                "YOUR_FIXED_COST_ACCOUNT", "YOUR_SHIPPING_ACCOUNT")
        s.setBackgroundColor('#234567')
        s.setCaptureDay('6')
        s.setCurrency('EUR')
        s.setLocale('fr_FR')
        s.setEmailAck('test@example.org')
        s.setLogin('YOUR_LOGIN', 'YOUR_PASSWORD')
        s.setMedia('WEB')
        s.setRating('+18')
        s.setIdForMerchant('YOUR_MERCHANT_ID')
        s.setMerchantSiteId('YOUR_MERCHANT_SITE_ID')
        s.setMerchantDatas({'alpha':23, 'beta':34})
        s.setURLOk("http://example.org/hipay/result/ok")
        s.setURLNok("http://example.org/hipay/result/ko")
        s.setURLCancel("http://example.org/hipay/result/cancel")
        s.setURLAck("http://example.org/hipay/result/ack")
        s.setLogoURL("http://example.org/hipay/shop/logo")        
        pr = hipay.Product()
        mta = hipay.Tax('tax')
        mestax=[dict(taxName='TVA 19.6', taxVal='19.6', percentage='true'), 
                dict(taxName='TVA 5.5', taxVal='5.5', percentage='true')]
        mta.setTaxes(mestax)
        
        products = [{'name':'The Fall of  Hyperion','info':u'Simmons, Dan – ISBN 0575076380', 
                     'quantity':'10', 'ref':'10', 'category':'91', 'price':'120', 'tax':mta},
                    {'name':'The Fall of  Hyperion','info':u'Simmons, Dan – ISBN 0575076380', 
                     'quantity':'10', 'ref':'10', 'category':'91', 'price':'120', 'tax':mta}]
        pr.setProducts(products)
        
        order = hipay.Order()
        af = hipay.Affiliate()

        # If you have affiliates
        affiliates = [dict(customerId='123', accountId='764527',percentageTarget='12', val='120')]
        af.setValue(affiliates)        
        taxes = dict()
        for root in 'shippingTax', 'insuranceTax', 'fixedCostTax':
            taxes[root] = hipay.Tax(root)
            mestax=[dict(taxName='TVA', taxVal='19.6', percentage='true')]
            taxes[root].setTaxes(mestax)
        
        data = [{'shippingAmount':1.50, 'insuranceAmount':2.00, 'fixedCostAmount':2.25, 
                'fixedCostTax':taxes['fixedCostTax'], 'insuranceTax': taxes['insuranceTax'], 
                'shippingTax':taxes['shippingTax'], 'orderTitle':'Mon ordre', 'orderInfo':'Box', 
                'orderCategory':91}]
        order.setOrders(data)
        pay = hipay.HiPay(s)        
        pay.SimplePayment(order, pr)
        # Validate against the provided schema  https://payment.hipay.com/schema/mapi.xs
        response = pay.SendPayment("https://test-payment.hipay.com/order/")



MultiplePayment
---------------

Code Sample::

        import hipay
        s = hipay.PaymentParams("YOUR_ITEM_ACCOUNT", "YOUR_TAX_ACCOUNT", "YOUR_INSURANCE_ACCOUNT", 
                                "YOUR_FIXED_COST_ACCOUNT", "YOUR_SHIPPING_ACCOUNT")
        s.setBackgroundColor('#234567')
        s.setCaptureDay('6')
        s.setCurrency('EUR')
        s.setLocale('fr_FR')
        s.setEmailAck('test@example.org')
        s.setLogin('YOUR_LOGIN', 'YOUR_PASSWORD')
        s.setMedia('WEB')
        s.setRating('+18')
        s.setIdForMerchant('YOUR_MERCHANT_ID')
        s.setMerchantSiteId('YOUR_MERCHANT_SITE_ID')
        s.setMerchantDatas({'alpha':23, 'beta':34})
        s.setURLOk("http://example.org/hipay/result/ok")
        s.setURLNok("http://example.org/hipay/result/ko")
        s.setURLCancel("http://example.org/hipay/result/cancel")
        s.setURLAck("http://example.org/hipay/result/ack")
        s.setLogoURL("http://example.org/hipay/shop/logo")        
        pr = hipay.Product()
        mta = hipay.Tax('tax')
        mestax=[dict(taxName='TVA 19.6', taxVal='19.6', percentage='true'), dict(taxName='TVA 5.5', taxVal='5.5', percentage='true')]
        mta.setTaxes(mestax)
        
        products = [{'name':'The Fall of  Hyperion','info':u'Simmons, Dan – ISBN 0575076380', 
                     'quantity':'10', 'ref':'10', 'category':'91', 'price':'120', 'tax':mta},
                    {'name':'The Fall of  Hyperion','info':u'Simmons, Dan – ISBN 0575076380', 
                     'quantity':'10', 'ref':'10', 'category':'91', 'price':'120', 'tax':mta}]
        pr.setProducts(products)
        
        order = hipay.Order()
        af = hipay.Affiliate()

        # If you have affiliates
        affiliates = [dict(customerId='123', accountId='764527',percentageTarget='12', val='120')]
        af.setValue(affiliates) 

        # Various taxes       
        taxes = dict()
        for root in 'shippingTax', 'insuranceTax', 'fixedCostTax':
            taxes[root] = hipay.Tax(root)
            mestax=[dict(taxName='TVA', taxVal='19.6', percentage='true')]
            taxes[root].setTaxes(mestax)
        
        # First and subsequent orders
        order_data = [{'shippingAmount':1.50, 'insuranceAmount':2.00, 'fixedCostAmount':2.25, 
                       'fixedCostTax':taxes['fixedCostTax'], 'insuranceTax': taxes['insuranceTax'], 
                       'shippingTax':taxes['shippingTax'], 'orderTitle':'Mon ordre 2', 'orderInfo':'Box 2', 
                       'orderCategory':91}, 
                      {'shippingAmount':1.50, 'insuranceAmount':2.00, 'fixedCostAmount':2.25, 
                       'fixedCostTax':taxes['fixedCostTax'], 'insuranceTax': taxes['insuranceTax'], 
                       'shippingTax':taxes['shippingTax'], 'orderTitle':'Mon ordre', 
                       'orderInfo':'Box', 'orderCategory':91}]
        order.setOrders(order_data)

        inst = hipay.Installement()
        mta = hipay.Tax('tax')
        mestax=[dict(taxName='TVA 19.6', taxVal='19.6', percentage='true'), dict(taxName='TVA 5.5', taxVal='5.5', percentage='true')]
        mta.setTaxes(mestax)

        # First installement and subsequent installements
        inst_data = [{'price':100, 'first':'true','paymentDelay':'1D', 'tax':mta},
                     {'price':100, 'first':'false','paymentDelay':'1M', 'tax':mta}]
        inst.setInstallements(inst_data)
        
        pay = hipay.HiPay(s)        
        pay.MultiplePayment(order, inst)

        # Validate against the provided schema https://payment.hipay.com/schema/mapi.xsd
        response = pay.SendPayment("https://test-payment.hipay.com/order/")


Django Views
------------

Code Sample::

    # urls
    url(r'^hipay/(?P<invoice_id>\d+)$', 'invoice.views.hipay_invoice', name='hipay_invoice'),
    url(r'^hipay/payment/(?P<action>cancel|ok|nook)/(?P<invoice_id>\d+)$', 'invoice.views.hipay_payment_url', name='hipay_payment_url'),
    url(r'^hipay/result/ack/(?P<invoice_id>\d+)$', 'invoice.views.hipay_ipn_ack', name='hipay_ipn_ack'),

    # views
    ... 
    base_host = "http%s://%s" %('s' if request.is_secure() else '',
                                request.get_host())
    s.setMerchantDatas({'invoice_id':invoice_id, 'customer':customer})
    s.setURLOk("%s%s" % (base_host, reverse('hipay_payment_url', kwargs={'invoice_id':invoice_id, 'action':'ok'})))
    s.setURLNok("%s%s" % (base_host, reverse('hipay_payment_url', kwargs={'invoice_id':invoice_id,'action':'nook'})))
    s.setURLCancel("%s%s" % (base_host, reverse('hipay_payment_url', kwargs={'invoice_id':invoice_id,'action':'cancel'})))
    s.setURLAck("%s%s" % (base_host, reverse('hipay_ipn_ack', kwargs={'invoice_id':invoice_id})))
    s.setLogoURL("%s%s" % (base_host, reverse('hipay_shop_logo')))
    ....

    def hipay_payment_url(request, invoice_id, action):
        """URL to redirect the client on canceled payment by the customer"""
        invoice = get_object_or_404(Invoices, pk=invoice_id)
        return render(request, 'invoice/hipay/%s_payment.html'%(action,), {'invoice':invoice})
    

    @require_http_methods(["POST"])
    @csrf_exempt
    def hipay_ipn_ack(request, invoice_id):
        """URL that get the ack from HIPAY"""
        # Use the Queryset qs that fits your needs
        invoice = get_object_or_404(qs, id_facture=invoice_id)
    
        res = hipay.ParseAck(request.POST.get('xml', None))
        if res.get('status', None) == 'ok':
            invoice.is_paye = True
            invoice.save()
        # Save the transaction for futur reference
        Transaction.objects.create(**res)

        # This is a bot that doesn't care about your response
        return HttpResponse("")

A possible transaction model::

class Transaction(models.Model):
    status = models.CharField(max_length=255)
    emailClient = models.EmailField()
    date = models.DateField()
    operation = models.CharField(max_length=255, null=True, blank=True)
    transid =  models.CharField(max_length=255, null=True, blank=True)
    merchantDatas = models.CharField(max_length=255, null=True, blank=True)
    origCurrency = models.CharField(max_length=255)
    origAmount  = models.CharField(max_length=255)
    idForMerchant = models.CharField(max_length=255)
    refProduct = models.CharField(max_length=255)
    time = models.TimeField()
    subscriptionId = models.CharField(max_length=255, null=True, blank=True)
    not_tempered_with = models.BooleanField()
    
    def __unicode__(self):
        return u"%s | %s | %s" % (
            unicode(self.status),
            unicode(self.transid),
            unicode(self.refProduct))



ACK returned
------------
In the `hipay_ipn_ack below', the dictionary returned by hipay.ParseAck have these keys::

           {'operation': ?
            'status': ?
            'date': ?
            'time': ?
            'transid': ?
            'origAmount': ?
            'origCurrency': ?
            'idForMerchant': ?
            'emailClient': ?
            'merchantDatas': ?
            'subscriptionId': ?
            'refProduct': ?
            'not_tempered_with': Boolean that compare the md5sum 
                                 sent with the computed one
             }

You may be willing to save these data in a transaction model/table and use
'merchantDatas' to identify the bills


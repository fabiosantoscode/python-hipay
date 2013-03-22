#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) 2011 Ousmane Wilane <ousmane@wilane.org>
# Copyright (C) 2011 Cyril Bouthors <cyril@bouthors.org>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
#
#$Id: tests.py 701 2011-11-24 21:32:08Z wilane $
__author__ = "Ousmane Wilane ♟ <ousmane@wilane.org>"
__date__   = "Thu Nov 17 17:44:19 2011"


import hashlib
import os
import xml.etree.ElementTree as ET
from lxml.etree import XMLSchema, XMLParser, fromstring, _Element
import hipay
from unittest import TestCase
import datetime
DIRNAME = os.path.dirname(__file__)

class HiPayTest(TestCase):
    def setUp(self):
        # We need a ticket and an account for test to pass before we use
        # selenium and friends
        # Hipay credentials
        self.login = '9f5b8ba9c9feca32055f0b5a9bcffb74'
        self.password = '7a745b3328536de84831d5f55f56d74d'
        self.schema = XMLSchema(file=open(os.path.join('mapi.xsd'), 'rb'), attribute_defaults=True)
        self.parser = XMLParser(schema=self.schema, attribute_defaults=True)
        

    def test_params(self):
        s = hipay.PaymentParams("123", "124", "125", "126", "127")
        s.setBackgroundColor('#234567')
        s.setCaptureDay('6')
        s.setCurrency('EUR')
        s.setLocale('fr_FR')
        s.setEmailAck('test@example.org')
        s.setLogin('546432', 'password')
        s.setMedia('WEB')
        s.setRating('+18')
        s.setIdForMerchant('142545')
        s.setMerchantSiteId('234567')
        s.setMerchantDatas({'alpha':23, 'beta':34})
        s.setURLOk("http://example.org/hipay/result/ok")
        s.setURLNok("http://example.org/hipay/result/ko")
        s.setURLCancel("http://example.org/hipay/result/cancel")
        s.setURLAck("http://example.org/hipay/result/ack")
        s.setLogoURL("http://example.org/hipay/shop/logo")

        self.assertEqual(hashlib.sha224(ET.tostring(s.asTree().getroot())).hexdigest(),
                         'e0d63034a599eaab08a8a7e3d3c127b8e14d1fe123d78ebddb686490')


    def test_taxes(self):
        mta = hipay.Tax('tax')
        mestax=[dict(taxName='TVA 19.6', taxVal='19.6', percentage='true'), dict(taxName='TVA 5.5', taxVal='5.5', percentage='true')]
        mta.setTaxes(mestax)
        self.assertEqual(hashlib.sha224(ET.tostring(mta.asTree().getroot())).hexdigest(),
                         '7dab36f4b0338e2511f7778b82d5963d2b24829ae3c67e8f3a909709')

        #### Various taxes
        checksums={'shippingTax':'9e66ef9ccc2d44a66af43a9c7e6b47d923988daffb96be0113cc1842',
                   'insuranceTax':'356b55f79c38c418fc2f67093b7f78cd7e62b1840c526ddc19595c5f',
                   'fixedCostTax':'ace001c581f1ca253017e6f75443453f0bc968fb2e6fbc51b57c1c61'
                   }
        taxes = dict()
        for root in 'shippingTax', 'insuranceTax', 'fixedCostTax':
            taxes[root] = hipay.Tax(root)
            mestax=[dict(taxName='TVA', taxVal='19.6', percentage='true')]
            taxes[root].setTaxes(mestax)
            self.assertEqual(hashlib.sha224(ET.tostring(taxes[root].asTree().getroot())).hexdigest(),
                             checksums[root])

    def test_affiliatess(self):
        af = hipay.Affiliate()
        affiliates = [dict(customerId='123', accountId='764527',percentageTarget='12', val='120')]
        af.setValue(affiliates)
        self.assertEqual(hashlib.sha224(ET.tostring(af.asTree().getroot())).hexdigest(),
                             '756035cf40a2b7784fb4314b8e0428cd0d760060ee3ad2a40d904875')


    def test_products(self):
        pr = hipay.Product()
        mta = hipay.Tax('tax')
        mestax=[dict(taxName='TVA 19.6', taxVal='19.6', percentage='true'), dict(taxName='TVA 5.5', taxVal='5.5', percentage='true')]
        mta.setTaxes(mestax)
        
        products = [{'name':'The Fall of  Hyperion','info':u'Simmons, Dan – ISBN 0575076380', 'quantity':'10', 'ref':'10', 'category':'91', 'price':'120', 'tax':mta},
                {'name':'The Fall of  Hyperion','info':u'Simmons, Dan – ISBN 0575076380', 'quantity':'10', 'ref':'10', 'category':'91', 'price':'120', 'tax':mta}]
        pr.setProducts(products)
        self.assertEqual(hashlib.sha224(ET.tostring(pr.asTree().getroot())).hexdigest(),
                         'adb1fe832c8fd782f7c00803dcbafafb083d929e457aa530256ca5c2')


    def test_installement(self):
        inst = hipay.Installement()
        mta = hipay.Tax('tax')
        mestax=[dict(taxName='TVA 19.6', taxVal='19.6', percentage='true'), dict(taxName='TVA 5.5', taxVal='5.5', percentage='true')]
        mta.setTaxes(mestax)        
        data = [{'price':100, 'first':'true','paymentDelay':'1D', 'tax':mta},{'price':100, 'first':'false','paymentDelay':'1M', 'tax':mta}]
        inst.setInstallements(data)
        self.assertEqual(hashlib.sha224(ET.tostring(inst.asTree().getroot())).hexdigest(),
                         '12c360c2946a1570cd603aff58c093965785a3a7696f75a05c6c18e2')


    def test_orders(self):
        order = hipay.Order()
        af = hipay.Affiliate()
        affiliates = [dict(customerId='123', accountId='764527',percentageTarget='12', val='120')]
        af.setValue(affiliates)        
        taxes = dict()
        for root in 'shippingTax', 'insuranceTax', 'fixedCostTax':
            taxes[root] = hipay.Tax(root)
            mestax=[dict(taxName='TVA', taxVal='19.6', percentage='true')]
            taxes[root].setTaxes(mestax)
        
        data = [{'shippingAmount':1.50, 'insuranceAmount':2.00, 'fixedCostAmount':2.25, 'fixedCostTax':taxes['fixedCostTax'], 'insuranceTax': taxes['insuranceTax'], 'shippingTax':taxes['shippingTax'], 'orderTitle':'Mon ordre', 'orderInfo':'Box', 'orderCategory':91, 'affiliate':af}]
        order.setOrders(data)
        self.assertEqual(hashlib.sha224(ET.tostring(order.asTree().getroot())).hexdigest(),
                         '125146d17f12c8c198a30076bb318213a3fa71aedbe2d4d477d9e0af')

    def test_simplepayment(self):
        s = hipay.PaymentParams("84971", "84971", "84971", "84971", "84971")
        s.setBackgroundColor('#234567')
        s.setCaptureDay('6')
        s.setCurrency('EUR')
        s.setLocale('fr_FR')
        s.setEmailAck('test@example.org')
        s.setLogin('546432', 'password')
        s.setMedia('WEB')
        s.setRating('+18')
        s.setIdForMerchant('142545')
        s.setMerchantSiteId('234567')
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
        
        products = [{'name':'The Fall of  Hyperion','info':u'Simmons, Dan – ISBN 0575076380', 'quantity':'10', 'ref':'10', 'category':'91', 'price':'120', 'tax':mta},
                {'name':'The Fall of  Hyperion','info':u'Simmons, Dan – ISBN 0575076380', 'quantity':'10', 'ref':'10', 'category':'91', 'price':'120', 'tax':mta}]
        pr.setProducts(products)
        
        order = hipay.Order()
        af = hipay.Affiliate()
        affiliates = [dict(customerId='123', accountId='764527',percentageTarget='12', val='120')]
        af.setValue(affiliates)        
        taxes = dict()
        for root in 'shippingTax', 'insuranceTax', 'fixedCostTax':
            taxes[root] = hipay.Tax(root)
            mestax=[dict(taxName='TVA', taxVal='19.6', percentage='true')]
            taxes[root].setTaxes(mestax)
        
        data = [{'shippingAmount':1.50, 'insuranceAmount':2.00, 'fixedCostAmount':2.25, 'fixedCostTax':taxes['fixedCostTax'], 'insuranceTax': taxes['insuranceTax'], 'shippingTax':taxes['shippingTax'], 'orderTitle':'Mon ordre', 'orderInfo':'Box', 'orderCategory':91, 'affiliate':af}]
        order.setOrders(data)
        pay = hipay.HiPay(s)        
        pay.SimplePayment(order, pr)
        self.assertEqual(hashlib.sha224(ET.tostring(pay.asTree().getroot())).hexdigest(),
                         'e70d425bd61c9b41767d4cf54dcced64d5d5d21e01e80b7859ba380a')
        root = fromstring(ET.tostring(pay.asTree().getroot()), self.parser)
        # Validate against the provided schema  https://payment.hipay.com/schema/mapi.xs
        self.assertIsInstance(root, _Element)
        self.assertTrue(pay.validate())

    def test_send_simplepayment(self):
        s = hipay.PaymentParams("84971", "84971", "84971", "84971", "84971")
        s.setBackgroundColor('#234567')
        s.setCaptureDay('6')
        s.setCurrency('EUR')
        s.setLocale('fr_FR')
        s.setEmailAck('test@example.org')
        s.setLogin('84971', '313666')
        s.setMedia('WEB')
        s.setRating('+18')
        s.setIdForMerchant('142545')
        s.setMerchantSiteId('3194')
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
        
        products = [{'name':'The Fall of  Hyperion','info':u'Simmons, Dan – ISBN 0575076380', 'quantity':'10', 'ref':'10', 'category':'91', 'price':'120', 'tax':mta},
                {'name':'The Fall of  Hyperion','info':u'Simmons, Dan – ISBN 0575076380', 'quantity':'10', 'ref':'10', 'category':'91', 'price':'120', 'tax':mta}]
        pr.setProducts(products)
        
        order = hipay.Order()
        af = hipay.Affiliate()
        affiliates = [dict(customerId='123', accountId='764527',percentageTarget='12', val='120')]
        af.setValue(affiliates)        
        taxes = dict()
        for root in 'shippingTax', 'insuranceTax', 'fixedCostTax':
            taxes[root] = hipay.Tax(root)
            mestax=[dict(taxName='TVA', taxVal='19.6', percentage='true')]
            taxes[root].setTaxes(mestax)
        
        data = [{'shippingAmount':1.50, 'insuranceAmount':2.00, 'fixedCostAmount':2.25, 'fixedCostTax':taxes['fixedCostTax'], 'insuranceTax': taxes['insuranceTax'], 'shippingTax':taxes['shippingTax'], 'orderTitle':'Mon ordre', 'orderInfo':'Box', 'orderCategory':91}]
        order.setOrders(data)
        pay = hipay.HiPay(s)        
        pay.SimplePayment(order, pr)
        root = fromstring(ET.tostring(pay.asTree().getroot()), self.parser)
        # Validate against the provided schema  https://payment.hipay.com/schema/mapi.xs
        self.assertIsInstance(root, _Element)
        self.assertTrue(pay.validate())
        response = pay.SendPayment("https://test-payment.hipay.com/order/")
        self.assertEquals(response['status'], 'Accepted')
        


    def test_multiplepayment(self):
        s = hipay.PaymentParams("84971", "84971", "84971", "84971", "84971")
        s.setBackgroundColor('#234567')
        s.setCaptureDay('6')
        s.setCurrency('EUR')
        s.setLocale('fr_FR')
        s.setEmailAck('test@example.org')
        s.setLogin('546432', 'password')
        s.setMedia('WEB')
        s.setRating('+18')
        s.setIdForMerchant('142545')
        s.setMerchantSiteId('234567')
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
        
        products = [{'name':'The Fall of  Hyperion','info':u'Simmons, Dan – ISBN 0575076380', 'quantity':'10', 'ref':'10', 'category':'91', 'price':'120', 'tax':mta},
                    {'name':'The Fall of  Hyperion','info':u'Simmons, Dan – ISBN 0575076380', 'quantity':'10', 'ref':'10', 'category':'91', 'price':'120', 'tax':mta}]
        pr.setProducts(products)
        
        order = hipay.Order()
        af = hipay.Affiliate()
        affiliates = [dict(customerId='123', accountId='764527',percentageTarget='12', val='120')]
        af.setValue(affiliates)        
        taxes = dict()
        for root in 'shippingTax', 'insuranceTax', 'fixedCostTax':
            taxes[root] = hipay.Tax(root)
            mestax=[dict(taxName='TVA', taxVal='19.6', percentage='true')]
            taxes[root].setTaxes(mestax)
        
        order_data = [{'shippingAmount':1.50, 'insuranceAmount':2.00, 'fixedCostAmount':2.25, 'fixedCostTax':taxes['fixedCostTax'], 'insuranceTax': taxes['insuranceTax'], 'shippingTax':taxes['shippingTax'], 'orderTitle':'Mon ordre 2', 'orderInfo':'Box 2', 'orderCategory':91, 'affiliate':af}, {'shippingAmount':1.50, 'insuranceAmount':2.00, 'fixedCostAmount':2.25, 'fixedCostTax':taxes['fixedCostTax'], 'insuranceTax': taxes['insuranceTax'], 'shippingTax':taxes['shippingTax'], 'orderTitle':'Mon ordre', 'orderInfo':'Box', 'orderCategory':91, 'affiliate':af}]
        order.setOrders(order_data)

        inst = hipay.Installement()
        mta = hipay.Tax('tax')
        mestax=[dict(taxName='TVA 19.6', taxVal='19.6', percentage='true'), dict(taxName='TVA 5.5', taxVal='5.5', percentage='true')]
        mta.setTaxes(mestax)        
        inst_data = [{'price':100, 'first':'true','paymentDelay':'1D', 'tax':mta},{'price':100, 'first':'false','paymentDelay':'1M', 'tax':mta}]
        inst.setInstallements(inst_data)
        
        pay = hipay.HiPay(s)        
        pay.MultiplePayment(order, inst)
        self.assertEqual(hashlib.sha224(ET.tostring(pay.asTree().getroot())).hexdigest(),
                         '319b6b3829f244cb34c5083b14c9feb5075f20d628210060d851f3d6')
        root = fromstring(ET.tostring(pay.asTree().getroot()), self.parser)
        # Validate against the provided schema  https://payment.hipay.com/schema/mapi.xs
        self.assertIsInstance(root, _Element)
        self.assertTrue(pay.validate())

    def test_send_multiplepayment(self):
        s = hipay.PaymentParams("84971", "84971", "84971", "84971", "84971")
        s.setBackgroundColor('#234567')
        s.setCaptureDay('6')
        s.setCurrency('EUR')
        s.setLocale('fr_FR')
        s.setEmailAck('test@example.org')
        s.setLogin('84971', '313666')
        s.setMedia('WEB')
        s.setRating('+18')
        s.setIdForMerchant('142545')
        s.setMerchantSiteId('3194')
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
        
        products = [{'name':'The Fall of  Hyperion','info':u'Simmons, Dan – ISBN 0575076380', 'quantity':'10', 'ref':'10', 'category':'91', 'price':'120', 'tax':mta},
                    {'name':'The Fall of  Hyperion','info':u'Simmons, Dan – ISBN 0575076380', 'quantity':'10', 'ref':'10', 'category':'91', 'price':'120', 'tax':mta}]
        pr.setProducts(products)
        
        order = hipay.Order()
        af = hipay.Affiliate()
        affiliates = [dict(customerId='123', accountId='764527',percentageTarget='12', val='120')]
        af.setValue(affiliates)        
        taxes = dict()
        for root in 'shippingTax', 'insuranceTax', 'fixedCostTax':
            taxes[root] = hipay.Tax(root)
            mestax=[dict(taxName='TVA', taxVal='19.6', percentage='true')]
            taxes[root].setTaxes(mestax)
        
        order_data = [{'shippingAmount':1.50, 'insuranceAmount':2.00, 'fixedCostAmount':2.25, 'fixedCostTax':taxes['fixedCostTax'], 'insuranceTax': taxes['insuranceTax'], 'shippingTax':taxes['shippingTax'], 'orderTitle':'Mon ordre 2', 'orderInfo':'Box 2', 'orderCategory':91}, {'shippingAmount':1.50, 'insuranceAmount':2.00, 'fixedCostAmount':2.25, 'fixedCostTax':taxes['fixedCostTax'], 'insuranceTax': taxes['insuranceTax'], 'shippingTax':taxes['shippingTax'], 'orderTitle':'Mon ordre', 'orderInfo':'Box', 'orderCategory':91}]
        order.setOrders(order_data)

        inst = hipay.Installement()
        mta = hipay.Tax('tax')
        mestax=[dict(taxName='TVA 19.6', taxVal='19.6', percentage='true'), dict(taxName='TVA 5.5', taxVal='5.5', percentage='true')]
        mta.setTaxes(mestax)        
        inst_data = [{'price':100, 'first':'true','paymentDelay':'1D', 'tax':mta},{'price':100, 'first':'false','paymentDelay':'1M', 'tax':mta}]
        inst.setInstallements(inst_data)
        
        pay = hipay.HiPay(s)        
        pay.MultiplePayment(order, inst)
        root = fromstring(ET.tostring(pay.asTree().getroot()), self.parser)
        # Validate against the provided schema  https://payment.hipay.com/schema/mapi.xs
        self.assertIsInstance(root, _Element)
        self.assertTrue(pay.validate())
        response = pay.SendPayment("https://test-payment.hipay.com/order/")
        self.assertEquals(response['status'], 'Accepted')


    def test_parse_ack(self):
        ack = """<?xml version="1.0" encoding="UTF-8"?> <mapi>
<mapiversion>1.0</mapiversion> <md5content>c0783cc613bf025087b8bf5edecac824</md5content> <result>
<operation>capture</operation> <status>ok</status>
<date>2010-02-23</date>
<time>10:32:12 UTC+0000</time> <transid>4B83AEA905C49</transid> <origAmount>10.20</origAmount> <origCurrency>EUR</origCurrency> <idForMerchant>REF6522</idForMerchant> <emailClient>email_client@hipay.com</emailClient> <merchantDatas>
<_aKey_id_client>2000</_aKey_id_client>
<_aKey_credit>10</_aKey_credit> </merchantDatas>
<subscriptionId>753EA685B55651DC40F0C2784D5E1170</subscriptionId> (si la transaction est liée à un abonnement)
<refProduct0>REF6522</refProduct0>
</result> </mapi>"""
        res = hipay.ParseAck(ack)
        expected_res = {'status': 'ok',
                        'origAmount': '10.20',
                        'emailClient':'email_client@hipay.com',
                        'date': datetime.datetime(2010, 2, 23, 0, 0),
                        'operation': 'capture',
                        'transid': '4B83AEA905C49',
                        'merchantDatas': {'_aKey_id_client': '2000',
                                          '_aKey_credit': '10'},
                        'origCurrency': 'EUR',
                        'idForMerchant': 'REF6522',
                        'refProduct': 'REF6522',
                        'time': datetime.datetime(1900, 1, 1, 10, 32, 1),
                        'subscriptionId': '753EA685B55651DC40F0C2784D5E1170',
                        'not_tampered_with': False,
                        'not_tempered_with': False}

        self.assertEqual(res, expected_res)

    def test_check_md5(self):
        xml = '<r><md5content>%s</md5content>%s</r>'

        result = u'<result> \n<some>a </some> <stuff> a</stuff></result>'
        md5 = hashlib.md5()
        md5.update(result)
        xml_right_hash = xml % (md5.hexdigest(), result)
        self.assertTrue(hipay.CheckMD5(xml_right_hash))

        xml_wrong_hash = xml % ('deadb33f', result)
        self.assertFalse(hipay.CheckMD5(xml_wrong_hash))


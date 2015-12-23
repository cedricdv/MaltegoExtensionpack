import time

__author__ = 'Cedric'
# Maltego transform: Ondertekenaars van Geneeskunde van het volk

from MaltegoTransform import *
import sys
import os
import requests
from lxml import html, etree

m = MaltegoTransform()

# m.parseArguments(sys.argv)
#
# website = m.getVar('fqdn')
# port = m.getVar('ports')
# port = port.split(',')
# ssl = m.getVar('website.ssl-enabled')
# robots = []

try:
    url = 'http://www.gvhv-mplp.be/index.php/nl/ondertekenaars'
    r = requests.get(url)
    if r.status_code == 200:
        # robots = str(r.text).split('\n')
        page = html.fromstring(r.content)
        # tree = etree.fromstring(r.content)
        rows = page.xpath('//tr')

        for row in rows:
            name = ''
            firstname = ''
            job = ''
            postalcode = ''
            email = ''
            phonenr = ''
            volunteer = False
            try:
                name = sanitise(str.strip(row.xpath('./td[1]/text()')[0]))
                fullname = name
                if row.xpath('./td[2]/text()'):
                    firstname = sanitise(row.xpath('./td[2]/text()')[0])
                    fullname = str.strip(firstname + ' ' + fullname)
                if row.xpath('./td[3]/text()'):
                    job = sanitise(row.xpath('./td[3]/text()')[0])
                if row.xpath('./td[4]/text()'):
                    postalcode = sanitise(row.xpath('./td[4]/text()')[0])
                if row.xpath('./td[5]/text()'):
                    email = sanitise(row.xpath('./td[5]/text()')[0])
                if row.xpath('./td[6]/text()'):
                    phonenr = sanitise(row.xpath('./td[6]/text()')[0])
                if row.xpath('./td[7]/text()'):
                    volunteer = sanitise(str.strip(row.xpath('./td[7]/text()')[0]).upper()) == 'Ik wil graag meewerken!'.upper()

                ent = m.addEntity('maltego.Person', fullname)
                ent.addAdditionalFields("person.fullname","Full Name",True,fullname)
                ent.addAdditionalFields("person.firstnames","First Names",True,firstname)
                ent.addAdditionalFields("person.lastname","Surname",True,name)
                ent.addAdditionalFields("person.job","Job/Function",True,job)
                ent.addAdditionalFields("person.postalcode","Postal Code",True,postalcode)
                ent.addAdditionalFields("person.email","Email Address",True,email)
                ent.addAdditionalFields("person.phone","Phone",True,phonenr)
                ent.addAdditionalFields("person.voluteer","Volunteer",True,volunteer)
            except Exception as e:
                pass
    else:
        m.addUIMessage("Page not found")
except Exception as e:
    m.addUIMessage(str(e))

m.returnOutput()
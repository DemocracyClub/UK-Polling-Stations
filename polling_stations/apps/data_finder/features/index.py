# -*- coding: utf-8 -*-
import os
import re
import json

from lxml import html

from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core.management import call_command

from lettuce import *
from lettuce.django import django_url



@before.all
def set_browser():
    world.browser = Client()

@before.all
def load_fixtures():
    call_command('loaddata', 'polling_stations/apps/pollingstations/fixtures/initial_data.json')

@step(u'Given I put in the postcode "([^"]*)"')
def postcode_search(step, postcode):
    url = reverse('postcode_view', args=(postcode,))
    postcode_url = django_url(url)
    response = world.browser.get(postcode_url)
    assert response.status_code == 200, "Postcode not found"
    world.dom = html.fromstring(response.content)

@step(u'I should be told to vote at "([^"]*)"')
def vote_at(step, station_name):
    assert station_name in world.dom.text_content(), "Station name not found"


@step(u'And the council\'s phone number is "([^"]*)"')
def councils_phone_number(step, number):
    assert number in world.dom.text_content(), "Council number not found"

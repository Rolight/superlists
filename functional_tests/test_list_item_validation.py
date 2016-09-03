#!/usr/bin/env python3
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip

import sys

class ItemValidationTest(FunctionalTest):
    
    def test_cannot_add_empty_list_items(self):
        self.fail('write me!')
        


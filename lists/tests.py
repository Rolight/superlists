from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item

import re

def remove_csrf_token(content):
	p = re.compile("<.*?name='csrfmiddlewaretoken'.*?>")
	return re.sub(p, '', content)

	
def none_empty_ch(content):
	p = re.compile('\s')
	return re.sub(p, '', content)

def pure(content):
	return none_empty_ch(remove_csrf_token(content))

class HomePageTest(TestCase):
	
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		# We shouldn't test const varible
		expected_html = render_to_string('lists/home.html')
		response_content = remove_csrf_token(response.content.decode())
		self.assertEqual(
			none_empty_ch(response_content),
			none_empty_ch(expected_html),
			'\nexpect:\n%s\nbut:\n%s\n' % (expected_html, response_content)
		)

	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'

		response = home_page(request)
		self.assertIn('A new list item', response.content.decode())

		expected_html = render_to_string(
			'lists/home.html',
			{'new_item_text': 'A new list item'}
		)
		self.assertEqual(pure(response.content.decode()), pure(expected_html))

class ItemModelTest(TestCase):
	
	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, first_item.text)
		self.assertEqual(second_saved_item.text, second_item.text)

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
    
    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

class NewListTest(TestCase):

    # if we modified database, the url shouldn't endwith '/'
    def test_saving_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()

        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'lists/list.html')

 
    def test_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')


   


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



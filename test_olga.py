from playwright.sync_api import sync_playwright
import pytest
import time

@pytest.fixture # функция кот вызывается перед каждым тестом и возвращает page
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page =browser.new_page()
        yield page # дает возможность дальше продолжать код (аналог return но...)
        browser.close()

# pytest -s main.py::test_add_product_to_cart (определ функция с выводом принтов print())
# pytest main.py::test_main_input (определенная функция)
# pytest main.py -m sort (запуск тест с опреденным параметром)
# def page_auth (добавить фикстуру)

@pytest.mark.parametrize("username, password, expected_url, key_enter", [
     ("standard_user", "secret_sauce", "https://www.saucedemo.com/inventory.html", False),
     ("standard_user", "secret", "https://www.saucedemo.com/", False), # неверный пароль
     ("locked_out_user", "secret_sauce", "https://www.saucedemo.com/", False),# заблокированный пользователь
     ("standard_user", "secret_sauce", "https://www.saucedemo.com/inventory.html", True)
])
@pytest.mark.auth
def test_main_input(page, username, password, expected_url, key_enter):
        page.goto("https://www.saucedemo.com/")
        input_username = page.locator("#user-name")
        input_username.fill(username)
        
        input_password = page.locator("#password")
        input_password.fill(password)
        
        if key_enter == True:
            page.keyboard.press('Enter')
           
        else:
            add_btn = page.locator("#login-button")
            add_btn.click()
            url_page = page.url
            assert expected_url == url_page

        if "inventory.html" in expected_url:
            items = page.locator(".inventory_item_name")
            assert items.count() > 0


@pytest.mark.parametrize("username, password, message", [
     ("standard_user", "secret", "Username and password do not match"), # неверный пароль
     ("locked_out_user", "secret_sauce", "user has been locked out")# заблокированный пользователь
])

@pytest.mark.auth
def test_сheck_message_invalid_data(page, username, password, message):
        page.goto("https://www.saucedemo.com/")
        input_username = page.locator("#user-name")
        input_username.fill(username)
        
        input_password = page.locator("#password")
        input_password.fill(password)
        
        add_btn = page.locator("#login-button")
        add_btn.click()
     
        error_btn = page.locator("h3").inner_text()
        assert  message in error_btn # проверка сод ли сообщение об ошибке текст

@pytest.fixture # функция кот вызывается перед каждым тестом и возвращает page
def page_auth(): 
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page_auth = browser.new_page()
        page_auth.goto("https://www.saucedemo.com/")
        input_username = page_auth.locator("#user-name")
        input_username.fill("standart_user")
        input_password = page_auth.locator("#password")
        input_password.fill("secret_sauce")
        add_btn = page_auth.locator("#login-button")
        add_btn.click()
        yield page_auth # дает возможность дальше продолжать код (аналог return но...)
        browser.close()





@pytest.mark.sort 
@pytest.mark.parametrize("sort, value, rev", [
     ("name_product", "az", False),
     ("name_product", "za", True),
     ("price_product","lohi", False),
     ("price_product", "hilo", True)
])      
def test_sort(page_auth, sort, value, rev):
     btn_sort = page_auth.locator(".product_sort_container")
     btn_sort.select_option(value) # использ вып окно сортировки

     if sort == "price_product":
        sorted_values = page_auth.locator(".inventory_item_price").all_inner_texts()                          
        values = [float(p.lstrip('$')) for p in sorted_values] 
     else:
        values = page_auth.locator(".inventory_item_name").all_inner_texts() 

     sorted_values = sorted(values, reverse=rev)
     assert sorted_values == values

@pytest.mark.add
def test_add_product_to_cart(page_auth):
     button = page_auth.locator("#add-to-cart-sauce-labs-backpack")
     button.click()
     count_shopping = page_auth.locator(".shopping_cart_badge").inner_text()
     assert int(count_shopping) == 1
    
     names_products = page_auth.locator(".inventory_item_name ").all_inner_texts()
     prices_products = page_auth.locator(".inventory_item_price").all_inner_texts()
   

     btn_first_product = page_auth.locator("#item_4_title_link")
     btn_first_product.click()
     open_name_first_products = page_auth.locator(".inventory_details_name").text_content() 
     assert open_name_first_products == names_products[0]

     open_price_first_products = page_auth.locator(".inventory_details_price").text_content()
     assert open_price_first_products == prices_products[0]
     print(open_price_first_products)  

     
     
     
   


     
    
    
    

       


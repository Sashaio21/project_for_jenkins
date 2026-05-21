from playwright.sync_api import sync_playwright
import pytest
import time



# [pytest]
# markers =
#     auth:  авторизациия 
#     cart:  корзина
#     products: товары



@pytest.fixture 
def page():
    with sync_playwright() as p: 
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        yield page 
        
        browser.close()
        
@pytest.mark.auth        
def test_autorisation(page):
    
    page.goto('https://www.saucedemo.com/')
    
    enter_name = page.locator("[data-test='username']")
    enter_name.fill('standard_user')
    
    enter_password = page.locator("[data-test='password']")
    enter_password.fill('secret_sauce')
    
    login = page.locator("[data-test='login-button']")
    login.click()
    
    current_url = page.url
    assert current_url == 'https://www.saucedemo.com/inventory.html'
    
    items_on_site = page.locator("[data-test='inventory-item-name']")
    all_items = items_on_site.count()
    
    assert all_items > 0 
    
    time.sleep(2)

@pytest.mark.auth            
def test_locked_out_user(page):
    
    page.goto('https://www.saucedemo.com/')
    
    enter_name = page.locator("[data-test='username']")
    enter_name.fill('locked_out_user')
    
    enter_password = page.locator("[data-test='password']")
    enter_password.fill('secret_sauce')
    
    login = page.locator("[data-test='login-button']")
    login.click()
    
    
    assert page.url == 'https://www.saucedemo.com/'
    
    error_text = page.locator("[data-test='error']").inner_text()
    assert error_text == 'Epic sadface: Sorry, this user has been locked out.'

@pytest.mark.auth        
def test_wrong_password(page):
    
    page.goto('https://www.saucedemo.com/')
    
    enter_name = page.locator("[data-test='username']")
    enter_name.fill('locked_out_user')
    
    enter_password = page.locator("[data-test='password']")
    enter_password.fill('wrong_password')
    
    login = page.locator("[data-test='login-button']")
    login.click()
    
    assert page.url == 'https://www.saucedemo.com/'
    error_text = page.locator("[data-test='error']").inner_text()
    
    assert error_text == 'Epic sadface: Username and password do not match any user in this service'


    
@pytest.fixture 
def cart():
    with sync_playwright() as p: 
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto('https://www.saucedemo.com/')
    
        enter_name = page.locator("[data-test='username']")
        enter_name.fill('problem_user')
    
        enter_password = page.locator("[data-test='password']")
        enter_password.fill('secret_sauce')
    
        login = page.locator("[data-test='login-button']")
        login.click()
        
        yield page 
        
        browser.close()




@pytest.mark.cart 
def test_item_to_cart(cart):
    
    item = cart.locator("[data-test='add-to-cart-sauce-labs-backpack']").all()
   
        
    clicks = 0
    for i in item:
        i.click()
        clicks +=1
        
    
    count_in_cart = cart.locator("[data-test='shopping-cart-badge']")
    cart_text = int(count_in_cart.inner_text())
    
    assert clicks == cart_text
    
    cart.goto('https://www.saucedemo.com/cart.html')
    name_item_in_cart = cart.locator("[data-test='inventory-item-name']").inner_text()
    price_item_in_cart = cart.locator("[data-test='inventory-item-price']").inner_text()
    
    clean_price = price_item_in_cart.replace("$", "")
    price_float = float(clean_price)
    expected_price = 29.99
    
    # хотел реализовать проверки таким образом , чтобы проходится циклом по выбранному/выбранным товарам 
    # и сразу доставать из этих товаров название товара и цену товара
    # а потом автоматочески подставлять это в проверку , у самого не получилось , хочу разобрать как это сделать
    
    assert price_float == expected_price
    assert name_item_in_cart == 'Sauce Labs Backpack'
    
    
    
    
    
    time.sleep(2)
    
    
# def test_sort_from_A_to_Z(cart):
    
#     sort = cart.locator("[data-test='product-sort-container']")
#     sort.select_option("az")
    
#     time.sleep(1)
    
#     product_names_elements = cart.locator(".inventory_item_name").all_inner_texts()
#     expected_sorted_list = sorted(product_names_elements)
#     assert product_names_elements == expected_sorted_list
    
# def test_sort_from_Z_to_A(cart):
#     sort = cart.locator("[data-test='product-sort-container']")
#     sort.select_option("za")
    
#     time.sleep(1)
    
#     product_names_elements = cart.locator(".inventory_item_name").all_inner_texts()
#     expected_sorted_list = sorted(product_names_elements, reverse=True)
    
#     assert product_names_elements == expected_sorted_list


# def test_sort_products_price_low_to_high(cart):
#     sort_dropdown = cart.locator("[data-test='product-sort-container']")
#     sort_dropdown.select_option("lohi")
    
#     time.sleep(1)
    
#     prices_as_strings = cart.locator(".inventory_item_price").all_inner_texts()
    
#     prices_as_floats = []
#     for price in prices_as_strings:
#         clean_price = price.replace('$','')
#         price_number = float(clean_price)
#         prices_as_floats.append(price_number)
#     expected_sorted_prices = sorted(prices_as_floats)
#     assert prices_as_floats == expected_sorted_prices
    
# def test_sort_products_price_high_to_low(cart):
#     sort_dropdown = cart.locator("[data-test='product-sort-container']")
#     sort_dropdown.select_option("hilo")
    
#     time.sleep(1)
    
#     prices_as_strings = cart.locator(".inventory_item_price").all_inner_texts()
    
#     prices_as_floats = []
#     for price in prices_as_strings:
#         clean_price = price.replace('$','')
#         float_price = float(clean_price)
#         prices_as_floats.append(float_price)
    
#     expected_sorted_prices = sorted(prices_as_floats,reverse=True)
    
#     assert prices_as_floats == expected_sorted_prices


@pytest.mark.parametrize("sort_option, data_type, reverse", [
    ("az", "name", False),
    ("za", "name", True),
    ("lohi", "price", False),
    ("hilo", "price", True)
])
@pytest.mark.products 
def test_saucedemo_sorting(cart, sort_option, data_type, reverse):
    
    # с помощью select_option взаимодействуем с дропдауном. sort_option == 'az' , 'za', 'lohi' , 'hilo' 
    cart.select_option("[data-test='product-sort-container']", value=sort_option)
    
    #  В зависимости от того что у нас попадает в sort_option программа идет либо в data_type == "name"(сортировка по названию), либо в data_type == "price"(сортировка по цене)

    if data_type == "name":
        ui_items = cart.locator("[data-test='inventory-item-name']").all_text_contents()
        expected_items = sorted(ui_items, reverse=reverse)
        
    elif data_type == "price":
        raw_prices = cart.locator("[data-test='inventory-item-price']").all_text_contents()
        ui_items = [float(price.replace("$", "")) for price in raw_prices]
        expected_items = sorted(ui_items, reverse=reverse)
        
    assert ui_items == expected_items

    
    

    

    
    
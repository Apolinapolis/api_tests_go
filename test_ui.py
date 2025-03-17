import allure
import requests
import logging
from selene import browser
from selene.support.conditions import be
from selene.support.conditions import have
from selene.core.query import text as get_text


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


URL_SHOP = 'https://demowebshop.tricentis.com/'
LOGIN = 'larra11@ya.ru'
PASSWORD = 123123
PRODUCT_ID = "45"
PRODUCT_NAME = "Fiction"



def authorize_and_get_cookies():
    """Авторизация через API и получение cookies."""
    with allure.step("Login via API"):
        post_response = requests.post(
            url=URL_SHOP + 'login',
            data={'Email': LOGIN, 'Password': PASSWORD, 'RememberMe': False},
            allow_redirects=False
        )
        assert post_response.status_code == 302, f"Failed to login. Status code: {post_response.status_code}"
        allure.attach(body=post_response.text, name='Response', attachment_type=allure.attachment_type.TEXT)
        allure.attach(body=str(post_response.cookies), name="Cookies", attachment_type=allure.attachment_type.TEXT)

        cookie = post_response.cookies.get('NOPCOMMERCE.AUTH')
        assert cookie, "Cookie 'NOPCOMMERCE.AUTH' not found in response"

    return post_response.cookies.get_dict()

headers = {
    "Connection": "keep-alive",
    "Accept": '*/*',
    "Accept-Encoding": "gzip, deflate, br"
}


@allure.title("Successful authorization via API")
def test_login_though_api():
    """Проверка успешной авторизации через API."""
    cookies = authorize_and_get_cookies()
    with allure.step("Set cookies"):
        browser.open(URL_SHOP)
        for name, value in cookies.items():
            browser.driver.add_cookie({"name": name, "value": value})
        browser.open(URL_SHOP)

    with allure.step("Verify successful login"):
        browser.element('.account').should(have.text(LOGIN))


@allure.title("Check product in cart via API and UI")
def test_current_product_in_cart():
    """Проверка добавления товара в корзину через API и его отображения в UI."""
    cookies = authorize_and_get_cookies()
    with allure.step("Add product to cart by API"):
        url = f"{URL_SHOP}/addproducttocart/catalog/{PRODUCT_ID}/1/1"
        post_response = requests.post(url, headers=headers, cookies=cookies)
        assert post_response.status_code==200, f"Failed to add product to cart. Status code:{post_response.status_code}"

    with allure.step("Set cookies in browser"):
        browser.open(URL_SHOP)
        for name, value in cookies.items():
            browser.driver.add_cookie({"name": name, "value": value})
        browser.open(URL_SHOP)

    with allure.step("Open tab Cart and check product"):
        browser.element("#topcartlink .cart-label").click()
        browser.element(".product-name").should(be.visible)

    with allure.step("Verify product name in cart"):
        cart_items = browser.all("a.product-name")
        assert any(get_text(item) == PRODUCT_NAME for item in cart_items), f"Product '{PRODUCT_NAME}' not found in cart"


@allure.title("Check product in wishlist via API and UI")
def test_current_product_in_wishlist():
    """Проверка добавления товара в wishList через API и его отображения в UI."""
    cookies = authorize_and_get_cookies()
    with allure.step("Add product to wishList"):
        url = f"{URL_SHOP}/addproducttocart/details/28/2"
        post_response = requests.post(url, headers=headers, cookies=cookies)
        assert post_response.status_code==200, f"add product to wishList. Status code:{post_response.status_code}"

    with allure.step("Set cookies"):
        browser.open(URL_SHOP)
        for name, value in cookies.items():
            browser.driver.add_cookie({"name": name, "value": value})
        browser.open(URL_SHOP)
        logger.info(f"Cookies set in browser: {browser.driver.get_cookies()}")

    with allure.step("Open tab wishList and check product"):
        browser.element("a.ico-wishlist").click()
        browser.element(".page-title").should(have.text("Wishlist"))

    with allure.step("Verify product name in cart"):
        wishlist_items = browser.all("td.product")
        target = any( item.element("a[href='/blue-and-green-sneaker']").matching(have.text("Blue and green Sneaker"))
            for item in wishlist_items)
        assert target, "Product 'Blue and green Sneaker' not found in Wishlist"
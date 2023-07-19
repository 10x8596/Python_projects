# Selenium allows us to automate our browser, and we download the webdriver
# which is a executable file, for whatever browser we want to use so that
# selenium can use that executable file to automate that specific browser
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

# browser variable
driver = webdriver.Chrome()

def get_images_from_browser(driver, delay, max_images):
    '''
    Function to scrape the images from the browser
    '''
    def scroll_down(driver):
        '''
        This function scrolls down the page
        '''
        # executes javascript script to scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Gives time to load the images if scrolling down the page
        time.sleep(delay)

    # url of the google images page to scrape from
    url = "https://www.google.com/search?q=cat&tbm=isch&ved=2ahUKEwit-M-2oJqAAxWdj2MGHQEYDB4Q2"
    "-cCegQIABAA&oq=cat&gs_lcp=CgNpbWcQAzIECCMQJzIECCMQJzIKCAAQigUQsQMQQzIHCAAQigUQQzIHCAAQigUQQ"
    "zIKCAAQigUQsQMQQzIHCAAQigUQQzIICAAQgAQQsQMyCAgAEIAEELEDMgoIABCKBRCxAxBDOgUIABCABFDdBVjdBWC6C"
    "GgAcAB4AIABpgGIAcECkgEDMC4ymAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=bZG3ZO2NOp2fjuMPgb"
    "Cw8AE&bih=811&biw=1355"

    # Use web driver to get the html source of the page
    driver.get(url)
    # Use set() to make sure there's no duplicate urls (images)
    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        # Scroll to the bottom of the page, find all the image thumbnails on the page,
        # loop through all of them and try to click on them. Once clicked get the source of the images
        scroll_down(driver)
        # get thumbnails of images that contain this class name in the source tag
        thumbnails = driver.find_elements(By.CLASS_NAME, "Q4LuWd")
        # loop through thumbnails and try to click on them. Avoid adding same thumbnails using len()
        for img in thumbnails[len(image_urls) + skips: max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue
            images = driver.find_elements(By.CLASS_NAME, "r48jcc") # r48jcc pT0Scc iPVvYb

            # Image Validity check
            # class name could return multiple images, so we loop through all the images 
            # the class name returns to do some checks. If images have a proper image
            # source, we add the url to the image_urls set.
            for image in images:
                # If image has already been found, increment the the len of image_urls and max_images
                # to continue scraping
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break
                # Check attributes of image to see if it has src tag
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)} image")
                    
    return image_urls


def download_image(download_path, url, file_name):
    '''
    Function to download image from a web browser
    '''
    try:
        # Get the content of the image
        image_content = requests.get(url).content
        # storing image content in memory as binary data type (storing file in memory)
        image_file = io.BytesIO(image_content)
        # Convert the binary data to an Pillow image which allows us to easily save the img
        image = Image.open(image_file)
        # generate the path to save the file by combining the download path and the file name
        file_path = download_path + file_name

        # open a brand new file (f) at the file path in write bytes mode
        with open(file_path, "wb") as f:
            # save the image to the new file as JPEG
            image.save(f, "JPEG")

        print(f"Image successfully saved as: {file_path}")
    except Exception as e:
        print("FAILED -", e)


# Get all image's urls
urls = get_images_from_browser(driver, 1, 5)

# loop through all the urls and call the download_image() function
# empty string means download in the current directory
for i, url in enumerate(urls):
    download_image("imgs/", url, str(i) + ".jpg")

# Close the browser window at the end
driver.quit()
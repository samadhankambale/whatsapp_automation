import bottle_websocket
import sys
sys.modules["bottle.ext.websocket"] = bottle_websocket
import eel, time, os, openpyxl, random, requests, Environ
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime as dt


def delay():
    hold = random.randint(2, 3)
    return hold


def send_to(browser, contact, message, imagePath, documentPath):
    search_box_x_path = Environ.search_box_x_path
    try:
        search_box = browser.find_element(By.XPATH, search_box_x_path)
    except:
        return 3

    search_box.click()

    # If something is written on search box, then clear it
    try:
        try:
            clear_btn = browser.find_element(By.XPATH, Environ.cancel_btn_x_path)
            time.sleep(delay())
            clear_btn.click()
        except:
            print("Cancel not found")
    except:
        pass

    time.sleep(delay())
    search_box = browser.find_element(By.XPATH, search_box_x_path)
    search_box.send_keys(contact)

    time.sleep(delay())
    try:
        browser.find_element(By.XPATH, Environ.first_result_x_path).click()
        print("Contact clicked successfully")
    except:
        print("first_result_x_path NOT FOUND")
    time.sleep(3)
    try:
        current_user_name = browser.find_element(
            By.XPATH, Environ.chat_label_x_path
        ).text
        print(f"Chat opened: {current_user_name}")
    except:
        print("chat_label_x_path NOT FOUND")
    try:
        try:
            current_user_name = browser.find_element(
                By.XPATH, Environ.chat_label_x_path
            ).text
        except:
            current_user_name = browser.find_element(
                By.XPATH, Environ.group_label_x_path
            ).text
    except:
        return 2
    if Environ.previous_user_name:
        print(f"Previous user name: {Environ.previous_user_name}")
    if current_user_name:
        print(f"Current user name: {current_user_name}")
    if current_user_name == Environ.previous_user_name:
        Environ.unsend_contacts.append(contact)
        return 2
    elif current_user_name != Environ.previous_user_name or not Environ.previous_user_name:
        Environ.previous_user_name = current_user_name
    time.sleep(3)

    # for msg
    if message:
        try:
            chat_box = browser.find_element(By.XPATH, Environ.chat_box_x_path)
            chat_box.click()
        except:
            print("Chat Box X Path not found")
            return 3
        content = message
        active_element = browser.switch_to.active_element
        for i in range(len(content)):
            for j in range(len(content[i])):
                if content[i][j][0] == "\n":
                    active_element.send_keys(Keys.SHIFT, "\n")
                elif content[i][j][0] in all_possible_characters:
                    active_element.send_keys(content[i][j])
                elif not content[i][j][0] in all_possible_characters and content[i][j][0] != "\n":
                    emoji_name = emoji.demojize(content[i][j])
                    emoji_name = emoji_name.replace("_", " ")
                    emoji_name = emoji_name.rstrip(":")
                    active_element.send_keys(str(emoji_name))
                    time.sleep(3)
                    active_element.send_keys(Keys.ENTER)

        time.sleep(delay())
        chat_box.send_keys(Keys.ENTER)
        time.sleep(delay())
        notify = "Mesage sent to {} on {:%Y-%b-%d  %H:%M:%S} and {} remaining contacts".format(
            contact, dt.now(), Environ.cont_no - 1
        )
        log_notifier = "{} \n".format(notify)
        Environ.log_list.append(log_notifier)
        eel.notify_js(notify)
        eel.sleep(1.0)

    # for img
    time.sleep(delay())
    if imagePath and not imagePath.isspace():
        imagePathList = imagePath.split(",")
        for imageFilePath in imagePathList:
            imageFileFullPath = os.path.join(
                os.getcwd(), "volume", "images", str(imageFilePath)
            )
            try:
                attach = browser.find_element(By.CSS_SELECTOR, Environ.attach_x_path)
            except:
                print("Attach x path not found")
                return 3
            attach.click()
            time.sleep(delay())
            try:
                image_box = browser.find_element(
                    By.CSS_SELECTOR, Environ.image_box_css_selecor
                )
            except:
                print("Image Box x path not found")
                return 3
            image_box.send_keys(imageFileFullPath)
            time.sleep(delay())
            try:
                image_media_send_button = browser.find_element(
                    By.XPATH, Environ.image_media_send_x_path
                )
            except:
                print("Media Chat x path not found")
                return 3

            image_media_send_button.click()
            time.sleep(delay())
            notify = "Image sent to {} on {:%Y-%b-%d  %H:%M:%S} and {} remaining contacts".format(
                contact, dt.now(), Environ.cont_no - 1
            )
            log_notifier = "{} \n".format(notify)
            Environ.log_list.append(log_notifier)
            eel.notify_js(notify)
            eel.sleep(1.0)

    # Do for document
    time.sleep(delay())
    if documentPath and not documentPath.isspace():
        documentPathList = documentPath.split(",")
        for doc in documentPathList:
            documentFileFullPath = os.path.join(os.getcwd(), "volume", "docs", str(doc))
            try:
                attach = browser.find_element(By.CSS_SELECTOR, Environ.attach_x_path)
            except:
                print("Attach x path not found")
                return 3
            attach.click()
            time.sleep(delay())
            try:
                document_icon = browser.find_element(
                    By.CSS_SELECTOR, Environ.document_icon_x_path
                )
            except:
                print("Document Box x path not found")
                return 3
            document_icon.send_keys(documentFileFullPath)
            time.sleep(delay())
            try:
                docs_media_send_button = browser.find_element(
                    By.XPATH, Environ.docs_media_send_x_path
                )
            except:
                print("Media Chat x path not found")
                return 3

            docs_media_send_button.click()
            time.sleep(delay())
            notify = "Document sent to {} on {:%Y-%b-%d  %H:%M:%S} and {} remaining contacts".format(
                contact, dt.now(), Environ.cont_no - 1
            )
            log_notifier = "{} \n".format(notify)
            Environ.log_list.append(log_notifier)
            eel.notify_js(notify)
            eel.sleep(1.0)
        time.sleep(delay())

    Environ.cont_no -= 1
    return 1


def read_contacts_list(contactSheet):
    wb = openpyxl.load_workbook(contactSheet)
    sheet = wb.active
    contact = []
    count = 0
    for index, row in enumerate(sheet, start=1):
        a = sheet[f"A{index}"].value
        if isinstance(a, float):
            a = str(int(a))
            count += 1
        if not (not (a and not a.isspace())):
            contact.append(a)
            count += 1
    return count, contact


def get_excel_path(excel_fileName):
    project_dir_path = os.getcwd()
    file_Name = str(excel_fileName)
    return os.path.join(project_dir_path, "volume", "excel", file_Name)


def setup():
    chromedriver_autoinstaller.install()
    cService = webdriver.ChromeService()
    browser = webdriver.Chrome(service=cService)
    return browser


eel.init("web")
Environ.browser = setup()
Environ.browser.get("https://web.whatsapp.com/")
Environ.browser.maximize_window()


@eel.expose
def update(username=None):
    response = requests.get(
        f"https://keedakandi.pythonanywhere.com/api/json-store/whatsapp_automation_xpath/{username}"
    )
    if response.text == "[]":
        eel.update_msg_text("Invalid Username")
    elif response.status_code == 200:
        json_data = response.json()
        content = str(json_data[0]["xpaths"])
        with open("Environ.py", "w") as file:
            file.write(content)
        eel.update_msg_text("Updated Successfully. Please Restart the Application")
        return
    else:
        eel.update_msg_text("Update Failed. Server is down")
        return


@eel.expose
def load_whatsapp(
    contactSheetName,
    message,
    imagePath=None,
    document_path=None,
):
    Environ.contact_sheet_path = contactSheetName
    Environ.msg = message
    Environ.imgPath = imagePath
    Environ.docsPath = document_path
    time.sleep(10)

    contactSheet = get_excel_path(excel_fileName=contactSheetName)
    cont_no, contacts_list = read_contacts_list(contactSheet)
    Environ.cont_no = cont_no
    Environ.contacts_list = contacts_list
    return Environ.cont_no, Environ.contacts_list


@eel.expose
def send_msg():
    no_of_contacts = Environ.cont_no
    contacts_list = Environ.contacts_list
    browser = Environ.browser
    imagePath = Environ.imgPath
    documentPath = Environ.docsPath
    message = Environ.msg

    eel.notify_js("Message Sending Initiated")
    log_notifier = "**** AUTOMATION START **** \n"
    Environ.log_list.append(log_notifier)

    for i in range(0, Environ.cont_no):
        contact = contacts_list[i]
        time.sleep(delay())
        status = send_to(browser, contact, message, imagePath, documentPath)
        if status == 2:
            notify = (
                "{} is either blocked or doesnt exesist. {} remaining contacts".format(
                    contact, Environ.cont_no - 1
                )
            )
            log_notifier = "{} \n".format(notify)
            Environ.log_list.append(log_notifier)
            eel.notify_js(notify)
            eel.notify_fail(contact)
            Environ.cont_no -= 1
            eel.sleep(1.0)
        elif status == 3:
            notify = "Sending Failed to {}. Xpaths have been changed. {} remaining contacts".format(
                contact, Environ.cont_no - 1
            )
            log_notifier = "{} \n".format(notify)
            Environ.log_list.append(log_notifier)
            eel.notify_js(notify)
            Environ.cont_no -= 1
            eel.sleep(1.0)

    log_file = open("{}_whatsapp_log.txt".format("user"), "w")
    log_file.writelines(Environ.log_list)
    log_file.close()

    log_notifier = "****AUTOMATION COMPLETE**** \n"
    Environ.log_list.append(log_notifier)
    eel.notify_js("Automation Completed")


@eel.expose
def terminate(browser=Environ.browser):
    log_notifier = "PROGRAM TERMINATED \n"
    Environ.log_list.append(log_notifier)
    browser.close()


eel.start("main.html")
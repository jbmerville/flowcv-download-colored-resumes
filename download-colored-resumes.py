from datetime import datetime
from os import listdir, mkdir, rename
from re import search
from time import sleep

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from config import colors, dirToDownloadResumesTo, email, password, sleepTime


class FlowCVAction():
    def __init__(self):
        self.currentDate = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        self.downloadPath = "%s/%s" % (dirToDownloadResumesTo,
                                       self.currentDate)
        chrome_options = webdriver.ChromeOptions()
        prefs = {
            'download.default_directory': self.downloadPath}
        chrome_options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=chrome_options)
        self.isLoggedIn = False
        self.isOnDesignTab = False
        mkdir(self.downloadPath)
        print("✅ Successfully created \"%s\" folder in \"%s\"" %
              (self.currentDate, dirToDownloadResumesTo))

    def executeSteps(self, name, steps):
        try:
            for step in steps:
                element = self.driver.find_element_by_xpath(step["xPath"])
                if step["action"] == "send_keys":
                    element.send_keys(step["action_payload"])
                if step["action"] == "click":
                    element.click()
                if step["sleepTime"]:
                    sleep(step["sleepTime"])
            print("✅ Successfully executed \"%s\"" % name)
        except Exception as exception:
            raise Exception("❌ %s failed with error:\n%s" %
                            (name.capitalize(), exception))

    def login(self):
        steps = [
            {
                "name": "email_input",
                "xPath": "/html/body/div/div[2]/div/div[4]/div/div/div/div/div/div[1]/input",
                "action": "send_keys",
                "action_payload": email,
                "sleepTime": 1
            },
            {
                "name": "next_button",
                "xPath": "/html/body/div/div[2]/div/div[4]/div/div/div/div/div/div[2]/button",
                "action": "click",
                "sleepTime": sleepTime or 2
            },
            {
                "name": "password_input",
                "xPath": "/html/body/div/div[2]/div/div[4]/div/div/div/div/div[2]/div[1]/div/input",
                "action": "send_keys",
                "action_payload": password,
                "sleepTime": 1
            },
            {
                "name": "loggin_button",
                "xPath": "/html/body/div/div[2]/div/div[4]/div/div/div/div/div[2]/div[2]/button",
                "action": "click",
                "sleepTime": sleepTime or 2
            },
        ]
        self.driver.get("https://flowcv.io/login")
        sleep(1)
        self.executeSteps("login", steps)
        self.isLoggedIn = True

    def navigateToDesignTab(self):
        if not self.isLoggedIn:
            raise Exception(
                "❌ User not logged in. Please Please execute \"login\" before executing \"navigateToDesignTab\"")
        steps = [
            {
                "name": "design_tab_link",
                "xPath": "/html/body/div[1]/div[2]/div/div[1]/div/nav/div[1]/a[2]",
                "action": "click",
                "sleepTime": 1
            }
        ]
        self.executeSteps("navigate to Design tab", steps)
        self.isOnDesignTab = True

    def downloadColoredResumes(self):
        if not self.isOnDesignTab:
            raise Exception(
                "❌ User not on Design tab. Please execute \"navigateToDesignTab\" before executing \"downloadColoredResumes\"")
        colorsXPath = {}
        colorsOrder = ["black", "red", "wine", "grape", "purple", "ocean", "blue", "sky", "cyan", "swamp",
                       "green", "grass", "vomit", "yellow", "sun", "orange", "red", "brown", "gray", "metal"]
        for index, color in enumerate(colorsOrder):
            colorsXPath[color] = "/html/body/div[1]/div[2]/div/div[2]/div/div[1]/div[3]/div[11]/div/div[2]/div[2]/div/label[%d]" % (
                index + 1)

        for color in colors:
            if color not in colorsXPath:
                raise Exception("❌ Invalid color \"%s\", please use only the following colors in your \"config.py\": %s" % (
                    color, colorsOrder))
            xPath = colorsXPath[color]
            steps = [
                {
                    "name": "choose_resume_color_%s" % color,
                    "xPath": xPath,
                    "action": "click",
                    "sleepTime": sleepTime or 2
                },
                {
                    "name": "download_button",
                    "xPath": "/html/body/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/button",
                    "action": "click",
                    "sleepTime": sleepTime or 5
                },
            ]

            self.executeSteps("download %s resume" % color, steps)
            self.moveResumeInsideFolder(color)
            self.driver.get("https://flowcv.io/app/resume/customization")
            sleep(1)

    def moveResumeInsideFolder(self, color, renameFileWithoutDate=True):
        fileNames = listdir(self.downloadPath)
        pdfFileCount = 0
        pdfFile = None
        for fileName in fileNames:
            if ".pdf" in fileName:
                pdfFileCount += 1
                pdfFile = fileName
        if pdfFile == None or pdfFileCount != 1:
            raise Exception(
                "❌ Excpected 1 \".pdf\" file in directory \"%s\" but found %d. Please execute moveResumeInsideFolder with maximum one \".pdf\" file in directory." % (self.downloadPath, pdfFileCount))
        if renameFileWithoutDate:
            firstNumber = search("\d", pdfFile).start()
            oldPathToPdfFile = "%s/%s" % (self.downloadPath, pdfFile)
            newPathToColorFolder = "%s/%s" % (self.downloadPath,
                                              color.capitalize())
            mkdir(newPathToColorFolder)
            newPathToPdfFile = "%s/%s.pdf" % (newPathToColorFolder,
                                              pdfFile[:firstNumber - 1])
            rename(oldPathToPdfFile, newPathToPdfFile)


if __name__ == "__main__":
    try:
        flow = FlowCVAction()
        flow.login()
        flow.navigateToDesignTab()
        flow.downloadColoredResumes()
        print("✅ Flow-CV downloads succeeded!")
    except Exception as error:
        print("❌ Flow-CV downloads failed with error:\n%s" % error)

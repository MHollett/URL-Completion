from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import json

# Delay between webpage switches (in seconds)
DELAY = 0.1


def main():
    # Read json
    URLfile = open("URLS.json", "r")
    URLS = URLfile.read()
    URLSdict = json.loads(URLS)

    # This is here so I can do a few different urls at once. Not sure if I'll need this, but I have to parse it somehow
    outputURLs = []
    for index, url in enumerate(URLSdict.keys()):
        testURL = url
        instructions = URLSdict[url]
        outputURLs.append([])

        parseUrlInstructions(url, instructions, outputURLs[-1])

        # Prompt user for if they want to see the URL list
        printList = input(
            "Generated list of URLs "
            + str(len(outputURLs[-1]))
            + " elements long. Press any key to print the list. "
        )
        if len(printList) > 0:
            print(outputURLs)

        webscrapeList(outputURLs[-1])


def parseUrlInstructions(baseStr, instrArray, outputArray):
    depth = len(instrArray)

    # Special case: array is empty
    if depth == 0:
        print("Error: Empty array")
        return

    # Special Loop case: index 0 is "count", in which case, count from number in index 1 to number in index 2
    if instrArray[0][0] == "count":
        for strFragment in range(instrArray[0][1], instrArray[0][2] + 1):
            tempStr = baseStr + str(strFragment)
            if depth == 1:
                outputArray.append(tempStr)
            else:
                newInstrArray = instrArray[1:]
                parseUrlInstructions(tempStr, newInstrArray, outputArray)

    # Standard Loop through first array in the array of arrays
    else:
        for strFragment in instrArray[0]:
            tempStr = baseStr + str(strFragment)
            if depth == 1:
                outputArray.append(tempStr)
            else:
                newInstrArray = instrArray[1:]
                parseUrlInstructions(tempStr, newInstrArray, outputArray)

    return


def webscrapeList(URLs):
    driver = webdriver.Chrome()

    for URL in URLs:
        driver.get(URL)
        sleep(DELAY)


if __name__ == "__main__":
    main()

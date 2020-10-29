# Howdy flowcv.io users!

This python script solves a niche problem I encountered... It automates downloading many-colored versions of your FlowCV resume. Script working as of October 29th, 2020.

## What is the use case for this script?

Applying for jobs often has better results when your resume is tailored for a specific company or job posting. One easy way to do this is by having different color variations of your resume! This tool automates the boring task of downloading colored resumes anytime you modify your FlowCV resume!

## How does the script work?

This script uses Selenium to control a Chromium browser without any user input! This scripts logs into your FlowCV account and downloads versions of your resume with different accent colors to your desired directory.

## What colors can I pick from?

As of October, 29th, 2020, this script works with any of the default colors:
![](flowcv-colors.png)

## The script keeps giving me an error, what's happening?

If you see errors similar to this error message: `"Message: no such element: Unable to locate element: {...}"`. This is most likely due to the script running faster than the page/requests. Try running the script again or you can increase the sleep time in between each action through the config file.

## How to set up the script?

1. Install python dependencies:

```
pip3 install selenium webdriver_manager
```

2. Download the chromium-browser at https://www.chromium.org/getting-involved/download-chromium
3. Complete config file with your username, password, desired colors, and the path to your download directory.
4. Run the script!

```
python3 flow-cv/download-colored-resumes
```

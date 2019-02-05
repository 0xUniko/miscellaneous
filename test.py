#%%
import requests, re, time
from selenium import webdriver
from PIL import Image
from io import BytesIO


#%%
s = webdriver.Edge(r'C:\Users\micro\Downloads\MicrosoftWebDriver.exe')

#%%
s.get('https://www.weibo.com')

#%%

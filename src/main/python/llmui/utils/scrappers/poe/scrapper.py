import json
import os
import typing

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time

from llmui.llm import LLM


class PoeScrapper:

	__POE_URL = "https://poe.com/"

	def __init__(self, cookies_path: typing.Optional[str] = None):
		self.driver = self._configure_driver()
		if cookies_path is not None:
			self.load_cookies(cookies_path)
		self.__current_bot: str = None

	def _configure_driver(self):
		options = webdriver.FirefoxOptions()
		options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
		options.add_argument("--headless")
		return webdriver.Firefox(options=options)

	def load_cookies(self, path):
		self.driver.get(self.__POE_URL)
		with open(path, 'r') as file:
			cookies = json.load(file)
			for cookie in cookies:
				self.driver.add_cookie(cookie)

	def _scroll_down(self):
		self.driver.execute_script("window.scrollTo(0, window.innerHeight);")

	def choose_bot(self, bot: str):
		self.driver.get(os.path.join(self.__POE_URL, bot))
		self.__current_bot = bot

	def send_message(self, message: str):
		if self.__current_bot is None:
			raise Exception("Bot not selected")
		chat_input = WebDriverWait(self.driver, 20).until(
			EC.element_to_be_clickable((By.XPATH,  f"//input[contains(@placeholder,'Talk to {self.__current_bot.capitalize()} on Poe')]"))
		)
		chat_input.send_keys(message)
		chat_input.send_keys(Keys.RETURN)

	def get_recent_response(self) -> str:
		element = self.driver.find_elements(By.CLASS_NAME, "ChatMessage_chatMessage__BmN0M")[-1]
		return element.text

	def chat(self, message: str) -> str:
		self.send_message(message)
		time.sleep(20)
		return self.get_recent_response()
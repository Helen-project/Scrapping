"""Base car object module."""
import datetime
import re

import pandas as pd


class Car:
    """Car class object."""

    def __init__(self):
        """Functions initialise the class."""
        self.url: str = ""
        self.title: str = ""
        self.price_usd: int = 0
        self.odometer: int = 0
        self.user_name: str = ""
        self.phone_number: int = 0
        self.image_url: str = ""
        self.images_count: int = 0
        self.car_number: str = ""
        self.car_vin: str = ""
        self.datetime_found = datetime.datetime.now()

    def check_and_convert_odometer(self, odometer):
        """Function for checking and convert odometer value.

        Args:
            odometer: Odometer value.
        """
        matched = re.match("^[0-9]+", odometer)
        if matched:
            self.odometer = int(f"{matched[0]}000")
        else:
            self.odometer = 0

    def check_phone_number(self, phone_number: str):
        """Function for checking phone number value.

        Args:
            phone_number: Phone number value.
        """
        matched = re.search("[0-9]+", phone_number)
        if matched:
            if matched[0].startswith("380") and len(matched[0]) == 12:
                self.phone_number = int(matched[0])

    def get_image_count(self, image_count: str):
        """Function for getting image count from string value.

        Args:
            image_count: String data with image value .
        """
        matched = re.match("^[0-9]+", image_count)
        if matched:
            self.images_count = int(matched[0])
        else:
            self.images_count = 0

    def currency_check(self, first_currency: str):
        """Function for check currency.

        Args:
            first_currency: String first_currency value .
        """
        if "$" in str(first_currency):
            self.price_usd = str(first_currency).replace("$", "").replace(" ", "")
        elif "€" in str(first_currency):
            self.price_usd = str(first_currency).replace("€", "").replace(" ", "")
        elif "грн" in str(first_currency):
            self.price_usd = str(first_currency).replace("грн", "").replace(" ", "")
        else:
            self.price_usd = first_currency.replace(" ", "")

    def convert_to_db(self):
        """Convert data class to data frame."""
        return pd.DataFrame(self.__dict__)

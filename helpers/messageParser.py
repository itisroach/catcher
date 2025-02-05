import re
from .tools import convert_numbers, extract_details



def parse_message(message: str):
      PRICE_REGEX = r"^.*\b(?![0+-])\d{5,}\b.*$"
      # some channels use this character for more beautiful texts like this: تـــومان so this line converts it to تومان 
      message = message.replace("ـ", "")
      
      # converting Farsi or Arabic numbers to English numbers
      cleaned_message = convert_numbers(message)

      matches = re.findall(PRICE_REGEX, cleaned_message, re.MULTILINE)

      # converting prices from Rial to Toman
      result = convert_currencies_to_toman(matches)
      return result




def convert_currencies_to_toman(matches):
      values = []

      for m in matches:
            # extracting details and price with currency from matches 
            details, m = extract_details(m)
            # a regex for detecting currencies 
            currencyReg = r"(?:تومان|ریال|Toman|Rials|Price|قیمت|تومن|\$|buy|sell|خرید|فروش|IRR|IRT)|(?<=\d)\$"
            # extracting the currency from text 
            currency = re.findall(currencyReg, m, re.IGNORECASE)
            # a regex for detecting numbers
            # regNum   = r"\b(?:\d{1,3}(?:[,.]\d{3})*|\d+)\b"
            # extracting the number
            
            number   = re.findall(r"\b(?![0+-])\d{5,}\b", m)
           
            if not number:
                  continue 
            
            # removing any commas and dots in numbers 13,000 => 13000
         
            number   = number[0].replace(".", "")

            number   = int(number.replace(",", ""))

            # checking if numbers has a coefficient like (هزار، میلیون، میلیارد)
            number = result_with_coefficient(m, number)
            
            # checking if a currency were detected and if they are rial based convert them to toman
            if currency and currency[0].lower() in ["ریال", "rial", "rials", "irr"]:
                  number /= 10
      
            # storing a dict for better accessing
            result = {
                  "price": number,
                  "details": details
            }

            values.append(result)

      return values         


def result_with_coefficient(text, number):
      # a regex for detecting the coefficient
      coeffRegex =  r"(?:هزار|میلیارد|میلیون|صد|ده)"
      # extracting them
      coeff = re.findall(coeffRegex, text)

      # if coefficients are more than 1 like this => هزار میلیارد تومان
      if len(coeff) > 1:
            for i in coeff:
                  number = result_with_coefficient(i, number)
                  coeff.remove(i)

      if coeff:
            match coeff[0]:
                  case "هزار":
                        number *= 1000
                  case "میلیون":
                        number *= 1_000_000
                  case "میلیارد":
                        number *= 1_000_000_000
                  case "صد":
                        number *= 100
                  case "ده":
                        number *= 10
      return number
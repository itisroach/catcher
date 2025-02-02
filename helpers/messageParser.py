import re


def parse_message(message: str):
      reg = r"\b(?:\d{1,3}(?:,\d{3})*|\d+|[\u06F0-\u06F9]+)\s*(?:تومان|ریال|Toman|Rials|Price|قیمت|تومن|\$|buy|sell|خرید|فروش|IRR|IRT|میلیون تومان|میلیون ریال|هزار تومان|هزار ریال)|" \
            r"(?:تومان|ریال|Toman|Rials|Price|قیمت|تومن|\$|buy|sell|خرید|فروش|IRR|IRT|میلیون تومان|میلیون ریال|هزار تومان|هزار ریال)\s*(?:\d{1,3}(?:,\d{3})*|\d+|[\u06F0-\u06F9]+)\b"


      matches = re.findall(reg, message, re.IGNORECASE)

      
      result = convert_currencies_to_toman(matches)

      return result




def convert_currencies_to_toman(matches):
      values = []
      for m in matches:
            # a regex for detecting currencies 
            currencyReg = r"(?:تومان|ریال|Toman|Rials|Price|قیمت|تومن|\$|buy|sell|خرید|فروش|IRR|IRT)|(?<=\d)\$"
            # extracting the currency from text 
            currency = re.findall(currencyReg, m, re.IGNORECASE)
            # a regex for detecting numbers
            regNum   = r"\b(?:\d{1,3}(?:,\d{3})*|\d+|[\u06F0-\u06F9]+)\b"
            # extracting the number
            number   = re.findall(regNum, m)
            # removing any comma in numbers 13,000 => 13000
            number   = int(number[0].replace(",", ""))
            
            # checking if numbers has a coefficient like (هزار، میلیون، میلیارد)
            number = result_with_coefficient(m, number)

            # checking if a currency were detected and if they are rial based convert them to toman
            if currency and currency[0].lower() in ["ریال", "rial", "rials", "irr"]:
                  number /= 10

            values.append(number)

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
      print(number)
      return number
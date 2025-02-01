import re


def parse_message(message: str):
      reg = r"(?:\d{1,3}(?:,\d{3})*|\d+|[\u06F0-\u06F9]+)\s*(?:تومان|ریال|Toman|Rials|Price|قیمت|تومن|\$|buy|sell|خرید|فروش|IRR|IRT)|" \
          r"(?:تومان|ریال|Toman|Rials|Price|قیمت|تومن|\$|buy|sell|خرید|فروش|IRR|IRT)\s*(?:\d{1,3}(?:,\d{3})*|\d+|[\u06F0-\u06F9]+)"


      matches = re.findall(reg, message, re.IGNORECASE)

      
      result = convert_currencies_to_toman(matches)

      return result




def convert_currencies_to_toman(matches):
      for m in matches:
            reg = r"(?:تومان|ریال|Toman|Rials|Price|قیمت|تومن|\$|buy|sell|خرید|فروش|IRR|IRT)|(?<=\d)\$"
            currency = re.findall(reg, m, re.IGNORECASE)
            print(m)
            regNum   = r"\d+"
            number   = re.findall(regNum, m)
            number   = int(number[0])

            if currency[0].lower() in ["ریال", "rial", "rials", "irr"]:
                  number /= 10
            
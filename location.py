import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import time

def start_phonenumber_tracer(target):
    print(f"[+] Phonetracer v2.1-OSINT")
    print(f"[*] Target : {target}")
    print(f"[*] initiating trace....")
    time.sleep(1)  # simulate processing

    try:
        if not target.startswith('+'):
            if len(target) == 10:
                target = '+91' + target
            else:
                target = '+' + target
        # parse phone number
        parse = phonenumbers.parse(target)

        # basic validation
        valid = phonenumbers.is_valid_number(parse)
        possible = phonenumbers.is_possible_number(parse)
        print(f"\n[+] Basic information : ")
        print(f"- Valid Number : {'Yes' if valid else 'No'} ")
        print(f"- Possible Number : {'Yes' if possible else 'No'}")

        # Location detail
        location = geocoder.description_for_number(parse, "en")  # added language parameter
        print(f"\n[+] Geographic Details : ")
        if location and location.strip().lower() not in ["india", "unknown"]:
            print(f"- Location : {location}")
        else:
            print(f"- Precise city/state information is not available for most mobile numbers due to privacy and data limitations.")
            print(f"- Country : {location if location else 'Unknown'}")

        # carrier information
        try:
            service_provider = carrier.name_for_number(parse, "en")
            if target.startswith('+91'):
                service_provider = carrier.name_for_number(parse, "en") or "Indian Telecom Provider"
            print(f"- Carrier/Service-provider : {service_provider}")
        except Exception:
            print("- Carrier : could not determine")

        # timezone
        time_zone = timezone.time_zones_for_number(parse)
        print(f"- Timezone : {', '.join(time_zone) if time_zone else 'Unknown'}")

        # Number type (landline/mobile/etc)
        number_type = phonenumbers.number_type(parse)
        type_map = {
            0: "Fixed Line",
            1: "Mobile",
            2: "Fixed/Mobile",
            3: "Toll Free",
            4: "Premium Rate",
            5: "Shared Cost",
            6: "VOIP",
            7: "Pager",
            8: "UAN",
            9: "Unknown"
        }
        print(f"- Number Type : {type_map.get(number_type, 'Unknown')}")

        # additional validation
        if valid:
            print(f"\n[+] Additional checks : ")
            print(f"- Possible number : {'Yes' if phonenumbers.is_possible_number(parse) else 'No'}")
            print(f"- Format (National) : {phonenumbers.format_number(parse, phonenumbers.PhoneNumberFormat.NATIONAL)}")
            print(f"- Format (International) : {phonenumbers.format_number(parse, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")

    except phonenumbers.phonenumberutil.NumberParseException as e:
        print(f"[-] Error : {e}")
    except Exception as e:
        print(f"[-] Unexpected Error : {e}")
    print(f"[+] Trace complete")

def main():
    print("\n----- PHONE NUMBER TRACER -----")
    phone = input("Enter the 10-digit phone number: ").strip()
    start_phonenumber_tracer(phone)

if __name__ == "__main__":
    main()
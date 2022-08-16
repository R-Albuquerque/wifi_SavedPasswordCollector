# wifi_SavedPasswordCollector

Python script to extract saved Wi-Fi passwords from a windows host.

## How it works

it uses ´netsh wlan show´ command to fetch all the ssid's saved on the system.

Then, it runs netsh wlan show profile "{ssid}" key=clear´ on each of the fetched ssid's to extract data from which cipher mode and key information is parsed.
After parsing and printing the information, it gives the option to save the results on a csv file.

No dependencies were used so the script may be saved to a USB drive and executed on any windows machine that has Python installed.

## Languages

This was written and tested on Windows systems with English and Portuguese as the System Language, so it may not run as expected if the target is set to another language. It is, however, easy to adapt to other languages. All you have to do is change the regex on lines 28 and 30 to your preferred language and you are probably good to go.

#### Disclaimer
This is solely for demonstration and educational purposes. What you do with this script is your own responsibility.
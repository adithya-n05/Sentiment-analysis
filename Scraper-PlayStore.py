import argparse
import google_play_scraper
import fpdf
import pandas as pd
import pdfkit

parser = argparse.ArgumentParser(description="Embeddings creation tool",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-c", "--country", type=str, help="Which country to access for play store. The last 2 characters of play store URL with country code.")
parser.add_argument("-n", "--name", help="App name")
args = parser.parse_args()
config = vars(args)
print("Input received: \n" + str(config))

AppCountry = config["country"]
AppName = config["name"]

def Scraper(AppCountry, AppName):
    
    pdf = fpdf.FPDF(format='letter')
    pdf.add_page()
    pdf.set_font("Arial", "",  size=4)

    print("Established connection to play store")
    print("Scraping app " + "\"" + AppName + "\"")

    axis_bank = google_play_scraper.reviews_all(AppName, country=AppCountry, lang="en", sleep_milliseconds=0)

    print(axis_bank)

    dataframepd = pd.json_normalize(axis_bank)
    dataframepd["at"] = dataframepd["at"].astype(str)

    print("Storing to pandas data frame:")
    print(dataframepd)
    print("Saving to disk...")

    html_table = dataframepd.to_html()

    options = {    'page-size': 'Letter',
    'margin-top': '0mm',
    'margin-right': '0mm',
    'margin-bottom': '0mm',
    'margin-left': '0mm'
    }

    pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    pdfkit.from_string(html_table, 'outputs.pdf', options=options)

    print("Successfully saved to disk!")

Scraper(AppCountry, AppName)
import argparse
import app_store_scraper
import fpdf
from datetime import datetime

parser = argparse.ArgumentParser(description="Embeddings creation tool",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-c", "--country", type=str, help="Which country to access for play store. The last 2 characters of play store URL with country code.")
parser.add_argument("-n", "--name", help="App name")
parser.add_argument("-i", "--AppID", help="The ID of the app you are attempting to scrape")
args = parser.parse_args()
config = vars(args)
print("Input received: \n" + str(config))

AppCountry = config["country"]
AppName = config["name"]
AppID = config["AppID"]

def Scraper(AppCountry, AppName, AppID):

    pdf = fpdf.FPDF(format='letter')
    pdf.add_page()
    pdf.set_font("Arial", "",  size=10)

    print("Established connection to play store")
    print("Scraping app " + "\"" + AppName + "\"")

    axis_bank = app_store_scraper.AppStore(country=AppCountry, app_name=AppName, app_id=AppID)   # Axis Mobile

    axis_bank.review(how_many=1000000)    # 20000 reviews

    print(axis_bank.reviews)

    print("Saving to disk")

    for i in range(len(axis_bank.reviews)):
        text = "User Name - " + str(axis_bank.reviews[i]['userName']) + ":"
        review = text.encode('latin-1', 'replace').decode('latin-1')
        pdf.write(12, review) 
        pdf.ln()
        text = "Date and time - " + datetime.strftime(axis_bank.reviews[i]['date'], "%d/%m/%Y %H:%M:%S") + ":"
        review = text.encode('latin-1', 'replace').decode('latin-1')
        pdf.write(12, review) 
        pdf.ln()
        text = "Review - " + str(axis_bank.reviews[i]['review']) + ":"
        review = text.encode('latin-1', 'replace').decode('latin-1')
        pdf.write(12, review)
        pdf.ln()

    pdf.output("Comments-" + "app_store-" + AppName + ".pdf")

    print("Successfully saved to disk!")

Scraper(AppCountry, AppName, AppID)
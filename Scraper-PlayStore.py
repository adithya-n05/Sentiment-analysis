import argparse
import google_play_scraper
import fpdf
from datetime import datetime
import pandas as pd

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
    pdf.set_font("Arial", "",  size=10)

    print("Established connection to play store")
    print("Scraping app " + "\"" + AppName + "\"")

    axis_bank = google_play_scraper.reviews_all(AppName, country=AppCountry, lang="en", sleep_milliseconds=0)

    print(axis_bank)

    dataframepd = pd.json_normalize(axis_bank)
    dataframepd["at"] = dataframepd["at"].astype(str)

    print("Storing to pandas data frame:")
    print(dataframepd)
    print("Saving to disk")

    for i in range(len(dataframepd[dataframepd.columns[0]].values.tolist())):
        text = str(dataframepd[dataframepd.columns[1]].values.tolist()[i]) + ":"
        review = text.encode('latin-1', 'replace').decode('latin-1')
        pdf.write(12, review) 
        pdf.ln()
        text = "Score - " + str(dataframepd[dataframepd.columns[4]].values.tolist()[i]) + ":"
        review = text.encode('latin-1', 'replace').decode('latin-1')
        pdf.write(12, review) 
        pdf.ln()
        text = "Date and time - " + dataframepd[dataframepd.columns[7]].values.tolist()[i] + ":"
        review = text.encode('latin-1', 'replace').decode('latin-1')
        pdf.write(12, review) 
        pdf.ln()
        text = str(dataframepd[dataframepd.columns[3]].values.tolist()[i]) + ":"
        review = text.encode('latin-1', 'replace').decode('latin-1')
        pdf.write(12, review)
        pdf.ln()


    pdf.output("Comments-" + "play_store-" + AppName + ".pdf")
    print("Successfully saved to disk!")

Scraper(AppCountry, AppName)
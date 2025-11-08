#!/usr/bin/env python

import glob
import pdfplumber
import re
import shutil
import sys
import os
import time
from datetime import datetime
import imaplib
import email
import os
from bs4 import BeautifulSoup
import urllib.request
import requests

print("Bryans PDF sorter Ver.: 1.8.0")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("I grab Sixt invoices and SEPA prenotifications, ShareNow invoices and SEPA prenotifications, FlixBus invoices and tickets from my gmail account. Future releases will also grab DB tickets and a lot more.")
print("I also find the date, invoice or order number and travel destinations on each item and sort everything nicely labeled into my filing cabinet.")
print("It is a time saver for an organized filing system.")



# Connect to the IMAP server
imap_server = imaplib.IMAP4_SSL("imap.gmail.com")

# Login to your account
imap_server.login("bryan.barcelona@gmail.com", "ctvdxpnigaijbuip")

# Select the inbox folder
imap_server.select("inbox")

######################################################################################
# Deleting irrelevant emails from the services used such as PayPal notification etc. #
######################################################################################

# Open a master email ID list for Emails targeted for deletion
email_ids = []

# Search for emails from service@paypal.de with "Bolt Operations" in the subject line
result, data = imap_server.search(None, '(FROM "service@paypal.de" SUBJECT "Bolt Operations")')
# Split the result into a list of email IDs and append to master list
email_id_current_search = data[0].split()
for i in email_id_current_search:
    email_ids.append(i)

# Search for emails from service@paypal.de with "EasyPark GmbH" in the subject line
result, data = imap_server.search(None, '(FROM "service@paypal.de" SUBJECT "EasyPark GmbH")')
# Split the result into a list of email IDs and append to master list
email_id_current_search = data[0].split()
for i in email_id_current_search:
    email_ids.append(i)

# Iterate over the email IDs
for email_id in email_ids:
    imap_server.store(email_id, '+X-GM-LABELS', '\\Trash')

####################################################
# Getting PDFs and deleting the emails starts here #
####################################################

senders = ['donotreply@sixt.com', 'postbote@myafterpay.com', 'hallo@share-now.com', 
           'noreply@booking.flixbus.com', 'noreply@flixbus.com', 'no-reply@easypark.net', 'noreply@stadtradhamburg.de']

# Search for emails from the specified senders
for sender in senders:
    result, data = imap_server.search(None, f'FROM "{sender}"')
    
    # Split the result into a list of email IDs
    email_ids = data[0].split()
    
    # Iterate over the email IDs
    for email_id in email_ids:
        result, data = imap_server.fetch(email_id, "(RFC822)")
        
        # Parse the email using the email library
        email_message = email.message_from_bytes(data[0][1])
        
        # Iterate over the attachments in the email and download only ATTACHED pdfs
        for part in email_message.walk():
            # Check if the part is an attachment
            if part.get_content_maintype() == "application" and part.get_content_subtype() == "pdf":
                # Get the filename of the attachment
                filename = part.get_filename()
                
                # Save the attachment to disk
                with open(os.path.join("C:\\Users\\Bryan Barcelona\\Downloads", filename), "wb") as f:
                    f.write(part.get_payload(decode=True))

        #go into specific email and pull the pdf link and then download it
        if sender == 'no-reply@easypark.net':
                # extract links from the email body
                if email_message.is_multipart():
                    for part in email_message.walk():
                        if part.get_content_type() == 'text/html':
                            soup = BeautifulSoup(part.get_payload(decode=True), 'html.parser')
                            links = soup.find_all('a')
                            
                            # URL of the PDF file to download
                            url = links[0].get('href')
                            
                            # Send a request to download the PDF file
                            response = requests.get(url)

                            # Check if the request was successful
                            if response.status_code == 200:
                                # Define the path to the downloads folder
                                download_folder = os.path.expanduser("~") + "/Downloads/"
                                
                                # Create the downloads folder if it doesn't exist
                                if not os.path.exists(download_folder):
                                    os.makedirs(download_folder)
                                
                                # Extract the filename from the URL
                                filename = url.split("/")[-3]
                                
                                # Save the PDF file to the downloads folder
                                with open(download_folder + filename +".pdf", 'wb') as f:
                                    f.write(response.content)
        
        # Move the email to the trash
        imap_server.store(email_id, '+X-GM-LABELS', '\\Trash')
        
# Close and log out of the IMAP connection
imap_server.close()
imap_server.logout()

###########################
# PDF sorting starts here #
###########################

def shuttle_service(from_where, to_where, doc_type):
    add_to_log = f"\n[{datetime.now()}]\tMoved and renamed {from_where} to {to_where} ({doc_type})."
    if from_where != to_where:
        print(add_to_log)
    else:
        print(f"\n[{datetime.now()}]\tThis is a not a pdf for the filing cabinet or hasn't been included in the automatic sorting process.")
    shutil.move(from_where, to_where)

def dateshift(grabbed_year, grabbed_month, grabbed_day, language: str):
    if language not in ['eng', 'deu', 'eng_long', 'deu_long']:
        raise ValueError('Language must be either "eng", "eng_long" or "deu"')
    else:
        pass

    if language == "eng":
        month_dict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    elif language == "deu":
        month_dict = {'Jan': '01', 'Feb': '02', 'Mär': '03', 'Apr': '04', 'Mai': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Okt': '10', 'Nov': '11', 'Dez': '12'}
    elif language == "eng_long":
        month_dict = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'}
    elif language == "deu_long":
        month_dict = {'Januar': '01', 'Februar': '02', 'März': '03', 'April': '04', 'Mai': '05', 'Juni': '06', 'Juli': '07', 'August': '08', 'September': '09', 'Oktober': '10', 'November': '11', 'Dezember': '12'}
    day = grabbed_day
    day = grabbed_day
    month_alphabetic = grabbed_month
    month_numerical = month_dict.get(month_alphabetic)
    year = grabbed_year
    new_filename = year + month_numerical + day
    return new_filename

pdf_list = glob.glob('C:\\Users\\Bryan Barcelona\\Downloads\\*.pdf')

doc_type = []
date = []
invoice_no = []
start_dest = []
split_date = []
year = ""
month = ""
day = ""

for i in range(len(pdf_list)):

    print(pdf_list[i])
    with pdfplumber.open(pdf_list[i]) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()

    doc_type.append("")
    date.append("")
    invoice_no.append("")
    start_dest.append("")

    lines = text.split("\n")
    con_lines = ' '.join(lines)

    #for line in lines:
    #    print(line)

    # checking and assigning the pdf category

    if "Sixt GmbH & Co. Autovermietung KG" in con_lines and "Rechn. Nr.:" in con_lines:
        doc_type[i] = "Invoice Sixt"
    elif "Riverty GmbH" in con_lines and "Postfach 5705" in con_lines and "ZAHLUNGSHINWEIS" in con_lines:
        doc_type[i] = "SEPA Sixt"
    elif "SHARE NOW GmbH" in con_lines and "SHARE NOW Fahrt" in con_lines:
        doc_type[i] = "Invoice ShareNow"
    elif "SHARE NOW GmbH" in con_lines and "SEPA Prenotification" in con_lines:
        doc_type[i] = "SEPA ShareNow"
    elif "Techem Energy Services GmbH" in con_lines:
        doc_type[i] = "Techem"
    elif "congstar Kundenservice" in con_lines:
        doc_type[i] = "Invoice Congstar"
    elif "Bolt Operations" in con_lines and "Tallinn" in con_lines:
        doc_type[i] = "Bolt Invoice"
    elif "Gesellschaft Gothaer Allgemeine Versicherung" in con_lines:
        doc_type[i] = "Gothaer"
    elif "Flix SE" in con_lines and "Rechnungen für Deine Buchung" in con_lines:
        doc_type[i] = "Invoice FlixBus"
    elif "Flix SE" in con_lines and "BORDKARTE" in con_lines:
        doc_type[i] = "Ticket FlixBus"
    elif "DB Fernverkehr AG" in con_lines and "Online-Ticket" in con_lines:
        doc_type[i] = "DB Ticket"
    elif "EasyPark GmbH" in con_lines and "Rechnung" in con_lines:
        doc_type[i] = "EasyPark"
    elif "Landesbetrieb Verkehr" in con_lines and "Besucherparkausweis" in con_lines:
        doc_type[i] = "Besucherparken"
    elif "Social Security Statement" in con_lines and "BRYAN BARCELONA" in con_lines:
        doc_type[i] = "Social Security"
    elif "Hamburger Sparkasse" in con_lines and "823351" in con_lines and "Kontoauszug" in con_lines:
        doc_type[i] = "Haspa Kontoauszug"
    elif "Mastercard" in con_lines and "Hamburger Sparkasse" in con_lines:
        doc_type[i] = "Kreditkarte"
    elif "Sollzinssatz" in con_lines and "KfW" in con_lines:
        doc_type[i] = "KfW Zinssatz"
    elif "Lastschriftankündigung" in con_lines and "KfW-Bankengruppe" in con_lines:
        doc_type[i] = "KfW Lastschrift"
    elif "Kontoauszug" in con_lines and "18838652" in con_lines and "KfW" in con_lines and "Jahreskontoauszug" not in con_lines:
        doc_type[i] = "KfW Kontoauszug"
    elif "Kontoauszug" in con_lines and "18838652" in con_lines and "KfW" in con_lines and "Jahreskontoauszug" in con_lines:
        doc_type[i] = "KfW Jahreskontoauszug"
    elif "Jahreszinsbescheinigung" in con_lines and "KfW" in con_lines:
        doc_type[i] = "KfW Jahreszinsbescheinigung"
    elif "AOK Rheinland/Hamburg" in con_lines and "Datenübermittlung an die Finanzverwaltung" in con_lines:
        doc_type[i] = "AOK Finanzamt"
    elif "1&1 Telecom GmbH" in con_lines and "539200683" in con_lines:
        doc_type[i] = "1&1 Invoice"
    elif "StadtRAD Hamburg" in con_lines and "Mainzer Landstraße" in con_lines:
        doc_type[i] = "StadtRAD"
    else:
        doc_type[i] = "None"


    # checking and assigning the date
    if doc_type[i] == "SEPA Sixt": #if date is in the line after "Bestellnummer"
        for j, line in enumerate(lines):
            if "Bestellnummer" in line:
                year = lines[j+1].split(" ")[1].split(".")[2]
                month = lines[j+1].split(" ")[1].split(".")[1]
                day = lines[j+1].split(" ")[1].split(".")[0]
                date[i] = f"{year}{month}{day}"
                break
    elif doc_type[i] == "Invoice Sixt":
        for j, line in enumerate(lines): #if date is in the line after "Bestellnummer"
            if "Pullach," in line:
                year = lines[j].split("Pullach, ")[1].split(".")[2]
                month = lines[j].split("Pullach, ")[1].split(".")[1]
                day = lines[j].split("Pullach, ")[1].split(".")[0]
                date[i] = f"{year}{month}{day}"
                break
    elif doc_type[i] == "Invoice ShareNow":
        for j, line in enumerate(lines): #if date is in the line after "Bestellnummer"
            if "Rechnungsdatum:" in line:
                year = lines[j].split(":")[1].split(".")[2]
                month = lines[j].split(":")[1].split(".")[1]
                day = lines[j].split(":")[1].split(".")[0]
                date[i] = f"{year}{month}{day}"
                break
    elif doc_type[i] == "SEPA ShareNow":
        for j, line in enumerate(lines): #if date is in the line after "Bestellnummer"
            if "Document Date" in line:
                split_date = lines[j+1].split(" ")        
                day = str(split_date[1].split(',')[0]).zfill(2)
                month = split_date[0]
                year = split_date[2]
                date[i] = dateshift(year, month, day, "eng")
                break
    elif doc_type[i] == "Invoice Congstar" or doc_type[i] == "Gothaer" or doc_type[i] == "1&1 Invoice":
        for j, line in enumerate(lines): #if date is in the line after "Bestellnummer"
            if "Rechnungsdatum" in line or "Beitragsbescheinigung" in line:
                year = lines[j].split(" ")[1].split(".")[2]
                month = lines[j].split(" ")[1].split(".")[1]
                day = lines[j].split(" ")[1].split(".")[0]
                date[i] = f"{year}{month}{day}"
                break
    elif doc_type[i] == "Techem":
        for j, line in enumerate(lines): #if date is in the line after "Bestellnummer"
            if "Techem" in line:
                year = lines[j-1].split(".")[2]
                month = lines[j-1].split(".")[1]
                day = lines[j-1].split(".")[0]
                date[i] = f"{year}{month}{day}"
                break
    elif doc_type[i] == "Bolt Invoice":
        for j, line in enumerate(lines): #if date is in the line after "Bestellnummer"
            if "Datum" in line:
                year = lines[j].split(": ")[1].split("-")[2]
                month = lines[j].split(": ")[1].split("-")[1]
                day = lines[j].split(": ")[1].split("-")[0]
                date[i] = f"{year}{month}{day}"
                break
    elif doc_type[i] == "Invoice FlixBus":
        year = lines[3].split(" ")[0].split(".")[2]
        month = lines[3].split(" ")[0].split(".")[1]
        day = lines[3].split(" ")[0].split(".")[0]
        date[i] = f"{year}{month}{day}"
    elif doc_type[i] == "Ticket FlixBus":
        for j, line in enumerate(lines): #if date is in the line after "Bestellnummer"
            if "Buchungsnummer" in line:
                split_date = lines[j+1].split(", ")[1].split(". ")       
                date[i] = dateshift(split_date[2], split_date[1], split_date[0], "deu")
                break
    elif doc_type[i] == "DB Ticket":
        for j, line in enumerate(lines):
            if "Halt" in line:
                year = lines[j-1].split(" ")[-1].split(".")[2]
                month = lines[j-1].split(" ")[-1].split(".")[1]
                day = lines[j-1].split(" ")[-1].split(".")[0]
                date[i] = f"{year}{month}{day}"      
                break
    elif doc_type[i] == "Besucherparken":
        for j, line in enumerate(lines): 
            if "Besucherparkausweis" in line:
                year = lines[j-1].split(" ")[-1].split(".")[2]
                month = lines[j-1].split(" ")[-1].split(".")[1]
                day = lines[j-1].split(" ")[-1].split(".")[0]
                date[i] = f"{year}{month}{day}"      
                break
    elif doc_type[i] == "Social Security":
        for j, line in enumerate(lines): 
            if "BRYAN BARCELONA" in line:
                year = lines[j].split(" ")[-1]
                month = lines[j].split(" ")[-3]
                day = lines[j].split(" ")[-2].split(",")[0]
                date[i] = dateshift(year, month, day, "eng_long")    
                break
    elif doc_type[i] == "Haspa Kontoauszug":
        for j, line in enumerate(lines): 
            if "Kontoauszug" in line:
                year = lines[j-1].split(" ")[-1]
                month = lines[j-1].split(" ")[-2]
                day = lines[j-1].split(" ")[-3].split(".")[0].zfill(2)
                date[i] = dateshift(year, month, day, "deu_long")   
                break
    elif doc_type[i] == "Kreditkarte":
        for j, line in enumerate(lines): 
            if "Abrechnungsdatum" in line:
                year = lines[j].split(" ")[-1]
                month = lines[j].split(" ")[-2]
                day = lines[j].split(" ")[-3].split(".")[0].zfill(2)
                date[i] = dateshift(year, month, day, "deu_long")   
                break
    elif doc_type[i] == "KfW Zinssatz" or doc_type[i] == "KfW Lastschrift" or doc_type[i] == "KfW Kontoauszug" or doc_type[i] == "EasyPark" or doc_type[i] == "KfW Jahreskontoauszug" or doc_type[i] == "KfW Jahreszinsbescheinigung":
        for j, line in enumerate(lines): 
            if "Datum" in line:
                year = lines[j].split(" ")[-1].split(".")[2]
                month = lines[j].split(" ")[-1].split(".")[1]
                day = lines[j].split(" ")[-1].split(".")[0]
                date[i] = f"{year}{month}{day}"   
                break
    elif doc_type[i] == "AOK Finanzamt":
        for j, line in enumerate(lines): 
            if "Datum" in line:
                year = lines[j+1].split(" ")[-1]
                month = lines[j+1].split(" ")[-2]
                day = "01"
                date[i] = dateshift(year, month, day, "deu_long")  
                break

    elif doc_type[i] == "StadtRAD":
        for j, line in enumerate(lines): 
            if "Frankfurt am Main," in line:
                year = lines[j].split(" ")[-1].split(".")[2]
                month = lines[j].split(" ")[-1].split(".")[1]
                day = lines[j].split(" ")[-1].split(".")[0]
                date[i] = f"{year}{month}{day}"   
                break

    else:
        date[i] = "None"

    # checking start and destination on travel items
    temp_start_dest = []
    if doc_type[i] == "Invoice FlixBus":
        start = lines[5].split(" ")[0]
        dest = lines[8].split(" ")[0]
        start_dest[i] = f"{start}-{dest}"
        
    elif doc_type[i] == "Ticket FlixBus":
        for j, line in enumerate(lines):
            if "(FlixTrain)" in line:
                temp_start_dest.append(lines[j].split(" ")[1])
        start_dest[i] = f"{temp_start_dest[0]}-{temp_start_dest[1]}"
        
    elif doc_type[i] == "DB Ticket":
        for j, line in enumerate(lines): #if date is in the line after "Bestellnummer"
            if "Halt" in line:
                start = lines[j+1].split(" ")[0]
                dest = lines[j+2].split(" ")[0]
                start_dest[i] = f"{start}-{dest}"      
                
    else:
        start_dest[i] = "N/A"

    # checking and assigning the order or invoice number
    if doc_type[i] == "SEPA Sixt":
        for j, line in enumerate(lines):
            if "Bestellnummer" in line:
                invoice_no[i] = lines[j+1].split(" ")[0]
                break
    elif doc_type[i] == "Invoice Sixt":
        for j, line in enumerate(lines):
            if "Rechn. Nr.:" in line:
                invoice_no[i] = lines[j].split("Rechn. Nr.: ")[1]
                break
    elif doc_type[i] == "Invoice ShareNow":
        for j, line in enumerate(lines):
            if "Rechnungsnr.:" in line:
                invoice_no[i] = lines[j].split(":")[1]
                break
    elif doc_type[i] == "Invoice FlixBus":
        for j, line in enumerate(lines):
            if "Buchungsnummer:" in line:
                invoice_no[i] = lines[j].split("#")[1]
                break
    elif doc_type[i] == "Invoice Congstar" or doc_type[i] == "Bolt Invoice"or doc_type[i] == "EasyPark":
        for j, line in enumerate(lines):
            if "Rechnungsnummer" in line:
                invoice_no[i] = lines[j].split(" ")[-1]
                break
    elif doc_type[i] == "DB Ticket":
        invoice_no[i] = lines[-1].split(" ")[0]
    elif doc_type[i] == "AOK Finanzamt":
        for j, line in enumerate(lines):
            if "für das Jahr" in line:
                invoice_no[i] = lines[j].split(" ")[-1]
                break
    else:
        invoice_no[i] = "None"

move_list= []

for i in range(len(pdf_list)):
    if doc_type[i] == "SEPA Sixt":
        move_list.append(f"D:\\Filing Cabinet\\Rechnungen und Tickets\\Car Sharing\\Sixt\\Zahlungshinweis\\{date[i]} {invoice_no[i]} SEPA notification.pdf")
    elif doc_type[i] == "Invoice Sixt":
        move_list.append(f"D:\\Filing Cabinet\\Rechnungen und Tickets\\Car Sharing\\Sixt\\Rechnung\\{date[i]} {invoice_no[i]} Rechnung.pdf")
    elif doc_type[i] == "Invoice ShareNow":
        move_list.append(f"D:\\Filing Cabinet\\Rechnungen und Tickets\\Car Sharing\\car2go\\Rechnungen\\{date[i]} Rechnung {invoice_no[i]}.pdf")
    elif doc_type[i] == "SEPA ShareNow":
        move_list.append(f"D:\\Filing Cabinet\\Rechnungen und Tickets\\Car Sharing\\car2go\\SEPA\\{date[i]} SEPA Prenotification.pdf")
    elif doc_type[i] == "Invoice Congstar":
        move_list.append(f"D:\\Filing Cabinet\\Handy\\{date[i]} Rechnung.pdf")
    elif doc_type[i] == "Techem":
        move_list.append(f"D:\\Filing Cabinet\\Wohnung\\{date[i]} Verbrauchsinfo Heizung.pdf")
    elif doc_type[i] == "Bolt Invoice":
        move_list.append(f"D:\\Filing Cabinet\\Rechnungen und Tickets\\Car Sharing\\Bolt\\{date[i]} {invoice_no[i]}.pdf")
    elif doc_type[i] == "Gothaer":
        move_list.append(f"D:\\Filing Cabinet\\Versicherungen\\Haftpflichtversicherung\\{date[i]} Finanzamtbescheinigung.pdf")
    elif doc_type[i] == "Invoice FlixBus":
        move_list.append(f"D:\\Filing Cabinet\\Travel\\{date[i]} {start_dest[i]} FlixBus Buchung {invoice_no[i]}.pdf")
    elif doc_type[i] == "Ticket FlixBus":
        move_list.append(f"D:\\Filing Cabinet\\Travel\\{date[i]} {start_dest[i]} FlixBus Ticket.pdf")
    elif doc_type[i] == "DB Ticket":
        move_list.append(f"D:\\Filing Cabinet\\Travel\\{date[i]} {start_dest[i]} {invoice_no[i]} DB Ticket.pdf")
    elif doc_type[i] == "EasyPark":
        move_list.append(f"D:\\Filing Cabinet\\Rechnungen und Tickets\\Car Sharing\\EasyPark\\{date[i]} {invoice_no[i]}.pdf")
    elif doc_type[i] == "Besucherparken":
        move_list.append(f"D:\\Filing Cabinet\\Auto\\Deutschland\\{date[i]} Besucherparkausweis.pdf")     
    elif doc_type[i] == "Social Security":
        move_list.append(f"D:\\Filing Cabinet\\USA\\Social Security\\{date[i]} Statement.pdf")
    elif doc_type[i] == "Haspa Kontoauszug":
        move_list.append(f"D:\\Filing Cabinet\\Haspa\\Kontoauszüge\\{date[i]} Kontoauszug.pdf")
    elif doc_type[i] == "Kreditkarte":
        move_list.append(f"D:\\Filing Cabinet\\Haspa\\Kreditkarte\\{date[i]} Kreditkartenabrechnung.pdf")
    elif doc_type[i] == "KfW Zinssatz":
        move_list.append(f"D:\\Filing Cabinet\\KfW-Studienkredit\\Zinssatz\\{date[i]} Zinssatz.pdf")
    elif doc_type[i] == "KfW Jahreszinsbescheinigung":
        move_list.append(f"D:\\Filing Cabinet\\KfW-Studienkredit\\Zinssatz\\{date[i]} Jahreszinsbescheinigung.pdf")
    elif doc_type[i] == "KfW Lastschrift":
        move_list.append(f"D:\\Filing Cabinet\\KfW-Studienkredit\\Lastschriftankündigung\\{date[i]} Lastschriftankündigung.pdf")
    elif doc_type[i] == "KfW Kontoauszug":
        move_list.append(f"D:\\Filing Cabinet\\KfW-Studienkredit\\Kontoauszüge\\{date[i]} Kontoauszug.pdf")
    elif doc_type[i] == "KfW Jahreskontoauszug":
        move_list.append(f"D:\\Filing Cabinet\\KfW-Studienkredit\\Kontoauszüge\\{date[i]} Jahreskontoauszug.pdf")
    elif doc_type[i] == "AOK Finanzamt":
        move_list.append(f"D:\\Filing Cabinet\\Medical\\AOK\\{date[i]} Beiträge für das Jahr {invoice_no[i]}.pdf")
    elif doc_type[i] == "1&1 Invoice":
        move_list.append(f"D:\\Filing Cabinet\\1&1\\{date[i]} Rechnung.pdf")
    elif doc_type[i] == "StadtRAD":
        move_list.append(f"D:\\Filing Cabinet\\Rechnungen und Tickets\\Car Sharing\\StadtRAD\\{date[i]} Stadtrad.pdf")
    else:
        move_list.append(pdf_list[i])

#print(move_list)
for i in range(len(pdf_list)):
    shuttle_service(pdf_list[i], move_list[i], doc_type[i])




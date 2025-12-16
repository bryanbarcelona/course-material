import glob
import pdfplumber
import re
from dateutil import parser
import os
import logging
import shutil
from string import ascii_uppercase
from .utils.health_check import is_pdf_healthy, is_healthy


class DoctopusPrime:
    def __init__(self, pdf_filepath, base_dir="E:\\Filing Cabinet\\"):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._pdf_filepath = pdf_filepath

        health = is_healthy(self._pdf_filepath)
        print(f"PDF health check for {self._pdf_filepath}: {health}")
        self.logger.info(f"PDF health check for {self._pdf_filepath}: {health}")
        self._base_dir = base_dir
        self._content = self._extract_content(pdf_filepath)
        self._classification_dictionary = self._initalize_classification_dictionary()
        self._category = self._determine_category()
        self._condensed_lines = self._reduce_to_relevant_line()
        self._special_case_handling()
        self._document_date = self._grab_first_date()
        self._invoice_id = self._grab_invoice_id()
        self._output_filename = self._assemble_filename()
        self._output_filepath = self._output_path()
        self._backup_path = self._get_backup_path()
        self._is_new_file = True

    @property
    def filepath(self):
        return self._pdf_filepath

    @property
    def output_path(self):
        return self._pdf_filepath

    @property
    def content(self, reduced=False):
        if not reduced:
            return self._content
        elif reduced:
            return self._condensed_lines

    @property
    def category(self):
        return self._category
    
    @property
    def document_date(self):
        return self._document_date
    
    @property
    def invoice_id(self):
        return self._invoice_id

    @property
    def is_new_file(self):
        return self._is_new_file
        
    def _initalize_classification_dictionary(self):
        dict = {"1&1 Invoice": ["1&1 Telecom GmbH", "539200683"],
                "AOK Finanzamt": ["AOK Rheinland/Hamburg", "Datenübermittlung an die Finanzverwaltung"],
                "Besucherparken": ["Landesbetrieb Verkehr", "Besucherparkausweis"],
                "Billiger-Mietwagen Kostenübersicht": ["FLOYT Mobility GmbH", "Kostenübersicht"],
                "Bolt Invoice": ["Bolt Operations", "Tallinn"],
                "Coaching": ["Georg-Stoklossa", "Coaching"],
                "Congstar Invoice": ["congstar Kundenservice"],
                "DB Ticket": ["DB Fernverkehr AG", "Online-Ticket"],
                "ePrimo Rechnung": ["eprimo GmbH", "Ihre Ökostromrechnung"],
                "ePrimo Abschlagsplan": ["eprimo GmbH", "Abschlagsplan"],
                "ePrimo Preissenkung": ["eprimo GmbH", "Preissenkung"],
                "ePrimo Preisänderung": ["eprimo GmbH", "neue Preis für"],
                "ePrimo Jahresabrechnung": ["eprimo GmbH", "Jahresabrechnung"],
                "EasyPark": ["EasyPark GmbH", "Rechnung"],
                "FlixBus Invoice": ["Flix SE", "Rechnungen für Deine Buchung"],
                "FlixBus Ticket": ["Flix SE", "BORDKARTE"],
                "Gothaer": ["Gesellschaft Gothaer Allgemeine Versicherung"],
                "Hamburg Wasser": ["2352273339", "HAMBURG WASSER"],
                "Haspa Kontoauszug": ["Hamburger Sparkasse", "823351", "Kontoauszug"],
                "H&M": ["H&M", "www.hm.com/de"],
                "KfW Jahreskontoauszug": ["per", "18838652", "KfW", "Jahreskontoauszug"],
                "KfW Jahreszinsbescheinigung": ["Jahreszinsbescheinigung", "KfW"],
                "KfW Kontoauszug": ["Kontoauszug", "18838652", "KfW", "Auszugsnummer"],
                "KfW Lastschriftankündigung": ["Lastschriftankündigung", "KfW-Bankengruppe"],
                "KfW Zinssatz": ["Sollzinssatz", "KfW"],
                "KfW Tilgungsplan": ["Tilgungsplan", "KfW", "KfW-Studienkredit (174)", "Festzinsoption"],
                "Kreditkarte": ["Mastercard", "Hamburger Sparkasse"],
                "Lohnsteuerbescheid": ["00082711", "Lohnsteuerbescheinigung"],
                "McDonalds Rechnung": ["www.mcdonalds.de/kontakt"],
                "Meldebescheinigung zur Sozialversicherung UKE": ["Universitätsklinikum Hamburg-Eppendorf", "Meldebescheinigung zur Sozialversicherung"],
                "Mietwagengutschein": ["Wir wünschen Ihnen eine angenehme Reise und viel Spaß", "Mietwagengutschein"],
                "Miles": ["MILES Mobility GmbH"],
                "MOIA": ["MOIA"],
                "Phrasly": ["Paddle.com Market Ltd"],
                "ShareNow Invoice": ["Free2move Deutschland", "Free2move Fahrt"],
                "ShareNow SEPA": ["Free2move Deutschland", "SEPA Prenotification"],
                "Sixt Invoice": ["Sixt GmbH & Co. Autovermietung KG", "Rechn. Nr.:"],
                "Sixt SEPA": ["Riverty GmbH", "Postfach 5705", "ZAHLUNGSHINWEIS"],
                "Social Security": ["Social Security Statement", "BRYAN BARCELONA"],
                "StadtRAD": ["StadtRAD Hamburg", "Raffineriestraße"],
                "Sushi für Hamburg Barmbek": ["Sushi für Hamburg Barmbek"],
                "Techem": ["Techem Energy Services GmbH"],
                "Techniker Krankenkasse": ["Z048474446"],
                "Tier Invoice": ["Tier Mobility SE", "Rechnung"],
                "UKE Lohnabrechnung": ["00082711", "Verdienstabrechnung"],
                "UHH Beitragsbescheid": ["Beitragsbescheide zum Semesterbeitrag", "keine Einzelbeträge"],
                "UHH Semesterbescheiniguung": ["SEMESTERBESCHEINIGUNG", "SEMESTER-CERTIFICATE"],
            }
        return dict

    def _get_backup_path(self):
        for drive in ascii_uppercase:
            if os.path.exists(f"{drive}:\\log.backup"):
                drive_letter = drive
                break
            else:
                drive_letter = None

        
        if drive_letter and self._output_filepath:
            backup_path = f"{drive_letter}:{self._output_filepath.split(':')[1]}"
            return backup_path
        else:
            return None

    def _extract_content(self, path):
        with pdfplumber.open(path) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()

        return text

    def _determine_category(self):

        for category, triggers in self._classification_dictionary.items():
            if all(trigger in self._content for trigger in triggers):
                return category
        return None

    def _reduce_to_relevant_line(self):
        relevant_triggers = {
            "same_line": ["Rechnungsdatum", "Rechnungsnummer", "Rechnungsnr.", "Rechnungs-Nr.", "Rechnungs-Nr", "Rechn. Nr.", "Rechnung #", 
                          "Abrechnungsdatum", "Datum", "Pullach", "Halle (Saale)", "BRYAN BARCELONA", "OM ", "übermittelt am", "Reference", 
                          "Kostenübersicht", "Buchungsnummer", "Rechnung:", "Invoice reference:", "Auszug:", "Lieferdatum:"],
            "previous_line": ["Besucherparkausweis", "Halt", "Techem", "Kontoauszug", "eprimo GmbH"],
            "next_line": ["Document Date", "Bestellnummer", "Buchungsnummer", "Datum", "Rechnungsdatum", "QUITTUNG"]
        }

        months = ["January", "Januar", "February", "Februar", "March", "März", "April", "May", "Mai", "June", "Juni", "July", "Juli", "August", 
                "September", "October", "Oktober", "November", "December", "Dezember"]

        month_translations = {"January": "Januar",
                      "February": "Februar",
                      "March": "März",
                      "May": "Mai",
                      "June": "Juni",
                      "July": "Juli",
                      "October": "Oktober",
                      "Oct": "Okt",
                      "December": "Dezember",
                      "Dec": "Dez",
                      }

        relevant_lines = []
        lines = self._content.split("\n")

        # Replace translated months with their corresponding keys in each string
        for i, line in enumerate(lines):
            for key, value in month_translations.items():
                if key not in line:
                    lines[i] = lines[i].replace(value, key)
                else:
                    pass


        for i, line in enumerate(lines):
            if any(substring in line for substring in month_translations.keys() | month_translations.values()):
                relevant_lines.append(line)


            for trigger_type, triggers in relevant_triggers.items():
                for trigger in triggers:
                    if trigger in line:
                        if trigger_type == "same_line":
                            line = f"{trigger}{line.split(trigger)[-1]}"
                            relevant_lines.append(line.replace(trigger, "").replace(":", "").strip())
                            relevant_lines.append(line)
                        elif trigger_type == "previous_line" and i > 0:
                            relevant_lines.append(lines[i - 1])
                        elif trigger_type == "next_line" and i < len(lines) - 1:
                            relevant_lines.append(lines[i + 1])

            if any(month.lower() in line.lower() for month in months):
                relevant_lines.append(line)


        return relevant_lines if relevant_lines else lines

    def _parse_date(self, line):

        line = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', line)

        if '.' in line:
        # European notation (DD.MM.YYYY)
            return parser.parse(line, dayfirst=True)
        elif '/' in line:
        # Anglo notation (MM/DD/YYYY)
            return parser.parse(line, dayfirst=False)
        else:
        # Default to European notation if no dots or slashes are found
            return parser.parse(line, dayfirst=True)

    def _grab_first_date(self):
        # Regular expression pattern to match dates in various formats
        #date_pattern = r'\b(?:\d{1,2}[.-/]\d{1,2}[.-/]\d{2,4}|\d{2,4}[.-/]\d{1,2}[.-/]\d{1,2})\b'
        #date_pattern = r'\b(?:\d{1,2}[.-/](?:\d{1,2}|(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?))[.-/]\d{2,4}\b'
        #date_pattern = r'\b(?:\d{1,2}[.-/](?:\d{1,2}|[a-zA-Z]+)[.-/]\d{2,4})\b'
        #date_pattern = r'\b(?:\d{1,2}[ ./-](?:\d{1,2}|[a-zA-Z]+)[ ./-]\d{2,4})\b'
        #date_pattern = r'\b(?:\d{1,2}[ ./-]{1,2}(?:\d{1,2}|[a-zA-Z]+)[ ./-]\d{2,4})\b'
        date_pattern = r'\b(?:\d{1,2}(?:st|nd|rd|th)?[ ./-](?:\d{1,2}|[a-zA-Z]+)[ ./-]\d{2,4})\b'

        date_list = []
        # Iterate through each line of the extracted text
        for i, line in enumerate(self._condensed_lines):
            # Attempt to find a date in the line
            match = re.search(date_pattern, line)
            if match:
                #print(line)
                #return match.group()
                date_list.append(match.group())

        parsed_date = None

        for line in date_list:

            try:
                parsed_date = self._parse_date(line)
                parsed_date = parsed_date.strftime("%Y%m%d")

                return parsed_date
            except:
                continue
         
        return parsed_date
        
    def _grab_invoice_id(self):
        invoice_triggers = ["Rechnungs-Nr",
                            "Rechnungsnummer",
                            "Rechn. Nr.",
                            "Rechnungsnr.",
                            "Rechnung #:",
                            "Rechnung:",
                            "Reference",
                            "Buchungsnummer",
                            "Invoice reference",
                            "Auszug:"
                            ]
        for line in self._condensed_lines:
            for trigger in invoice_triggers:
                if trigger in line:
                    invoice_number = line.replace(trigger, "").replace(":", "").replace(". ", "").replace(")", "").strip()
                    invoice_number = invoice_number.split(" ")[0]
                    return invoice_number

    def _assemble_filename(self):

        filename = ""

        if self._document_date is not None:
            filename += f"{self._document_date} "  # Add space after var1
        if self._category is not None:
            filename += f"{self._category} "  # Add space after var2
        if self._invoice_id is not None:
            filename += f"{self._invoice_id} "  # Add space after var3

        filename = filename.strip()

        filename = f"{filename}.pdf"
        return filename

    def _output_path(self):
        
        filepath = None

        relative_output_paths = {"1&1 Invoice": "1&1",
                "AOK Finanzamt": "Medical\\AOK",
                "Besucherparken": "Auto\\Deutschland",
                "Billiger-Mietwagen Kostenübersicht": "Rechnungen und Tickets\\Car Sharing\\Mietwagen",
                "Bolt Invoice": "Rechnungen und Tickets\\Car Sharing\\Bolt",
                "Coaching": "Medical\\Coaching",
                "Congstar Invoice": "Handy",
                "DB Ticket": "Travel",
                "EasyPark": "Rechnungen und Tickets\\Car Sharing\\EasyPark",
                "ePrimo Rechnung": "Strom",
                "ePrimo Abschlagsplan": "Strom",
                "ePrimo Preissenkung": "Strom",
                "ePrimo Preisänderung": "Strom",
                "ePrimo Jahresabrechnung": "Strom",
                #"FlixBus Invoice": ["Flix SE", "Rechnungen für Deine Buchung"],
                #"FlixBus Ticket": ["Flix SE", "BORDKARTE"],
                "Gothaer": "Versicherungen\\Haftpflichtversicherung",
                "Hamburg Wasser": "Hamburg Wasser",
                "Haspa Kontoauszug": "Haspa\\Kontoauszüge",
                "H&M": "Rechnungen und Tickets",
                "KfW Jahreskontoauszug": "KfW-Studienkredit\\Kontoauszüge",
                "KfW Jahreszinsbescheinigung": "KfW-Studienkredit\\Zinssatz",
                "KfW Kontoauszug": "KfW-Studienkredit\\Kontoauszüge",
                "KfW Lastschriftankündigung": "KfW-Studienkredit\\Lastschriftankündigung",
                "KfW Tilgungsplan": "KfW-Studienkredit\\Tilgungsplan",
                "KfW Zinssatz": "KfW-Studienkredit\\Zinssatz",
                "Kreditkarte": "Haspa\\Kreditkarte",
                "Lohnsteuerbescheid": "Finanzamt\\Lohnsteuerbescheide",
                "McDonalds Rechnung": "Rechnungen und Tickets\\Food",
                "Meldebescheinigung zur Sozialversicherung UKE": "Finanzamt\\Sozialversicherung",
                "Mietwagengutschein": "Rechnungen und Tickets\\Car Sharing\\Mietwagen",
                "Miles": "Rechnungen und Tickets\\Car Sharing\\Miles",
                "MOIA": "Rechnungen und Tickets\\Car Sharing\\MOIA",
                "Phrasly": "Rechnungen und Tickets\\Phrasly",
                "ShareNow Invoice": "Rechnungen und Tickets\\Car Sharing\\car2go\\Rechnungen",
                "ShareNow SEPA": "Rechnungen und Tickets\\Car Sharing\\car2go\\SEPA",
                "Sixt Invoice": "Rechnungen und Tickets\\Car Sharing\\Sixt\\Rechnung",
                "Sixt SEPA": "Rechnungen und Tickets\\Car Sharing\\Sixt\\Zahlungshinweis",
                "Social Security": "USA\\Social Security",
                "StadtRAD": "Rechnungen und Tickets\\Car Sharing\\StadtRAD",
                "Sushi für Hamburg Barmbek": "Rechnungen und Tickets\\Food",
                "Techem": "Wohnung",
                "Techniker Krankenkasse": "Medical\\Krankenkasse",
                "Tier Invoice": "Rechnungen und Tickets\\Car Sharing\\Tier",
                "UKE Lohnabrechnung": "\\Arbeit\\Lohnabrechnungen\\UKE",
                "UHH Beitragsbescheid": "Universität",
                "UHH Semesterbescheiniguung": "Universität",
            }

        for category, path in relative_output_paths.items():
            if self._category == category:
                filepath = f"{self._base_dir}\\{path}\\{self._output_filename}"
                #return filepath
        
        if filepath is None:
            return None

        if not os.path.isfile(filepath):
            return filepath
        
        # If the file already exists and has the same content, append a number to the filename
        if self._extract_content(self._pdf_filepath) == self._extract_content(filepath):
            return filepath
        
        i = 1
        base, ext = os.path.splitext(filepath)

        while os.path.isfile(f"{base}({i}){ext}"):
            i += 1

        filepath = f"{base}({i}){ext}"

        return filepath

    def shuttle_service(self, include_backup=False):

        if self._category is not None:
            output_dir = os.path.dirname(self._output_filepath)
            
            # Create directory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Check if destination file already exists
            if os.path.exists(self._output_filepath):
                # Verify source file exists before deleting
                if os.path.exists(self._pdf_filepath):
                    self._is_new_file = False
                    os.remove(self._pdf_filepath)
                    self.logger.info(f"Destination exists. Deleted source file: {self._pdf_filepath}")
                    print(f"Destination exists. Deleted source file: {self._pdf_filepath}")
                else:
                    self.logger.warning(f"Source file does not exist: {self._pdf_filepath}")
            else:
                # Verify source file exists before moving
                if os.path.exists(self._pdf_filepath):
                    self._is_new_file = True
                    shutil.move(self._pdf_filepath, self._output_filepath)
                    self.logger.info(f"Moved {self._pdf_filepath} to {self._output_filepath}.")
                    print(f"Moved {self._pdf_filepath} to {self._output_filepath}.")
                else:
                    self.logger.warning(f"Source file does not exist: {self._pdf_filepath}")
        else:
            return
        
        if self._backup_path and include_backup:
            if not os.path.exists(os.path.dirname(self._backup_path)):
                os.makedirs(os.path.dirname(self._backup_path))
            shutil.copy(self._output_filepath, self._backup_path)
            print(f"Backed up {self._output_filepath} to {self._backup_path}.")
            self.logger.info(f"Backed up {self._output_filepath} to {self._backup_path}.")

    def _special_case_handling(self):

        date_pattern = r'\b(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(19|20)\d{2}\b' # e.g. 17.08.2023

        if self._category == "McDonalds Rechnung":
            for i, line in enumerate(self._condensed_lines):
                match = re.search(date_pattern, line)
                if match:
                    # Keep only the matched date, discard rest of the line
                    self._condensed_lines[i] = match.group(0).replace("/", ".")
                    

if __name__ == "__main__":

    pdfs = glob.glob(r"C:\Users\bryan\Downloads\*.pdf")

    for pdf in pdfs:
        print(f"{"_"*20}")
        print(pdf)
        current = DoctopusPrime(pdf)
        
        #print(current._output_filepath)
        # # print(current._backup_path)
        #print(current._content)
        print(current._output_filepath)
        # print(current._condensed_lines)
        # print(current._document_date)
        # print(current._category)
        # print(current._invoice_id)
        #current.shuttle_service()





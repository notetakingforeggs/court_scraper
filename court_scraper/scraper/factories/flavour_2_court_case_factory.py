from court_scraper.db.models import CourtCase
from court_scraper.utils.time_converter import normalise_start_time
import re

#TODO this is just copied from 1, needs complete overhaul i reckon
class Flavour2CourtCaseFactory:

    def __init__(self, messy_texts, date, city):
        self.messy_texts = messy_texts
        self.date = date
        self.city = city


    def process_rows_to_cases(self):
            """Converts each row into a court case object."""
            court_cases = []      
            
            for row in self.messy_texts:   
                try: 
                    # print(f"flav2 ccf\n row: {repr(row)}")

                    if len(row) == 6: # Flavour 2, all rows have six maybe?
                        start_time, duration, case_id, case_details, hearing_type, hearing_channel = row
                    #'10:00 AM', '20004883 FK,', 'PUBLIC HEARING - WITH REPORTING   RESTRICTIONS In Person', '60 mins']
                    elif len(row) == 4:
                         start_time, _, case_id, case_details, duration, _, _ = row
                    else:
                        print(f"unexpected row size, skipping this one {row}")
                        continue
                
  
                    hearing_channel = " ".join(hearing_channel.split())
                    hearing_type = " ".join(hearing_type.split())


                    # claimaint vs defendant type
                    if re.search(r' v |vs|-v-|-V-| V ', case_details): 
                    
                        match = re.search(r"(.+?)\s*(?:v|vs|-v-|-V-| V )\s*(.+)", case_details) 
                        if match: # maybe there is a bug where the first research passes and the second one doesnt?
                            claimant = match.group(1).strip()
                            defendant = match.group(2).strip()
                            start_time = normalise_start_time(start_time)
                            court_case = CourtCase(
                                case_id,
                                start_time,
                                self.date,
                                duration,
                                case_details,
                                claimant,
                                defendant,
                                False,
                                hearing_type,
                                hearing_channel,
                                self.city
                            )
                            court_cases.append(court_case)

                    # TODO idk if any of these flavour 2 case lists have a minors? check and remove below if not needed...

                    # subject is A Minor
                    elif re.search(r"a minor", case_details.lower()):
                        court_case = CourtCase(
                        case_id,
                        start_time,
                        self.date,
                        duration,
                        case_details,
                        None,
                        None,
                        True,
                        hearing_type,
                        hearing_channel,
                        self.city
                        )
                        court_cases.append(court_case)
                    # Other
                    else: 
                            court_case = CourtCase(
                            case_id,
                            start_time,
                            self.date,
                            duration,
                            case_details,
                            None,
                            None,
                            False,
                            hearing_type,
                            hearing_channel,
                            self.city
                        )
                            court_cases.append(court_case)
                    
                except (IndexError, ValueError)  as e:
                    print(f"issue with unpacking {e}\n Row: {row}") # this may now be redundant due to the elif chain?     
            return court_cases
            
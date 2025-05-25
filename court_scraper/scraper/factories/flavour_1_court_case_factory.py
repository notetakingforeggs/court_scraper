from court_scraper.db.models import CourtCase
from court_scraper.utils.time_converter import parse_duration, normalise_start_time
import re


class Flavour1CourtCaseFactory:

    def __init__(self, messy_texts, date, city):
        self.messy_texts = messy_texts
        self.date = date
        self.city = city


    def process_rows_to_cases(self):
            """Converts each row into a court case object."""
            court_cases = []      
            
            for row in self.messy_texts:   

                # TODO for chelmsford, issue with only one empty td at the start so trying to parse duration from courtcase ID.

                try:
                    # print(f"flav1 ccf\n row: {repr(row)}")
                    if len(row)>8:
                        try:
                            start_time_span, duration_span, case_details_span, hearing_type_span, hearing_channel_span = row[2:7]
                        except Exception as e:
                            print(f"tried to unpack, and got exception: {e}")
                            continue
                    elif len(row) == 8:
                        # print("88888888888888")
                        start_time_span, duration_span, case_details_span_1, case_details_span_2, hearing_type_span, hearing_channel_span = row[2:8]
                        case_details_span = case_details_span_1 + case_details_span_2
                    elif len(row) == 7:
                        # print("77777777777")
                        start_time_span, duration_span, case_details_span, hearing_type_span, hearing_channel_span = row[2:7]
                        # print(start_time_span, duration_span, case_details_span, hearing_type_span, hearing_channel_span)
                    elif len(row) == 6: # No rows have six?
                        # print("66666666666")
                        _, start_time_span, duration_span, case_details_span, hearing_type_span, hearing_channel_span = row
                    elif len(row) == 5:
                        # print("5555555555")
                        start_time_span, duration_span, case_details_span, hearing_type_span, hearing_channel_span = row
                    elif len(row) == 4:
                        start_time_span, _, case_id, case_details_span, duration_span, _, _ = row
                    else:
                        print(f"unexpected row size, skipping this one {row}")
                        continue
                
                    # TODO some of the case details d cells have two spans in, use the re.search for v to find these cells and conditional
                    # for two spans, consequently joining the inner text into one case details var... maybe can do this before then feeding the rows in?
            
                    start_time_span = normalise_start_time(" ".join(start_time_span.split()))
                    duration_span = parse_duration(duration_span)
                    hearing_channel_span = " ".join(hearing_channel_span.split())
                    hearing_type_span = " ".join(hearing_type_span.split())
                    case_details_list = case_details_span.split(" ")
                    case_id = case_details_list[0]
                    details_span_less_case_id = (" ").join(case_details_list[1:])


                    if re.search(r' v |vs|-v-|-V-| V ', case_details_span): 
                    
                        match = re.search(r"(.+?)\s*(?:v|vs|-v-|-V-| V )\s*(.+)", details_span_less_case_id) 
                        if match: # maybe there is a bug where the first research passes and the second one doesnt?
                            claimant = match.group(1).strip()
                            defendant = match.group(2).strip()
                            court_case = CourtCase(
                                case_id,
                                start_time_span,
                                self.date,
                                duration_span,
                                case_details_span,
                                claimant,
                                defendant,
                                False,
                                hearing_type_span,
                                hearing_channel_span,
                                self.city
                            )
                            court_cases.append(court_case)
                    elif re.search(r"a minor", details_span_less_case_id.lower()):
                        # if len(case_details_list) == 5:  # TODO think about this... why am i doing this if else clause? there was a case where it made sense I think? length 5??/
                        court_case = CourtCase(
                        case_id,
                        start_time_span,
                        self.date,
                        duration_span,
                        case_details_span,
                        None,
                        None,
                        True,
                        hearing_type_span,
                        hearing_channel_span,
                        self.city
                        )
                        court_cases.append(court_case)

                    else: 
                            court_case = CourtCase(
                            case_id,
                            start_time_span,
                            self.date,
                            duration_span,
                            case_details_span,
                            None,
                            None,
                            False,
                            hearing_type_span,
                            hearing_channel_span,
                            self.city
                        )
                            court_cases.append(court_case)
                    
                except (IndexError, ValueError)  as e:
                    print(f"issue with unpacking {e}\n Row: {row}") # this may now be redundant due to the elif chain?     
            return court_cases
            
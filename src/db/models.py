# For data models only

from dataclasses import dataclass,field
from scraper.utils.time_converter import convert_to_unix_timestamp

@dataclass
class CourtCase:
    case_id: str
    start_time_string: str
    duration: str
    claimant: str
    defendant: str
    hearing_type: str
    hearing_channel: str
    start_time_epoch: int  = field(init=False)  
        
    def __post_init__(self):
        self.start_time_epoch = convert_to_unix_timestamp(self.start_time_string)
        
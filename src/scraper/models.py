from dataclasses import dataclass,field

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
        self
    # implement string time to epoch conversion here.
    # maybe also can call a court case normaliser util or smth to get specific court case from string
        
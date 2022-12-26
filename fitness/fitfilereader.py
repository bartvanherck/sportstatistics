import fitdecode
from .fitsession import FitSession, FitDataType

class FitFileReader(object):
    def parse(self, file_name: str) -> bool:
        with fitdecode.FitReader(file_name) as f:
            for frame in f:
                if isinstance(frame, fitdecode.records.FitDataMessage):
                    if frame.name == 'session':
                        yield FitDataType.SESSION, FitSession(frame)

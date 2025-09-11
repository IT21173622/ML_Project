import sys

def error_message_details(error,error_details:sys):
    _,_exc_tb = error_details.exc_info()
    file_name = _exc_tb.tb_frame.f_code.co_filename
    error_message ="ERROR occured in python scripts name [{0}] line number [{1}]  error message[{2}] ".format(
        file_name,_exc_tb.tb_lineno,str(error)
    )


class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_details(error_message,error_detail=error_detail)
    
    def __str__(self):
        return self.error_message
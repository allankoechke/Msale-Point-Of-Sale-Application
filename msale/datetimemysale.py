from datetime import datetime,date,time,timedelta

def getCurrentDate():
    # Return Current Date 
    dt = datetime.now()
    c_date = f"{dt.year}-{dt.month}-{dt.day}"
    print(c_date)
    return c_date

getCurrentDate()
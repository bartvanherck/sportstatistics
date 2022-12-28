
def name_of_month(number):
    m = ["Januari", "Februari", "Maart", "April", "Mei", "Juni", 
         "Juli", "Augustus", "September", "Oktober", "November", "December"]
    return m[number-1]

def speed_to_min_km(speed):
     total = 1000/speed
     minute = int(total/60)
     seconds = int(total) - minute * 60
     return minute, seconds 
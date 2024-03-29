import pandas as pd
from datetime import datetime, date, timedelta
from csv import writer

def str_to_date_list(str_list, date_list):
    for string in str_list:
        date_list.append(datetime.strptime(string, "%d/%m/%Y"))

def str_to_datetime_list(str_list, datetime_list):
    for string in str_list:
        datetime_list.append(datetime.strptime(string, "%d/%m/%Y %H:%M:%S"))

def time_to_datetime_list(date_list, time_list):
    date_time_list = []
    for i in range( len(date_list) ):
        date_time_list.append(date_list[i] + " " + time_list[i])
    return date_time_list

def sort_subject_list(s_subject_list, f_start_datetime_list, s_f_start_datetime_list, num_entries):
    for i in range(num_entries):
        for j in range (num_entries):
            if (f_start_datetime_list[j] == s_f_start_datetime_list[i]):
                s_subject_list.append(subject_list[j])
    return s_subject_list

def datetime_to_str(datetime_object, option):
    if (option == "date"):
        return datetime_object.strftime("%d/%m/%Y")
    elif (option == "time"):
        return datetime_object.strftime("%H:%M")
    else:
        return datetime_object.strftime("%d/%m/%Y %H:%M")
    
def str_to_datetime(str_input, option):
    if (option == "date"):
        return datetime.strptime(str_input, "%d/%m/%Y")
    elif (option == "time"):
        return datetime.strptime(str_input, "%H:%M")
    else:
        return datetime.strptime(str_input, "%d/%m/%Y %H:%M")
    
def datediff_to_h_min(end_date, start_date):
    h_min = end_date - start_date
    h_min = str(h_min).replace(":", " ")
    if ("00 00") in h_min:
        h_min = h_min.replace(" 00 00", "h")
    else:
        h_min = h_min.replace(" 00", "")
        h_min = h_min.replace(" ", "h ") + "min"
    return h_min
    
def compare_strings_case_insensitive(string1, string2, option = "equals"):

    if (option == "greater"):
        if (string1.lower() > string2.lower()):
            return True
        else:
            return False
        
    if (option == "lesser"):
        if (string1.lower() < string2.lower()):
            return True
        else:
            return False

    if (string1.lower() == string2.lower()):
        return True
    else:
        return False
    
def compare_datetime(datetime1, datetime2, option = "equals"):
    
    if (option == "greater"):
        if (datetime1 > datetime2):
            return True
        else:
            return False
        
    if (option == "greater or equal"):
        if (datetime1 >= datetime2):
            return True
        else:
            return False
        
    if (option == "lesser"):
        if (datetime1 < datetime2):
            return True
        else:
            return False
        
    if (option == "lesser or equal"):
        if (datetime1 <= datetime2):
            return True
        else:
            return False

    if (datetime1 == datetime2):
        return True
    else:
        return False

def compare_dates_only(datetime1, datetime2, option = "equals"):
    
    if (option == "greater"):
        if (datetime1.date() > datetime2.date()):
            return True
        else:
            return False
        
    if (option == "greater or equal"):
        if (datetime1.date() >= datetime2.date()):
            return True
        else:
            return False
        
    if (option == "lesser"):
        if (datetime1.date() < datetime2.date()):
            return True
        else:
            return False
        
    if (option == "lesser or equal"):
        if (datetime1.date() <= datetime2.date()):
            return True
        else:
            return False

    if (datetime1.date() == datetime2.date()):
        return True
    else:
        return False
    
def is_time_between(datetimeToCompare, datetime1, datetime2):
    if (datetimeToCompare < datetime1) and (datetimeToCompare > datetime2):
        return True
    elif (datetimeToCompare > datetime1) and (datetimeToCompare < datetime2):
        return True
    else:
        return False

def EventSearch():
    valid_subject = 0
    desired_subject = input(f"Subjects: \n{nd_subject_list}\n What subject would you like to know about")
    for i in range(num_entries):
        if ( (compare_strings_case_insensitive(desired_subject, s_subject_list[i])) and (compare_dates_only(current_datetime, s_f_date_list[i], "lesser or equal")) ):
            Subject = s_subject_list[i]
            Date = datetime_to_str(s_f_date_list[i], "date")
            Start_time = datetime_to_str(s_f_start_datetime_list[i], "datetime")
            End_time = datetime_to_str(s_f_end_datetime_list[i], "datetime")
            print(f'''The next {Subject} class is on {Date}, {Start_time} to {End_time}''')
            print(f"That is in {s_f_start_datetime_list[i] - current_datetime}")
            valid_subject = 1
            break
    
    if (valid_subject == 0):
        print("I wasn't able to find that subject :( what did you do")

def TimeSearch():
    print(f"Enter a time, something like {example_datetime}\n")
    desired_time = input()

    class_found = 0
    more_classes_found = 0

    # "now" is a special string
    if (compare_strings_case_insensitive(desired_time, "now")):
        desired_time = current_datetime

    # "today" is a special string
    elif (desired_time.lower().startswith("today")):
        time_component = desired_time.split()[1]
        desired_time = datetime_to_str(current_datetime.date(), "date") + " " + time_component
        desired_time = str_to_datetime(desired_time, "datetime")

    # "tomorrow" is a special string
    elif (desired_time.lower().startswith("tomorrow")):
        time_component = desired_time.split()[1]
        desired_time = datetime_to_str(current_datetime.date() + timedelta(days=1), "date") + " " + time_component
        desired_time = str_to_datetime(desired_time, "datetime")

    # TODO later can make in x amount of days, just change timedelta(days=x)

    else:
        try:
            desired_time = str_to_datetime(desired_time, "datetime")
        except ValueError:
            print("I think that's not the right format!")

    for i in range(num_entries):
        if (is_time_between(desired_time, s_f_start_datetime_list[i], s_f_end_datetime_list[i])):
            print(f"\nDad is in {s_subject_list[i]}, which ends in {s_f_end_datetime_list[i] - desired_time}")
            class_found = 1

    message_to_send = []

    for k in range(num_entries):
        if ( (compare_dates_only(desired_time, s_f_date_list[k])) and (compare_datetime(desired_time, s_f_end_datetime_list[k], "lesser")) ):
            if (more_classes_found == 0):
                if (class_found == 0):
                    print(f"\nNext class is in: {s_f_start_datetime_list[k] - desired_time}")
                print(f"Classes remaining today:")
            Subject = f"{s_subject_list[k]:10}"
            Start_time = datetime_to_str(s_f_start_datetime_list[k], "time")
            End_time = datetime_to_str(s_f_end_datetime_list[k], "time")
            message_to_send.append(f'''{Subject} | {Start_time} to {End_time}\n''')
            more_classes_found = 1

    if (more_classes_found == 0):
        print("Dad has no more classes afterwards.")
    else:
        message_to_send = "".join(message_to_send)
        print(f'''```{message_to_send}```''')

    if (class_found == 0):
        print("Dad is free at this time. Go nuts!") # + time of next class of the day

def DaySchedule():
    print(f"Enter a date, example: {example_date}\n")
    desired_date = input()
    class_found = 0

    # "today" and "tomorrow" are special strings
    if (compare_strings_case_insensitive(desired_date, "today")):
        desired_date = datetime_to_str(current_datetime, "date")

    if (compare_strings_case_insensitive(desired_date, "tomorrow")):
        desired_date = datetime_to_str(current_datetime + timedelta(days=1), "date")
        
    try:
        desired_date = str_to_datetime(desired_date, "date")
    except ValueError or TypeError:
        print("I think that's not the right format!")

    message_to_send = []

    for i in range(num_entries):
        if (compare_dates_only(desired_date, s_f_date_list[i])):
            Subject = f"{s_subject_list[i]:10}"
            Start_time = datetime_to_str(s_f_start_datetime_list[i], "time")
            End_time = datetime_to_str(s_f_end_datetime_list[i], "time")
            message_to_send.append(f'''{Subject} | {Start_time} to {End_time}\n''')
            class_found = 1
    
    if (class_found == 0):
        print("No classes on that day")
    else:
        message_to_send = "".join(message_to_send)
        print(f'''```{message_to_send}```''')

def EventAdd():
    with open('dadclasses_copy.csv', 'a', newline = '', encoding = 'utf-8') as dc:

        dc_writer = writer(dc)

        print(f'''Enter an event. Format:\n Subject, Date, Start Time, End Time\
            \n Example: {s_subject_list[1]}, {example_date}, {datetime_to_str(current_datetime, "time")}, {"23:69"}\n''')
        
        # row_w is the content to be written
        row_w = input()

        # split into respective columns 0 to 3
        row_w = row_w.split(", ")

        # csv format: subject, start_date, start_time, end_date, end_time
        # all strings
        # dates in d/m/y, times in hr:min:sec
        # start_date and end_date always the same

        # TODO proper exit

        # expect exactly 4 columns of information
        if (len(row_w) != 4):
            print(f'''Number of entries do not match. Please make sure entries are separated by ", " \nYour entry: {row_w}\nYou entered {len(row_w)} values, I want to see 4 values''')

        subject_w =  row_w[0]
        date_w = row_w[1]
        start_time_w = row_w[2] + ":00" # adding the seconds
        end_time_w = row_w[3] + ":00"

        write_list = [subject_w, date_w, start_time_w, date_w, end_time_w]
        print(write_list)

        print("Are you sure you want to add this to your calendar? Y/N\n")
        write_confirm = input()

        if write_confirm.upper() == "Y":
            dc_writer.writerow(write_list)
            print("Success!")
        else:
            print("It's ok, mistakes happen. Look at you.")

def AvailabilitySearch():
    class_found = 0

    print(f"Enter a date, example: {example_date}\n")
    desired_date = input()

    if (compare_strings_case_insensitive(desired_date, "today")):
        desired_date = datetime_to_str(current_datetime, "date")

    if (compare_strings_case_insensitive(desired_date, "tomorrow")):
        desired_date = datetime_to_str(current_datetime + timedelta(days=1), "date")
        
    try:
        desired_date = str_to_datetime(desired_date, "date")
    except ValueError or TypeError:
        print("I think that's not the right format!")

    message_to_send = []

    for i in range(num_entries):
        if (compare_dates_only(desired_date, s_f_date_list[i])):
            class_found = 1
            # s_f_end_datetime_list[i] to s_f_start_datetime_list[i+1], if i+1 matches the current date
            if (compare_dates_only(desired_date, s_f_start_datetime_list[i+1])):
                Free_time_length = datediff_to_h_min(s_f_start_datetime_list[i+1], s_f_end_datetime_list[i])
                Start_time = datetime_to_str(s_f_end_datetime_list[i], "time")
                End_time = datetime_to_str(s_f_start_datetime_list[i+1], "time")
                message_to_send.append(f'''Dad is free for {Free_time_length} from {Start_time} to {End_time}\n''')
            else:
                message_to_send = "".join(message_to_send)
                print(f'''{message_to_send}''')
                print(f'''Dad comes home after {datetime_to_str(s_f_end_datetime_list[i], "time")}''')
        
    if (class_found == 0):
        print("No classes on that day")


df = pd.read_csv(r"dadclasses_copy.csv",
    delimiter = ",",
    usecols = ["Subject", "Date", "Start Time", "End Time"],
    dtype = None)

subject_list =  df["Subject"].values.tolist() # 'COM S 227', 'COM S 227', 'COM S 227', 'COM S 227'
s_subject_list = []
nd_subject_list = [*set(subject_list)]

# list of dates where I have classes
date_list = df["Date"].values.tolist() # '19/1/2023', '26/1/2023', '31/1/2023', '2/2/2023', '7/2/2023'
f_date_list = []
str_to_date_list(date_list, f_date_list)
s_f_date_list = sorted(f_date_list)

# start time of classes
start_time_list = df["Start Time"].values.tolist() # '08:50:00', '08:50:00', '08:50:00', '08:50:00', '08:50:00'
start_datetime_list = time_to_datetime_list(date_list, start_time_list)
f_start_datetime_list = []
str_to_datetime_list(start_datetime_list, f_start_datetime_list)
s_f_start_datetime_list = sorted(f_start_datetime_list)

# end time of classes 
end_time_list = df["End Time"].values.tolist() # '09:40:00', '09:40:00', '09:40:00', '09:40:00', '09:40:00', '09:40:00'
end_datetime_list = time_to_datetime_list(date_list, end_time_list)
f_end_datetime_list = []
str_to_datetime_list(end_datetime_list, f_end_datetime_list)
s_f_end_datetime_list = sorted(f_end_datetime_list)

# useful when iterating over lists, length of most lists unless they are nd or otherwise
num_entries = len(subject_list)

# sorting subject list
for i in range(num_entries):
    for j in range (num_entries):
        if (f_start_datetime_list[j] == s_f_start_datetime_list[i]):
            s_subject_list.append(subject_list[j])

current_datetime = datetime.now()
example_datetime = datetime_to_str(current_datetime, "datetime")
example_date = datetime_to_str(current_datetime, "date")
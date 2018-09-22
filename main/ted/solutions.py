def SingleRunway(flight_list):
    flight_details = flight_list["Flights"]

    reserve_time = flight_list["Static"]["ReserveTime"]

    flight_details = sorted(flight_details, key=lambda k: k['Time'])

    json_object = {
        "Flights": flight_details
    }

    return json_object


def convertToMinutes(seconds):
    '''takes in seconds and returns num_of_minutes'''

    # gets lower denom of minutes
    num_of_minutes = seconds // 60

    # get number of remaining seconds
    remainder = seconds - num_of_minutes * 60

    if remainder != 0:
        num_of_minutes += 1

    return num_of_minutes


def addToTime(time, seconds):
    '''takes in time parameter and seconds parameter and adds them together
    returning time in 24 hour clock format'''

    # extract number of minutes on 24 hours clock from the time
    minutes = convertToMinutes(seconds)

    clock_minutes = int(time[2:])

    clock_hours = int(time[:2])

    total_mins = clock_minutes + minutes

    if total_mins >= 60:

        hours_to_add = total_mins // 60

        minutes_remainding = minutes - hours_to_add * 60
    else:
        minutes_remainding = minutes
        hours_to_add = 0

    minutes_time = clock_minutes + minutes_remainding

    hours_time = clock_hours + hours_to_add

    # account for 24 hours above clock

    if hours_time >= 24:
        # get the num times it exceeds the 24 hour clock
        hours_multiple = hours_time // 24

        hours_left = hours_time - (hours_multiple * 24)

        hours_time = hours_left

    # if length of minutes and hours is only 1, append a 0 to the start of the string so that you get an accurate 24 hours clock
    if len(str(minutes_time)) == 1:
        minutes_time = "0" + str(minutes_time)

    if len(str(hours_time)) == 1:
        hours_time = "0" + str(hours_time)

    return str(hours_time) + str(minutes_time)


def MultipleRunways(flight_list):
    # sorted list of dictionaries of flights according to their time of arrival

    flight_details = sorted(flight_list["Flights"], key=lambda k: k['Time'])

    # list of available runways
    runways = flight_list["Static"]["Runways"]

    print(runways)

    # reserve_time is in seconds
    reserve_time = int(flight_list["Static"]["ReserveTime"])

    # sort the list
    minutes = convertToMinutes(reserve_time)

    # get the assigned list
    runway_assigned_list = []
    print(flight_details)

    length_list = len(flight_details)

    # loop through flight_details flights dict and assign runway according to flights

    flight_details[0]["Runway"] = runways[0]
    runway_assigned_list.append(flight_details[0])

    runway_lead_time_dict = {}
    for runway in runways:
        runway_lead_time_dict[runway] = 0

    runway_index = list(runway_lead_time_dict.keys())

    runway_lead_time_dict[runway_index[0]] = int(
        addToTime(flight_details[0]["Time"], int(flight_list["Static"]["ReserveTime"])))

    for i in range(1, length_list):

        # lead_time = addToTime(flight_details[i-1]["Time"], int(flight_list["Static"]["ReserveTime"]))
        plane_dets = flight_details[i]

        for k in range(len(runway_index)):
            # print(runway_lead_time_dict)

            lead_time = runway_lead_time_dict[runway_index[k]]

            if int(plane_dets["Time"]) > lead_time:
                flight_details[i]["Runway"] = runway_index[k]
                runway_assigned_list.append(flight_details[i])
                lead_time = addToTime(flight_details[i]["Time"], int(flight_list["Static"]["ReserveTime"]))
                runway_lead_time_dict[runway_index[k]] = int(lead_time)
                break

            else:
                continue
            #     if k == len(runway_index) - 1:
            #         k = 0
            #     else:
            #         k = k + 1
            #     flight_details[i]["Runway"] = runway_index[k]
            #     runway_assigned_list.append(flight_details[i])
            #     lead_time = addToTime(flight_details[i]["Time"], int(flight_list["Static"]["ReserveTime"]))
            #     runway_lead_time_dict[runway_index[k]] = int(lead_time)
            # break

    return runway_assigned_list
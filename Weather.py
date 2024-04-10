# DSC 510 T302
# Week 12 Final Project
# Programming assignment- weather utility
# David Pahmer
# 3/5/22
# This program gives weather information for locations specified by the user

'''
Weather Program
For your class project we will be creating an application to interacts with a webservice in order to obtain data.
    Your program will use all of the information you’ve learned in the class in order to create a useful application.
Your program must prompt the user for their city or zip code and request weather forecast data from OpenWeatherMap.
Your program must display the weather information in a READABLE format to the user.
Requirements:
    Create a header for your program just as you have in the past.
    Create a Python Application which asks the user for their zip code or city (Your program must perform both a city and a zip lookup).
    You must ask the user which they want to perform with each iteration of the program.
    Use the zip code or city name in order to obtain weather forecast data from OpenWeatherMap.
    Display the weather forecast in a readable format to the user. Do not display the weather data in Kelvin, since this is not readable to the average person.
    You should allow the user to choose between Celsius and Fahrenheit and ideally also Kelvin.
    Use comments within the application where appropriate in order to document what the program is doing.
    Comments should add value to the program and describe important elements of the program.
    Use functions including a main function and a properly defined call to main. You should have multiple functions.
    Allow the user to run the program multiple times to allow them to look up weather conditions for multiple locations.
    Validate whether the user entered valid data. If valid data isn’t presented notify the user. Your program should never crash with bad user input.
    Use the Requests library in order to request data from the webservice.
    Use Try blocks to ensure that your request was successful. If the connection was not successful display a message to the user.
    Use Python 3
    Use try blocks when establishing connections to the webservice. You must print a message to the user indicating whether or not the connection was successful.
    You must have proper coding convention including proper variable names (See PEP8).
Deliverables:
    Final Program in a .py file (Due week 12)
Project Notes:
    Be creative. This assignment is a real world program. Use it as an opportunity to improve your knowledge.
    Make a connection to the API using the Requests library.

'''

import requests, json, datetime


def location_getter():
    location = input("Please enter the city for your inquiry. Or city, country.")
    mykey = ""
    locurl = "https://api.openweathermap.org/geo/1.0/direct?q=" + location + "&limit=1" + mykey
    try:
        response = requests.get(locurl)
        response.raise_for_status()
    except:
        print("That location isn't valid. Please try again next time.")
        return ""

    if len(response.text) < 10:  # Sometimes it comes back blank.
        print("The system doesn't recognize that location. PLease try a different name.")
        return ""
    else:
        loc = json.loads(response.text)
        latlon = "&lat=" + str(loc[0]["lat"]) + "&lon=" + str(loc[0]["lon"])
        try:
            statecode = loc[0]["state"]  # because the state value isn't always present, like for some international cities
        except:
            statecode = ""

        print("You requested weather information for", loc[0]["name"], "located in", statecode, loc[0]["country"])
        return latlon


def ziptocoord():
    zip = input("Please enter the zipcode for your inquiry.")
    mykey = "&APPID="
    locurl = "https://api.openweathermap.org/geo/1.0/zip?zip=" + zip + mykey

    try:
        response = requests.get(locurl)
        response.raise_for_status()
    except:
        print("That location isn't valid. Please try again next time.")
        return ""

    if len(response.text) < 10:
        print("The system doesn't recognize that location. PLease try a different name.")
        return ""

    loc = json.loads(response.text)
    latlon = "&lat=" + str(loc["lat"]) + "&lon=" + str(loc["lon"])
    print("You requested weather information for zipcode", loc["zip"], "located in", loc["name"])
    return latlon


def connect_to_forecast(location, unit):
    website_forecast = "https://api.openweathermap.org/data/3.0/onecall?"
    mykey = "&APPID="
    unitcall = "&units=" + unit
    urlpage_forecast = website_forecast + location + unitcall + mykey
    try:
        response = requests.get(urlpage_forecast)
        response.raise_for_status()
    except:
        return ""

    return response.text


def cleanup(report):
    week = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

    print("\n Current temperature:", int(report['current']['temp']), "    Current conditions:", report['current']['weather'][0]['description'], "\n")

    print("****   Forecast for the next few days:   ****\n")
    print("Day #   (Day)             (Date)         Low Temp:   High Temp:     Condition:     Chance of rain / snow:")
    for daynum in range(7):
        print(daynum + 1, "   ",
              f"{week[datetime.datetime.utcfromtimestamp(report['daily'][daynum]['dt']).weekday()]:<15}",
              f"{datetime.datetime.utcfromtimestamp(report['daily'][daynum]['dt']).strftime('%m/%d/%Y'):<20}",
              f"{int(report['daily'][daynum]['temp']['min']):>5}", "     ",
              f"{int(report['daily'][daynum]['temp']['max']):>5}", "         ",
              f"{report['daily'][daynum]['weather'][0]['main']:<10}", "           ",
              int(100*(report["daily"][daynum]['pop'])), "%")

    try:
        alerts = report["alerts"][0]["description"]
    except:
        print("No weather alerts in effect")
    else:
        print(alerts)
    print()


def main():

    print("Welcome to the Weather application\n")
    while True:
        selector = input("Enter location for forecast: type 1 for zipcode; type 2 for city name; type Q to quit ")
        if selector.upper() == "Q":
            exit()
        elif selector == "1":
            coordinates = ziptocoord()
        elif selector == "2":
            coordinates = location_getter()
        else:
            continue
        if coordinates != "":
            units = "imperial"
            changeunit = input("Type C for Celsius; if you want Fahrenheit just hit enter ")
            if changeunit.upper() == "C":
                units = "metric"
            try:
                report = json.loads(connect_to_forecast(coordinates, units))
            except:
                print("Something went wrong. Try again. ")
            else:
                cleanup(report)


if __name__ == '__main__':
    main()

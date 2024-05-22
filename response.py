import random
import json
import streamlit as st
from datetime import datetime

# Generate response
def generate_response(tag, tag_prob, intents, data):
    if tag_prob > 0.75:
        for intent in intents['intents']:
            if intent['tag'] == tag:
                responses = intent['responses']
                selected_response = random.choice(responses)

                # Handle specific responses
                match tag:
                    # Route
                    case "route":
                        return selected_response, "images/Routes.png"
                    case "route AB":
                        return selected_response, "images/Route_AB.png"
                    case "route BA":
                        return selected_response, "images/Route_BA.png"
                    case "route C":
                        return selected_response, "images/Route_C.png"
                    case "route D":
                        return selected_response, "images/Route_D.png"
                    case "route E":
                        return selected_response, "images/Route_E.png"
                    case "route 13":
                        return selected_response, "images/Route_13.png"
                    # Schedule
                    case "schedule":
                        return selected_response, "images/Schedule.png"
                    case "schedule/frequency for bus AB":
                        return selected_response, "images/Schedule_AB_BA_E.png"
                    case "schedule/frequency for bus BA":
                        return selected_response, "images/Schedule_AB_BA_E.png"
                    case "schedule/frequency for bus C":
                        return selected_response, "images/Schedule_C.png"
                    case "schedule/frequency for bus D":
                        return selected_response, "images/Schedule_D.png"
                    case "schedule/frequency for bus E":
                        return selected_response, "images/Schedule_AB_BA_E.png"
                    case "schedule/frequency for bus 13":
                        return selected_response, "images/Schedule_13.png"
                    # Next and previous bus times
                    case "next/previous bus for route AB":
                        return handle_next_previous_bus("AB", data, selected_response)
                    case "next/previous bus for route BA":
                        return handle_next_previous_bus("BA", data, selected_response)
                    case "next/previous bus for route C":
                        return handle_next_previous_bus("C", data, selected_response)
                    case "next/previous bus for route D":
                        return handle_next_previous_bus("D", data, selected_response)
                    case "next/previous bus for route E":
                        return handle_next_previous_bus("E", data, selected_response)
                    case "next/previous bus for route 13":
                        return handle_next_previous_bus("13", data, selected_response)
                    # Destinations
                    case "UM CENTRAL":
                        return get_routes_for_destination("UM CENTRAL", selected_response, data)
                    case "KK13":
                        return get_routes_for_destination("KK13", selected_response, data)
                    case "KK12":
                        return get_routes_for_destination("KK12", selected_response, data)
                    case "KK11":
                        return get_routes_for_destination("KK11", selected_response, data)
                    case "KK10":
                        return get_routes_for_destination("KK10", selected_response, data)
                    case "KK8":
                        return get_routes_for_destination("KK8", selected_response, data)
                    case "KK7":
                        return get_routes_for_destination("KK7", selected_response, data)
                    case "KK5":
                        return get_routes_for_destination("KK5", selected_response, data)
                    case "KK4":
                        return get_routes_for_destination("KK4", selected_response, data)
                    case "KK3":
                        return get_routes_for_destination("KK3", selected_response, data)
                    case "KK1":
                        return get_routes_for_destination("KK1", selected_response, data)
                    case "INTERNATIONAL HOUSE":
                        return get_routes_for_destination("INTERNATIONAL HOUSE", selected_response, data)
                    case "FACULTY OF ENGINEERING":
                        return get_routes_for_destination("FACULTY OF ENGINEERING", selected_response, data)
                    case "FACULTY OF SCIENCE":
                        return get_routes_for_destination("FACULTY OF SCIENCE", selected_response, data)
                    case "ACADEMY OF ISLAM STUDIES":
                        return get_routes_for_destination("ACADEMY OF ISLAM STUDIES", selected_response, data)
                    case "ACADEMY OF MALAY STUDIES":
                        return get_routes_for_destination("ACADEMY OF MALAY STUDIES", selected_response, data)
                    case "BANGSAR SOUTH":
                        return get_routes_for_destination("BANGSAR SOUTH", selected_response, data)
                    case "KTM ANGKASAPURI STATION":
                        return get_routes_for_destination("KTM ANGKASAPURI STATION", selected_response, data)
                    case "PANTAI PERMAI":
                        return get_routes_for_destination("PANTAI PERMAI", selected_response, data)
                    case "PASUM":
                        return get_routes_for_destination("PASUM", selected_response, data)
                    case "RAPID STOP":
                        return get_routes_for_destination("RAPID STOP", selected_response, data)
                   
                return selected_response, None
                
        return "I'm sorry, I don't understand. Please try a different question.", None
    else:
        return "I'm sorry, I don't understand. Please try a different question.", None

def handle_next_previous_bus(selected_route, data, selected_response):
    # Get current time
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    for route in data['routes']:
        if route['route name'] == selected_route:
            next_bus_time = get_next_bus(current_time, route['arrival times'])
            previous_bus_time = get_previous_bus(current_time, route['arrival times'])
                
            selected_response = selected_response.replace("{next bus time}", next_bus_time).replace("{previous bus time}", previous_bus_time)
    return selected_response, None

def get_next_bus(current_time, arrival_times):
    format = "%H:%M"
    current_time = datetime.strptime(current_time, format)

    for time in arrival_times:
        time = datetime.strptime(time, format)
        if time > current_time:
            return time.strftime(format)
    return arrival_times[0]

def get_previous_bus(current_time, arrival_times):
    format = "%H:%M"
    current_time = datetime.strptime(current_time, format)
    
    for time in reversed(arrival_times):
        time = datetime.strptime(time, format)
        if time < current_time:
            return time.strftime(format)
    return arrival_times[-1]

def get_routes_for_destination(destination, selected_response, data):
    routes = []
    for route in data['routes']:
        for stop in route['stops']:
            if stop.lower() == destination.lower() or destination.lower() in stop.lower():
                routes.append(route['route name'])
                break
    
    selected_response = selected_response + ', '.join(routes)
    return selected_response, None
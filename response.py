import random
import json
from datetime import datetime

# Generate response
def generate_response(tag, tag_prob, intents):
    if tag_prob > 0.75:
        for intent in intents['intents']:
            if intent['tag'] == tag:
                responses = intent['responses']
                selected_response = random.choice(responses)

                # Handle the responses that contain images
                # Route
                if (tag == "route"):
                    return selected_response, "images/Routes.png"
                if (tag == "route AB"):
                    return selected_response, "images/Route_AB.png"
                if (tag == "route BA"):
                    return selected_response, "images/Route_BA.png"
                if (tag == "route C"):
                    return selected_response, "images/Route_C.png"
                if (tag == "route D"):
                    return selected_response, "images/Route_D.png"
                if (tag == "route E"):
                    return selected_response, "images/Route_E.png"
                if (tag == "route 13"):
                    return selected_response, "images/Route_13.png"
                
                # Schedule
                if (tag == "schedule"):
                    return selected_response, "images/Schedule.png"
                if (tag == "schedule/frequency for bus AB" or tag == "schedule/frequency for bus BA" or tag == "schedule/frequency for bus E"):
                    return selected_response, "images/Schedule_AB_BA_E.png"
                if (tag == "schedule/frequency for bus C"):
                    return selected_response, "images/Schedule_C.png"
                if (tag == "schedule/frequency for bus D"):
                    return selected_response, "images/Schedule_D.png"
                if (tag == "schedule/frequency for bus 13"):
                    return selected_response, "images/Schedule_13.png"

                # Next and previous bus times
                if (tag == "next/previous bus for route AB"):
                    return handle_next_previous_bus("AB", selected_response)
                if (tag == "next/previous bus for route BA"):
                    return handle_next_previous_bus("BA", selected_response)
                if (tag == "next/previous bus for route C"):
                    return handle_next_previous_bus("C", selected_response)
                if (tag == "next/previous bus for route D"):
                    return handle_next_previous_bus("D", selected_response)
                if (tag == "next/previous bus for route E"):
                    return handle_next_previous_bus("E", selected_response)
                if (tag == "next/previous bus for route 13"):
                    return handle_next_previous_bus("13", selected_response)
                
                return selected_response, None
                
        return "I'm sorry, I don't understand. Please try again.", None
    else:
        return "I'm sorry, I don't understand. Please try again.", None

def handle_next_previous_bus(selected_route, selected_response):
    # Get current time
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    with open('data.json') as data:
        schedule = json.load(data)

    for routes in schedule['routes']:
        for route in routes['route name']:
            if route == selected_route:
                next_bus_time = get_next_bus(current_time, routes['arrival times'])
                previous_bus_time = get_previous_bus(current_time, routes['arrival times'])
                
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

def load_intents():
    with open('intents.json') as data:
        intents = json.load(data)
    return intents

# Testing purposes
intents = load_intents()
print(generate_response("next/previous bus for route 13", 0.8, intents))
import customtkinter as ctk
import joblib
import numpy as np

# Load model
model = joblib.load("model.pkl")

# Constants
airlines = ['AirAsia', 'Air_India', 'GO_FIRST', 'Indigo', 'SpiceJet', 'Vistara']
cities = ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Hyderabad', 'Chennai']
departure_times = ['Morning', 'Early_Morning', 'Evening', 'Night', 'Afternoon', 'Late_Night']
arrival_times = ['Night', 'Evening', 'Morning', 'Afternoon', 'Early_Morning', 'Late_Night']
stops_list = ['zero', 'one', 'two_or_more']
classes = ['Economy', 'Business']

# Encode features
def encode_inputs(user_input):
    stops = {'zero': 0, 'one': 1, 'two_or_more': 2}[user_input['stops']]
    travel_class = 0 if user_input['class'] == 'Economy' else 1
    duration = float(user_input['duration'])
    days_left = int(user_input['days_left'])

    features = [stops, travel_class, duration, days_left]

    def one_hot(value, categories): return [1 if value == cat else 0 for cat in categories]

    features += one_hot(user_input['airline'], airlines)
    features += one_hot(user_input['source_city'], cities)
    features += one_hot(user_input['destination_city'], cities)
    features += one_hot(user_input['arrival_time'], arrival_times)
    features += one_hot(user_input['departure_time'], departure_times)

    return np.array([features])

# Prediction handler
def predict_price():
    try:
        user_input = {
            'airline': airline_cb.get(),
            'source_city': source_cb.get(),
            'destination_city': destination_cb.get(),
            'departure_time': departure_cb.get(),
            'arrival_time': arrival_cb.get(),
            'stops': stops_cb.get(),
            'class': class_cb.get(),
            'duration': duration_entry.get(),
            'days_left': days_entry.get()
        }

        X = encode_inputs(user_input)
        prediction = model.predict(X)[0]
        result_label.configure(text=f"₹ {int(prediction)}", text_color="#00aa55")
    except Exception:
        result_label.configure(text="Invalid input", text_color="red")

def clear_fields():
    airline_cb.set(airlines[0])
    source_cb.set(cities[0])
    destination_cb.set(cities[1])
    departure_cb.set(departure_times[0])
    arrival_cb.set(arrival_times[0])
    stops_cb.set(stops_list[0])
    class_cb.set(classes[0])
    duration_entry.delete(0, "end")
    days_entry.delete(0, "end")
    result_label.configure(text="")

# Appearance
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# App config
app = ctk.CTk()
app.title("Flight Price Predictor")
app.geometry("400x580")
app.resizable(False, False)

title = ctk.CTkLabel(app, text="Flight Price Predictor", font=ctk.CTkFont(size=20, weight="bold"))
title.pack(pady=10)

frame = ctk.CTkFrame(app)
frame.pack(pady=5, padx=10, fill="both", expand=True)

# Grid form
def add_row(row, label_text, widget):
    ctk.CTkLabel(frame, text=label_text).grid(row=row, column=0, sticky="w", padx=10, pady=4)
    widget.grid(row=row, column=1, padx=10, pady=4)

airline_cb = ctk.CTkComboBox(frame, values=airlines, width=160)
source_cb = ctk.CTkComboBox(frame, values=cities, width=160)
destination_cb = ctk.CTkComboBox(frame, values=cities, width=160)
departure_cb = ctk.CTkComboBox(frame, values=departure_times, width=160)
arrival_cb = ctk.CTkComboBox(frame, values=arrival_times, width=160)
stops_cb = ctk.CTkComboBox(frame, values=stops_list, width=160)
class_cb = ctk.CTkComboBox(frame, values=classes, width=160)
duration_entry = ctk.CTkEntry(frame, width=160)
days_entry = ctk.CTkEntry(frame, width=160)

airline_cb.set(airlines[0])
source_cb.set(cities[0])
destination_cb.set(cities[1])
departure_cb.set(departure_times[0])
arrival_cb.set(arrival_times[0])
stops_cb.set(stops_list[0])
class_cb.set(classes[0])

add_row(0, "Airline:", airline_cb)
add_row(1, "Source:", source_cb)
add_row(2, "Destination:", destination_cb)
add_row(3, "Departure:", departure_cb)
add_row(4, "Arrival:", arrival_cb)
add_row(5, "Stops:", stops_cb)
add_row(6, "Class:", class_cb)
add_row(7, "Duration (hrs):", duration_entry)
add_row(8, "Days Left:", days_entry)

# Buttons
btn_frame = ctk.CTkFrame(app, fg_color="transparent")
btn_frame.pack(pady=10)

ctk.CTkButton(btn_frame, text="Predict", command=predict_price, width=120).grid(row=0, column=0, padx=10)
ctk.CTkButton(btn_frame, text="Clear", command=clear_fields, width=80, fg_color="gray", hover_color="darkgray").grid(row=0, column=1, padx=10)

# Result label
result_label = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=18, weight="bold"))
result_label.pack(pady=10)

# Run loop
app.mainloop()
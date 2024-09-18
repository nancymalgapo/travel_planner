import streamlit as st
import openai

from utils.helpers import send_email, is_valid_input, create_pdf
from utils.values import *


def app_sidebar():
    departure_date = st.sidebar.date_input(
        "Select a date",
        help="Choose the date of departure."
    )

    return_date = st.sidebar.date_input(
        label="Select a return date",
        key="return_date",
        help="Choose the date of return.",
    )

    origin = st.sidebar.selectbox(
        "Origin",
        options=destinations,
        help="Select your target destination",
    )

    destination = st.sidebar.selectbox(
        "Destination",
        options=destinations,
        help="Select your target destination",
    )

    trip_type = st.sidebar.selectbox(
        "Select a travel reason",
        options=["Solo", "Business", "Romantic", "Friends", "Family"],
        help="Select your travel reason",
    )

    budget = st.sidebar.slider("Your budget", min_value=3000, max_value=1000000)
    st.sidebar.write("PHP", budget)

    if st.sidebar.button("Plan My Travel"):
        openai.api_key = st.secrets["openai"][key]
        error_message, is_valid = is_valid_input(departure_date, return_date, openai.api_key)
        if is_valid:
            with st.spinner("Generating itinerary based on your preferences .."):
                st.title("My Plans For Your Travel")
                try:
                    response = openai.Completion.create(
                        engine="gpt-3.5-turbo-instruct",
                        prompt=f"Generated a travel itinerary from {origin} to {destination} from {departure_date} to "
                               f"{return_date} with a budget of PHP{budget} for a {trip_type} trip.",
                        max_tokens=300
                    )
                    itinerary = response.choices[0].text.strip()
                    st.success("Here’s your itinerary:")
                    st.write(itinerary)

                    st.download_button(
                        label="Download TravelMate Generated Itinerary",
                        data=create_pdf(itinerary),
                        file_name="TravelMate_generated_itinerary.pdf",
                        mime="application/pdf"
                    )

                    recipient_email = st.text_input("Enter your email to receive the itinerary:")
                    if st.button("Send to Email"):
                        if recipient_email:
                            send_email(itinerary, recipient_email)
                        else:
                            st.error("Please enter a valid email address.", icon="🚨")

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}", icon="🚨")
        else:
            st.error(error_message, icon="🚨")

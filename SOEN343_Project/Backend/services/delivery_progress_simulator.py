"""
Delivery Progress Simulator
Simulates the progress of a delivery, updating the tracker and estimated delivery time.
"""

import time
from threading import Thread
from flask import current_app
from models.logistics.delivery_request import DeliveryRequest
from models.logistics.tracker import Tracker, DeliveryStatus
from services.distance_service import DistanceService
from dbconnection import db


def start_simulation(tracker_id):
    """
    Start the delivery simulation in a separate thread.
    """
    app = current_app._get_current_object()  # Get the actual app object
    Thread(target=simulate_delivery_progress, args=(app, tracker_id)).start()


def simulate_delivery_progress(app, tracker_id):
    """
    Simulate the delivery progress of a tracker, updating its estimated delivery time
    and status at intermediate locations.
    """
    with app.app_context():  # Push the app context explicitly for threading
        tracker = Tracker.query.get(tracker_id)
        if not tracker:
            print(f"Tracker with ID {tracker_id} not found.")
            return

        delivery_request = DeliveryRequest.query.get(
            tracker.order.delivery_request_id
        )
        if not delivery_request:
            print(f"Delivery request for tracker {tracker_id} not found.")
            return

        origin = f"{delivery_request.pick_up_address.street} {delivery_request.pick_up_address.house_number}, " \
            f"{delivery_request.pick_up_address.city}, {
                delivery_request.pick_up_address.country}"
        destination = f"{delivery_request.drop_off_address.street} {delivery_request.drop_off_address.house_number}, " \
            f"{delivery_request.drop_off_address.city}, {
                delivery_request.drop_off_address.country}"

        try:
            # Fetch intermediate locations and calculate total travel time
            intermediate_locations = DistanceService.get_intermediate_locations(
                origin, destination)
            total_travel_time = DistanceService.calculate_route_time(
                origin, destination)

            if not intermediate_locations or total_travel_time is None:
                print(f"No intermediate locations or invalid travel time for tracker {
                      tracker_id}.")
                return

            print(f"Intermediate locations for tracker {
                  tracker_id}: {intermediate_locations}")
            print(f"Total travel time for tracker {
                  tracker_id}: {total_travel_time} minutes")

            # Initialize estimated delivery time if it's not set
            if tracker.estimated_delivery_time is None:
                tracker.estimated_delivery_time = total_travel_time
                db.session.commit()

            # Calculate time to reach each intermediate location
            segment_time = total_travel_time / len(intermediate_locations)

            for location in intermediate_locations:
                # Simulate reaching an intermediate location
                tracker.estimated_delivery_time = max(
                    0, tracker.estimated_delivery_time - segment_time
                )
                db.session.commit()

                print(
                    f"Tracker {tracker_id} reached intermediate location: {location}")
                print(f"Updated estimated delivery time for tracker {
                      tracker_id}: {tracker.estimated_delivery_time} minutes")
                time.sleep(10)  # Simulate delay for demonstration purposes

            # Mark tracker as DELIVERED after all locations are processed
            tracker.update_status(DeliveryStatus.DELIVERED)
            print(f"Tracker {tracker_id} marked as DELIVERED.")

        except Exception as e:
            print(f"Error simulating delivery progress for tracker {
                  tracker_id}: {e}")

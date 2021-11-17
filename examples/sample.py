from TrackZero import TrackZero, Entity
from datetime import datetime
from uuid import uuid4

trackZero_client = TrackZero("{your api key here}")

analytics_space_id = "python_example-space"

trackZero_client.create_analytics_space(analytics_space_id)

order = Entity("Orders", 712) \
            .add_attribute("Time", datetime.utcnow()) \
            .add_attribute("Total Amount", uuid4()) \
            .add_entity_reference_attribute("Items", "Products", 1) \
            .add_entity_reference_attribute("Items", "Products", 2) \
            .add_entity_reference_attribute("Order By", "Customers", 23)

trackZero_client.upsert_entity(order, analytics_space_id)

session = trackZero_client.create_analytics_space_session(analytics_space_id, 3600)

print(session.url)

# trackZero_client.delete_analytics_space(analytics_space_id)

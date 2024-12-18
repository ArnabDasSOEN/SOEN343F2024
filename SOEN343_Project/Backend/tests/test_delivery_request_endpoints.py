from .test_utils import create_address, create_package, create_delivery_request


def test_create_delivery_request_success(client):
    delivery_request_data = {
        "customer_id": 13,
        "pick_up_address": {
            "street": "123 Main St",
            "house_number": "123",
            "apartment_number": "2B",
            "postal_code": "12345",
            "city": "New York",
            "country": "USA"
        },
        "drop_off_address": {
            "street": "456 Elm St",
            "house_number": "456",
            "apartment_number": "4A",
            "postal_code": "67890",
            "city": "Los Angeles",
            "country": "USA"
        },
        "package": {
            "unit_system": "imperial",
            "width": 10,
            "length": 20,
            "height": 5,
            "weight": 30,
            "is_fragile": True,
            "package_items": [
                {
                    "item_description": "Glass Vase",
                    "quantity": 2,
                    "weight": 1.5
                },
                {
                    "item_description": "Fragile Sculpture",
                    "quantity": 1,
                    "weight": 2.0
                }
            ]
        }
    }

    response = client.post(
        '/delivery_request/create_delivery_request', json=delivery_request_data)
    data = response.get_json()

    assert response.status_code == 201
    assert data["message"] == "Delivery request and quotation created successfully"
    assert "delivery_request_id" in data
    assert "quotation_price" in data


def test_create_delivery_request_missing_fields(client):
    incomplete_data = {
        "customer_id": 13,  # Missing pick_up_address, drop_off_address, and package
    }

    response = client.post(
        '/delivery_request/create_delivery_request', json=incomplete_data)
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Missing required fields"


def test_create_delivery_request_invalid_customer_id(client):
    invalid_data = {
        "customer_id": "invalid_id",  # Should be an integer
        "pick_up_address": {
            "street": "123 Main St",
            "house_number": "123",
            "apartment_number": "2B",
            "postal_code": "12345",
            "city": "New York",
            "country": "USA"
        },
        "drop_off_address": {
            "street": "456 Elm St",
            "house_number": "456",
            "apartment_number": "4A",
            "postal_code": "67890",
            "city": "Los Angeles",
            "country": "USA"
        },
        "package": {
            "unit_system": "imperial",
            "width": 10,
            "length": 20,
            "height": 5,
            "weight": 30,
            "is_fragile": True,
            "package_items": [
                {
                    "item_description": "Glass Vase",
                    "quantity": 2,
                    "weight": 1.5
                }
            ]
        }
    }

    response = client.post(
        '/delivery_request/create_delivery_request', json=invalid_data)
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Invalid customer_id format"


def test_cancel_delivery_request_success(client):
    with client.application.app_context():
        # Use test_utils to create entities
        pick_up_address = create_address()
        drop_off_address = create_address()
        package = create_package()
        delivery_request = create_delivery_request(
            customer_id=13,
            pick_up_address_id=pick_up_address.id,
            drop_off_address_id=drop_off_address.id,
            package_id=package.id,
            status="Pending"
        )

        response = client.post('/delivery_request/cancel_delivery_request',
                               json={"delivery_request_id": delivery_request.id})
        data = response.get_json()

        assert response.status_code == 200
        assert data["message"] == "Delivery request cancelled successfully"


def test_cancel_delivery_request_invalid_id(client):
    response = client.post('/delivery_request/cancel_delivery_request',
                           json={"delivery_request_id": "invalid_id"})
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Invalid or missing delivery_request_id"


def test_cancel_delivery_request_not_found(client):
    response = client.post(
        '/delivery_request/cancel_delivery_request', json={"delivery_request_id": 999})
    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Delivery request not found"


def test_view_delivery_requests_success(client):
    with client.application.app_context():
        # Use test_utils to create entities
        pick_up_address = create_address()
        drop_off_address = create_address()
        package = create_package()
        delivery_request = create_delivery_request(
            customer_id=13,
            pick_up_address_id=pick_up_address.id,
            drop_off_address_id=drop_off_address.id,
            package_id=package.id,
            status="Pending"
        )

        response = client.post(
            '/delivery_request/view_delivery_requests', json={"user_id": 13})
        data = response.get_json()

        assert response.status_code == 200
        assert len(data) > 0
        assert data[0]["status"] == "Pending"


def test_view_delivery_requests_not_found(client):
    response = client.post(
        '/delivery_request/view_delivery_requests', json={"user_id": 13})
    data = response.get_json()

    assert response.status_code == 404
    assert data["message"] == "No delivery requests found for user_id 13"

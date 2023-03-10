from flask.testing import FlaskClient

def test_parameters(client : FlaskClient, app):
    new_parameters = {
        "T": 19.3,
        "H": 13.4,
        "Hb": 39.2,
    }
    response = client.patch("/api/parameters", json=new_parameters)
    assert response.status_code == 200
    assert app.config["settings"]["parameters"] == new_parameters

    new_parameters = {
        "T": 19,
        "H": 13,
        "Hb": 39,
    }
    response = client.patch("/api/parameters", json=new_parameters)
    assert response.status_code == 200
    assert app.config["settings"]["parameters"] == new_parameters

    new_parameters = {
        "T": 19,
        "H": 13,
        "Hb": 39.3,
    }
    response = client.patch("/api/parameters", json=new_parameters)
    assert response.status_code == 200
    assert app.config["settings"]["parameters"] == new_parameters

    new_parameters = {
        "T": 19.3,
        "H": 400,
        "Hb": 39.2,
    }
    response = client.patch("/api/parameters", json=new_parameters)
    assert response.status_code == 400

    new_parameters = {
        "T": 19.3,
        "H": 30.2,
        "Hb": 333,
    }
    response = client.patch("/api/parameters", json=new_parameters)
    assert response.status_code == 400

    new_parameters = {
        "T": 19.3,
        "H": "13.4",
        "Hb": 39.2,
    }
    response = client.patch("/api/parameters", json=new_parameters)
    assert response.status_code == 400

    new_parameters = {
        "T": 19.3,
        "Hb": 39.2,
    }
    response = client.patch("/api/parameters", json=new_parameters)
    assert response.status_code == 404

def test_state(client : FlaskClient, app):
    response = client.get("/api/state")

    assert response.status_code == 200
    assert response.get_json()["result"] == app.config["settings"]

def test_total_hum(client : FlaskClient, app):
    response = client.patch("/api/total_hum", json={
        "state": 1
    })
    assert response.status_code == 200

    response = client.patch("/api/total_hum", json={
        "state": 0
    })
    assert response.status_code == 200

    response = client.patch("/api/total_hum", json={
        "state": 2
    })
    assert response.status_code == 400

    response = client.patch("/api/total_hum", json={
        "state": None
    })
    assert response.status_code == 400

    response = client.patch("/api/total_hum", json={
        "state": "1"
    })
    assert response.status_code == 400

    response = client.patch("/api/total_hum", json={})
    assert response.status_code == 404

def test_fork_drive(client : FlaskClient, app):
    response = client.patch("/api/fork_drive", json={
        "state": 1
    })
    assert response.status_code == 200

    response = client.patch("/api/fork_drive", json={
        "state": 0
    })
    assert response.status_code == 200

    response = client.patch("/api/fork_drive", json={
        "state": 2
    })
    assert response.status_code == 400

    response = client.patch("/api/fork_drive", json={
        "state": None
    })
    assert response.status_code == 400

    response = client.patch("/api/fork_drive", json={})
    assert response.status_code == 404

def test_watering(client : FlaskClient, app):
    json = {
        "id": 1,
        "state": 1
    }
    response = client.patch("/api/watering", json=json)
    assert response.status_code == 200
    assert app.config["settings"]["watering"][0] == json["state"]

    json = {
        "id": 7
    }
    response = client.patch("/api/watering", json=json)
    assert response.status_code == 404

    json = {
        "id": 7,
        "state": None
    }
    response = client.patch("/api/watering", json=json)
    assert response.status_code == 400

    json = {
        "id": 7,
        "state": "1"
    }
    response = client.patch("/api/watering", json=json)
    assert response.status_code == 400

    json = {
        "id": 1,
        "state": 2
    }
    response = client.patch("/api/watering", json=json)
    assert response.status_code == 400

    json = {
        "id": 7,
        "state": 1
    }
    response = client.patch("/api/watering", json=json)
    assert response.status_code == 400

def test_emergency(client : FlaskClient, app):
    json = {
        "state": 1
    }
    response = client.patch("/api/emergency", json=json)
    assert response.status_code == 200

    json = {
        "state": 0
    }
    response = client.patch("/api/emergency", json=json)
    assert response.status_code == 200

    json = {
        "state": "1"
    }
    response = client.patch("/api/emergency", json=json)
    assert response.status_code == 400

    json = {
        "state_invalid": "1"
    }
    response = client.patch("/api/emergency", json=json)
    assert response.status_code == 404

    json = {}
    response = client.patch("/api/emergency", json=json)
    assert response.status_code == 404

def test_add_data(client : FlaskClient, app):
    json = {
        "air": [
            [13.2, 13.3],
            [13.2, 13.3],
            [13.2, 13.3],
            [13.2, 13.3]
        ],
        "ground": [13.2, 13.2, 13.2, 13.2, 13.2, 13.2]
    }
    response = client.post("/api/add_data", json=json)
    assert response.status_code == 200

    json = {
        "air": [
            [13, 13.3],
            [13, 13],
            [13.2, 13],
            [13.2, 13.3]
        ],
        "ground": [13.2, 13, 13, 13, 13.2, 13.2]
    }
    response = client.post("/api/add_data", json=json)
    assert response.status_code == 200

    json = {
        "air": [
            [13.2, 13.3],
            [13.2, 13.3],
            [13.2, 13.3],
            ["13.2", 13.3]
        ],
        "ground": [13.2, 13.2, 13.2, 13.2, 13.2, 13.2]
    }
    response = client.post("/api/add_data", json=json)
    assert response.status_code == 400

    json = {
        "air": [
            [13.2, 13.3],
            [13.2, 13.3],
            [13.2, 13.3],
            [13.2, 13.3]
        ],
        "ground": ["13.2", 13.2, 13.2, 13.2, 13.2, 13.2]
    }
    response = client.post("/api/add_data", json=json)
    assert response.status_code == 400

    json = {
        "air": [
            [13.2, 13.3],
            [13.2, 13.3],
            [13.2, 13.3]
        ],
        "ground": [13.2, 13.2, 13.2, 13.2, 13.2, 13.2]
    }
    response = client.post("/api/add_data", json=json)
    assert response.status_code == 400

    json = {
        "air": [
            [13.2, 13.3],
            [13.2, 13.3],
            [13.2, 13.3],
            [13.2, 13.3]
        ],
        "ground": [13.2, 13.2, 13.2, 13.2, 13.2]
    }
    response = client.post("/api/add_data", json=json)
    assert response.status_code == 400

    json = {
        "ground": [13.2, 13.2, 13.2, 13.2, 13.2, 13.2]
    }
    response = client.post("/api/add_data", json=json)
    assert response.status_code == 404

    json = {
        "air": [
            [13.2, 13.3],
            [13.2, 13.3],
            [13.2, 13.3]
        ]
    }
    response = client.post("/api/add_data", json=json)
    assert response.status_code == 404

def test_api_get_stores(test_client, populate_db):
    res = test_client.get("/api/")
    assert res.status_code == 200
    body = res.json
    assert body["stores"][0]["name"].startswith("A")
    assert body["stores"][-1]["name"].startswith("W")


def test_api_get_stores_empty_db(test_client):
    res = test_client.get("/api/")
    assert res.status_code == 200
    body = res.json
    assert len(body["stores"]) == 0


def test_api_get_stores_filter_missing(test_client):
    res = test_client.get("/api/filter/?postcode=&radius=")
    assert res.status_code == 400
    assert "Postcode is a required field" in res.json
    assert "Radius is a required field" in res.json


def test_api_get_stores_filter_invalid(test_client):
    res = test_client.get("/api/filter/?postcode=test&radius=test")
    assert res.status_code == 400
    assert "not a valid postcode" in res.json
    assert "not a valid radius" in res.json


def test_api_get_stores_filter(test_client, populate_db):
    # Tests with valid postcodes make an api call to postcodes.io
    # PostcodesClient should be mocked
    res = test_client.get("/api/filter/?postcode=CR0 4NX&radius=10")
    assert res.status_code == 200
    body = res.json
    assert len(body["stores"]) == 4
    assert body["stores"][0]["latitude"] > body["stores"][-1]["latitude"]


def test_api_get_stores_filter_none_found(test_client, populate_db):
    res = test_client.get("/api/filter/?postcode=YO8 6RA&radius=10")
    assert res.status_code == 200
    body = res.json
    assert len(body["stores"]) == 0

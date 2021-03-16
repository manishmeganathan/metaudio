"""
Functional Test Module for the /get endpoint of the AudioServer
Test Framework: pyTest
"""
import json
import random


def test_Create_Song(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** the create endpoint is hit with a POST request for creating a Song\n
    **THEN** check that the response is valid for a 200 response (OK), perform a get on the
    file that has been created, check its values and then delete the file.
    """
    # Create a Song file
    name = f"test-song-{random.randint(100,999)}"
    request = {"audioFileType": "Song", "audioFileMetadata": {"name": f"{name}", "duration": 45}}
    response = client.post(f"/create", json=request)

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert isinstance(data['status'], int)
    assert isinstance(data['message'], str)
    assert isinstance(data['result'], str)
    assert isinstance(data['document'], int)

    assert data['status'] == 200
    assert data['message'] == f"Create Complete"
    assert data['result'] == f"Song file with ID {data['document']} has been created"

    # Retrieve document and check its values
    response = client.get(f"/get/song/{data['document']}")

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    test_data = json.loads(response.data)

    assert test_data['documents'][0]['_id'] == data['document']
    assert test_data['documents'][0]['type'] == "Song"
    assert test_data['documents'][0]['name'] == name
    assert test_data['documents'][0]['duration'] == 45

    # Cleanup - Delete the added test file
    response = client.get(f"/delete/song/{data['document']}")
    assert response.status_code == 200


def test_Create_Podcast(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** the create endpoint is hit with a POST request for creating a Podcast\n
    **THEN** check that the response is valid for a 200 response (OK), perform a get on the
    file that has been created, check its values and then delete the file.
    """
    # Create a Podcast file
    name = f"test-podcast-{random.randint(100, 999)}"
    request = {"audioFileType": "Podcast",
               "audioFileMetadata": {"name": f"{name}", "duration": 45,
                                     "host": "host1", "participants": ["cast1"]}}
    response = client.post(f"/create", json=request)

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert isinstance(data['status'], int)
    assert isinstance(data['message'], str)
    assert isinstance(data['result'], str)
    assert isinstance(data['document'], int)

    assert data['status'] == 200
    assert data['message'] == f"Create Complete"
    assert data['result'] == f"Podcast file with ID {data['document']} has been created"

    # Retrieve document and check its values
    response = client.get(f"/get/podcast/{data['document']}")

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    test_data = json.loads(response.data)

    assert test_data['documents'][0]['_id'] == data['document']
    assert test_data['documents'][0]['type'] == "Podcast"
    assert test_data['documents'][0]['name'] == name
    assert test_data['documents'][0]['host'] == "host1"
    assert test_data['documents'][0]['participants'] == ["cast1"]
    assert test_data['documents'][0]['duration'] == 45

    # Cleanup - Delete the added test file
    response = client.get(f"/delete/podcast/{data['document']}")
    assert response.status_code == 200


def test_Create_Audiobook(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** the create endpoint is hit with a POST request for creating an Audiobook\n
    **THEN** check that the response is valid for a 200 response (OK), perform a get on the
    file that has been created, check its values and then delete the file.
    """
    # Create an Audiobook file
    name = f"test-book-{random.randint(100, 999)}"
    request = {"audioFileType": "Audiobook",
               "audioFileMetadata": {"name": f"{name}", "duration": 45,
                                     "author": "author1", "narrator": "narrator1"}}
    response = client.post(f"/create", json=request)

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert isinstance(data['status'], int)
    assert isinstance(data['message'], str)
    assert isinstance(data['result'], str)
    assert isinstance(data['document'], int)

    assert data['status'] == 200
    assert data['message'] == f"Create Complete"
    assert data['result'] == f"Audiobook file with ID {data['document']} has been created"

    # Retrieve document and check its values
    response = client.get(f"/get/audiobook/{data['document']}")

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    test_data = json.loads(response.data)

    assert test_data['documents'][0]['_id'] == data['document']
    assert test_data['documents'][0]['type'] == "Audiobook"
    assert test_data['documents'][0]['name'] == name
    assert test_data['documents'][0]['author'] == "author1"
    assert test_data['documents'][0]['narrator'] == "narrator1"
    assert test_data['documents'][0]['duration'] == 45

    # Cleanup - Delete the added test file
    response = client.get(f"/delete/audiobook/{data['document']}")
    assert response.status_code == 200


def test_Create_missing_key(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** the create endpoint is hit with a POST request with missing keys\n
    **THEN** check that the response is valid for a 400 response (OK)
    """
    # Test for missing 'audioFileMetadata'
    request = {"audioFileMetadata": {"name": "test-song", "duration": 45}}
    response = client.post(f"/create", json=request)

    assert response.status_code == 400
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert data['status'] == 400
    assert data['message'] == f"Bad Request"
    assert data['error'] == f"'audioFileType' is required"

    # Test for missing 'audioFileMetadata'
    request = {"audioFileType": "Song"}
    response = client.post(f"/create", json=request)

    assert response.status_code == 400
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert data['status'] == 400
    assert data['message'] == f"Bad Request"
    assert data['error'] == f"'audioFileMetadata' is required"


def test_Create_invalid_type(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** the create endpoint is hit with a POST request with an invalid 'audioFileType'\n
    **THEN** check that the response is valid for a 400 response (OK)
    """
    # Test for 'audioFileType' not an str
    request = {"audioFileType": 34, "audioFileMetadata": {"name": "test-song", "duration": 45}}
    response = client.post(f"/create", json=request)

    assert response.status_code == 400
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert data['status'] == 400
    assert data['message'] == f"Bad Request"
    assert data['error'] == f"'audioFileType' must be an str"

    # Test for unsupported 'audioFileType'
    request = {"audioFileType": "music", "audioFileMetadata": {"name": "test-song", "duration": 45}}
    response = client.post(f"/create", json=request)

    assert response.status_code == 400
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert data['status'] == 400
    assert data['message'] == f"Bad Request"
    assert data['error'] == f"'Music' is not supported"


def test_Create_invalid_metadata(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** the create endpoint is hit with a POST request with an invalid 'audioFileMetadata'\n
    **THEN** check that the response is valid for a 400 response (OK)
    """
    # Test for 'audioFileMetadata' not a dict
    request = {"audioFileType": "song", "audioFileMetadata": ["name", "test-song", "duration", 45]}
    response = client.post(f"/create", json=request)

    assert response.status_code == 400
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert data['status'] == 400
    assert data['message'] == f"Bad Request"
    assert data['error'] == f"'audioFileMetadata' must be a dict"


def test_Create_invalid_metadata_values(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** the create endpoint is hit with a POST request with invalid metadata values\n
    **THEN** check that the response is valid for a 400 response (OK)
    """
    # Test for invalid field in 'audioFileMetadata'
    request = {"audioFileType": "song", "audioFileMetadata": {"name": 33, "duration": 45}}
    response = client.post(f"/create", json=request)

    assert response.status_code == 400
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert data['status'] == 400
    assert data['message'] == f"Bad Request"
    assert data['error'] == f"metadata value is invalid for 'name' - not an str"

    # Test for missing field in 'audioFileMetadata'
    request = {"audioFileType": "song", "audioFileMetadata": {"duration": 45}}
    response = client.post(f"/create", json=request)

    assert response.status_code == 400
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert data['status'] == 400
    assert data['message'] == f"Bad Request"
    assert data['error'] == f"metadata value is missing for 'name'"


def test_Create_GET(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** the create endpoint is hit with a GET request\n
    **THEN** check that the response is valid for a 405 response (Method not Allowed)
    """
    response = client.get(f"/create")

    assert response.status_code == 405
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert isinstance(data['message'], str)
    assert data['message'] == f"The method is not allowed for the requested URL."


def test_Create_badURL(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** an invalid URL for the create endpoint is hit with a POST request\n
    **THEN** check that the response is valid for a 404 response (Not Found)
    """
    response = client.post(f"/create/")
    assert response.status_code == 404

    response = client.post(f"/create/234234")
    assert response.status_code == 404

    response = client.post(f"/create/something")
    assert response.status_code == 404

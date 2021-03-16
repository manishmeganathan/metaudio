"""
Functional Test Module for the /get endpoint of the AudioServer
Test Framework: pyTest
"""
import json


def test_Get_all_valid(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** a valid endpoint for retrieving all files of a type is hit with a GET request\n
    **THEN** check that the response is valid for a 200 response (OK)
    """
    for endpoint in ['song', 'Song', 'SONG', 'sONG', 'podcast', 'Podcast',
                     'PODCAST', 'audiobook', 'Audiobook', 'AUDIOBOOK']:

        response = client.get(f"/get/{endpoint}")

        assert response.status_code == 200
        assert isinstance(response.data, bytes)

        data = json.loads(response.data)

        assert isinstance(data['status'], int)
        assert isinstance(data['message'], str)
        assert isinstance(data['result'], str)
        assert isinstance(data['documents'], list)
        assert isinstance(data['matches'], int)

        assert data['status'] == 200
        assert data['message'] == f"Get Complete"
        assert data['result'] == f"{data['matches']} result(s) found"


def test_Get_one_valid(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** a valid endpoint for retrieving a file is hit with a GET request\n
    **THEN** check that the response is valid for a 200 response (OK)
    """
    for endpoint in ['Song', 'Podcast', 'Audiobook']:

        response = client.get(f"/get/{endpoint}")
        data = json.loads(response.data)

        IDs = [doc['_id'] for doc in data['documents']]

        for ID in IDs[:3]:
            response = client.get(f"/get/{endpoint}/{ID}")

            assert response.status_code == 200
            assert isinstance(response.data, bytes)

            data = json.loads(response.data)

            assert isinstance(data['status'], int)
            assert isinstance(data['message'], str)
            assert isinstance(data['result'], str)
            assert isinstance(data['documents'], list)
            assert isinstance(data['matches'], int)

            assert data['status'] == 200
            assert data['message'] == f"Get Complete"
            assert data['result'] == f"1 result(s) found"
            assert data['matches'] == 1

            assert data['documents'][0]['_id'] == ID
            assert data['documents'][0]['type'] == endpoint


def test_Get_all_invalid(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** an invalid endpoint for retrieving all files of a type is hit with a GET request\n
    **THEN** check that the response is valid for a 400 response (Bad Request)
    """
    for endpoint in ['sony', 'pod', 'audio']:
        response = client.get(f"/get/{endpoint}")

        assert response.status_code == 400
        assert isinstance(response.data, bytes)

        data = json.loads(response.data)

        assert isinstance(data['status'], int)
        assert isinstance(data['message'], str)
        assert isinstance(data['error'], str)

        assert data['status'] == 400
        assert data['message'] == f"Bad Request"
        assert data['error'] == f"'{endpoint.capitalize()}' is not supported"


def test_Get_all_POST(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** a valid endpoint for retrieving all files of a type is hit with a POST request\n
    **THEN** check that the response is valid for a 405 response (Method not Allowed)
    """
    for endpoint in ['song', 'podcast', 'audiobook']:
        response = client.post(f"/get/{endpoint}")

        assert response.status_code == 405
        assert isinstance(response.data, bytes)

        data = json.loads(response.data)

        assert isinstance(data['message'], str)
        assert data['message'] == f"The method is not allowed for the requested URL."


def test_Get_one_POST(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** a valid endpoint for retrieving a file is hit with a POST request\n
    **THEN** check that the response is valid for a 405 response (Method not Allowed)
    """
    for endpoint in ['Song', 'Podcast', 'Audiobook']:
        response = client.get(f"/get/{endpoint}")
        data = json.loads(response.data)

        IDs = [doc['_id'] for doc in data['documents']]

        for ID in IDs[:3]:
            response = client.post(f"/get/{endpoint}/{ID}")

            assert response.status_code == 405
            assert isinstance(response.data, bytes)

            data = json.loads(response.data)

            assert isinstance(data['message'], str)
            assert data['message'] == f"The method is not allowed for the requested URL."


def test_Get_badURL(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** an invalid URL for the get endpoint is hit with a GET request\n
    **THEN** check that the response is valid for a 404 response (Not Found)
    """
    response = client.get(f"/get")
    assert response.status_code == 404

    response = client.get(f"/get/")
    assert response.status_code == 404

    response = client.post(f"/get/song/something")
    assert response.status_code == 404

import pytest
from unittest.mock import Mock
from api.tahoe import TahoeClient

BASE_URL="http://127.0.0.1:3456/"
WELCOME_RESPONSE = b'{\n "introducers": {\n  "statuses": []\n },\n "servers": [\n  {\n   "nodeid": "v0-5cx26l27quxgeqzcq6hdez35zirk6ybir6zygzz5brl4e4jugsfq",\n   "connection_status": "Connected to tcp:localhost:41737 via tcp",\n   "available_space": 10559796736,\n   "nickname": "storage0",\n   "version": "tahoe-lafs/1.20.0",\n   "last_received_data": 1741634265.924307\n  }\n ]\n}\n'

@pytest.fixture
def mock_http():
    return Mock()

@pytest.fixture
def client(mock_http):
    return TahoeClient(base_url=BASE_URL, http=mock_http)

@pytest.fixture
def data_file():
    data_file = Mock()
    data_file.read.return_value = "test data"
    return data_file

# Client creation tests
def test_create_client_happy(client, mock_http):
    assert client.base_url == BASE_URL
    assert client.http is mock_http
    


def test_create_client_no_url(mock_http):
    with pytest.raises(TypeError) as e:
        client = TahoeClient(mock_http)
    
    error_message = str(e.value)

    assert "missing 1 required positional argument" in error_message
    assert "http" in error_message

def test_create_client_no_http():
    with pytest.raises(TypeError) as e:
        client = TahoeClient(BASE_URL)
    
    error_message = str(e.value)

    assert "missing 1 required positional argument" in error_message
    assert "http" in error_message

# Post data tests
def test_post_data_immutable_happy(client, mock_http):
    mock_response = Mock(status=200, data=b"cap_string")
    mock_http.request.return_value = mock_response

    result = client.post_data("test data")

    mock_http.request.assert_called_once_with("PUT", BASE_URL, "test data")
    assert result == "cap_string"


def test_post_data_mutable_happy(client, mock_http):
    mock_response = Mock(status=200, data=b"cap_string")
    mock_http.request.return_value = mock_response
    request_url = BASE_URL + "?format=SDMF"

    result = client.post_data("test data", mutable=True)

    mock_http.request.assert_called_once_with("PUT", request_url, "test data")
    assert result == "cap_string"

def test_post_data_bad_response(client, mock_http):
    mock_response = Mock(status=404)
    mock_http.request.return_value = mock_response
    
    result = client.post_data("test data")

    mock_http.request.assert_called_once_with("PUT", BASE_URL, "test data")
    assert result is None

def test_post_data_exception(client, mock_http):
    mock_http.request.side_effect = Exception()
    
    with pytest.raises(Exception):
        client.post_data("test data")

def test_post_data_dircap_happy(client, mock_http):
    mock_response = Mock(status=200, data=b"cap_string")
    mock_http.request.return_value = mock_response

    result = client.post_data("test data", dir_cap="$DIRCAP")

    mock_http.request.assert_called_once_with("PUT", BASE_URL+"$DIRCAP"+"/my_data.txt", "test data")
    assert result == "cap_string"

def test_post_data_dircap_bad_response(client, mock_http):
    mock_response = Mock(status=404)
    mock_http.request.return_value = mock_response
    
    result = client.post_data("test data", dir_cap="$DIRCAP")

    mock_http.request.assert_called_once_with("PUT", BASE_URL+"$DIRCAP"+"/my_data.txt", "test data")
    assert result is None

def test_post_data_dircap_exception(client, mock_http):
    mock_http.request.side_effect = Exception()
    
    with pytest.raises(Exception):
        client.post_data("test data", dir_cap="$DIRCAP")

def test_post_data_file_happy(client, mock_http, data_file):
    mock_response = Mock(status=200, data=b"cap_string")
    mock_http.request.return_value = mock_response

    result = client.post_data(data_file)

    data_file.read.assert_called_once()
    mock_http.request.assert_called_once_with("PUT", BASE_URL, "test data")
    assert result == "cap_string"

def test_post_data_file_bad_response(client, mock_http, data_file):
    mock_response = Mock(status=404)
    mock_http.request.return_value = mock_response

    result = client.post_data(data_file)

    data_file.read.assert_called_once()
    mock_http.request.assert_called_once_with("PUT", BASE_URL, "test data")
    assert result is None

def test_post_data_file_exception(client, mock_http, data_file):
    mock_http.request.side_effect = Exception()
    
    with pytest.raises(Exception):
        client.post_data(data_file)

def test_post_data_file_dircap_happy(client, mock_http, data_file):
    mock_response = Mock(status=200, data=b"cap_string")
    mock_http.request.return_value = mock_response

    result = client.post_data(data_file, dir_cap="$DIRCAP")

    mock_http.request.assert_called_once_with("PUT", BASE_URL+"$DIRCAP"+"/my_data.txt", "test data")
    assert result == "cap_string"

def test_post_data_file_dircap_bad_response(client, mock_http, data_file):
    mock_response = Mock(status=404)
    mock_http.request.return_value = mock_response
    
    result = client.post_data(data_file, dir_cap="$DIRCAP")

    mock_http.request.assert_called_once_with("PUT", BASE_URL+"$DIRCAP"+"/my_data.txt", "test data")
    assert result is None

def test_post_data_file_dircap_exception(client, mock_http, data_file):
    mock_http.request.side_effect = Exception()
    
    with pytest.raises(Exception):
        client.post_data(data_file, dir_cap="$DIRCAP")

# Get data tests
def test_get_data_happy(client, mock_http):
    mock_response = Mock(status=200, data=b"test data")
    mock_http.request.return_value = mock_response

    result = client.get_data("cap_string")

    mock_http.request.assert_called_once_with("GET", BASE_URL+"cap_string")
    assert result[0] == "test data"
    assert result[1] == 200

def test_get_data_bad_response(client, mock_http):
    mock_response = Mock(status=404)
    mock_http.request.return_value = mock_response

    result = client.get_data("cap_string")

    mock_http.request.assert_called_once_with("GET", BASE_URL+"cap_string")
    assert result[0] is None
    assert result[1] == 404

def test_get_data_dircap_happy(client, mock_http):
    mock_response = Mock(status=200, data=b"test data")
    mock_http.request.return_value = mock_response

    result = client.get_data("cap_string", dir_cap="$DIRCAP")

    mock_http.request.assert_called_once_with("GET", BASE_URL+"$DIRCAP/my_data.txt")
    assert result[0] == "test data"
    assert result[1] == 200

def test_get_data_dircap_bad_response(client, mock_http):
    mock_response = Mock(status=404)
    mock_http.request.return_value = mock_response

    result = client.get_data("cap_string", dir_cap="$DIRCAP")

    mock_http.request.assert_called_once_with("GET", BASE_URL+"$DIRCAP/my_data.txt")
    assert result[0] is None
    assert result[1] == 404

# Put data tests
def test_put_data_happy(client, mock_http):
    mock_create_response = Mock(status=201, data=b"cap_string")
    mock_http.request.return_value = mock_create_response

    cap_string = client.post_data('testdata', mutable=True)

    mock_update_response = Mock(status=200, data=b"cap_string")
    mock_http.request.return_value = mock_update_response

    client.put_data('datatest', cap_string=cap_string)
    mock_http.request.return_value = Mock(status=200, data=b'datatest')
    get_update_result = client.get_data(cap_string)

    assert get_update_result[0] == 'datatest'
    assert get_update_result[1] == 200

def test_put_data_file_happy(client, mock_http, data_file):
    mock_create_response = Mock(status=201, data=b"cap_string")
    mock_http.request.return_value = mock_create_response

    cap_string = client.post_data(data_file, mutable=True)

    mock_update_response = Mock(status=200, data=b"cap_string")
    mock_http.request.return_value = mock_update_response
    new_data_file = Mock()
    new_data_file.read.return_value = "datatest"

    client.put_data(new_data_file, cap_string=cap_string)
    mock_http.request.return_value = Mock(status=200, data=b'datatest')
    get_update_result = client.get_data(cap_string)

    assert get_update_result[0] == 'datatest'
    assert get_update_result[1] == 200


# Make dir tests
def test_make_dir_happy(client, mock_http):
    mock_response = Mock(status=200, data=b"$DIRCAP")
    mock_http.request.return_value = mock_response

    result = client.make_dir()

    mock_http.request.assert_called_once_with("POST", BASE_URL[:-1]+"?t=mkdir")
    assert result == "$DIRCAP"

def test_make_dir_bad_response(client, mock_http):
    mock_response = Mock(status=404)
    mock_http.request.return_value = mock_response

    result = client.make_dir()

    mock_http.request.assert_called_once_with("POST", BASE_URL[:-1]+"?t=mkdir")
    assert result is None

def test_make_dir_exception(client, mock_http):
    mock_http.request.side_effect = Exception()
    
    with pytest.raises(Exception):
        client.make_dir()


# Get welcome tests
def test_get_welcome_happy(client, mock_http):
    mock_response = Mock(status=200, data=WELCOME_RESPONSE)
    mock_http.request.return_value = mock_response

    result = client.get_welcome()

    mock_http.request.assert_called_once_with("GET", BASE_URL+"?t=json")
    assert result.status == 200
    assert result.data == WELCOME_RESPONSE

def test_get_welcome_exception(client, mock_http):
    mock_http.request.side_effect = Exception()
    
    with pytest.raises(Exception):
        client.get_welcome()
import requests


def test_case(init_test_case, api_server_addr):
    print(f"test [api-server] {api_server_addr}")
    response = requests.get(api_server_addr + "/", timeout=1)
    assert response.status_code == 200
    assert response.json().get("message") == "Hello from [api-server]!"

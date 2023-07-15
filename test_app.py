import app

def test_index():
    response = app.get("/")
    assert response.status_code == 200
    assert response.content == "Hello, world!"

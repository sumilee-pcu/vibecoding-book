from app import app, todos


def setup_function():
    todos.clear()


def client():
    return app.test_client()


def test_empty_list():
    res = client().get("/api/todos")
    assert res.status_code == 200
    assert res.get_json() == []


def test_add_todo():
    res = client().post("/api/todos", json={"title": "원고 마감"})
    assert res.status_code == 201
    body = res.get_json()
    assert body["title"] == "원고 마감"
    assert body["done"] is False


def test_add_todo_with_priority():
    res = client().post("/api/todos", json={"title": "교정", "priority": "높음"})
    assert res.get_json()["priority"] == "높음"


def test_toggle_done():
    c = client()
    todo = c.post("/api/todos", json={"title": "탈고"}).get_json()
    res = c.post(f"/api/todos/{todo['id']}/toggle")
    assert res.status_code == 200
    assert res.get_json()["done"] is True


def test_delete_todo():
    c = client()
    todo = c.post("/api/todos", json={"title": "임시"}).get_json()
    res = c.delete(f"/api/todos/{todo['id']}")
    assert res.status_code == 200
    assert c.get("/api/todos").get_json() == []


def test_delete_missing_returns_404():
    res = client().delete("/api/todos/999")
    assert res.status_code == 404

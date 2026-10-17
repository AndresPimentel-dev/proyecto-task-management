def test_health_check(cliente):
    response = cliente.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "working"


##############################################################################################
# TESTS AUTHENTICATION ENDPOINTS
##############################################################################################


def test_endpoint_register(cliente):
    response = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )

    assert response.status_code == 201
    assert response.json()["token_type"] == "bearer"


def test_endpoint_login(cliente):
    cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    response = cliente.post(
        "/api/v1.0/auth/login",
        data={"username": "fakeusername", "password": "fakepassword"},
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_register_duplicated_username(cliente):
    cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    response = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    assert response.status_code == 409


def test_invalid_email(cliente):
    response = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "invalidemail",
            "password": "fakepassword",
        },
    )
    assert response.status_code == 422


def test_post_invalid_data(cliente):
    cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    response = cliente.post("/api/v1.0/auth/register", json={"data": "invalid_data"})
    assert response.status_code == 422


def test_incorrect_password(cliente):
    cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    response = cliente.post(
        "/api/v1.0/auth/login",
        data={"username": "fakeusername", "password": "contrasenaincorrecta"},
    )

    assert response.status_code == 401


def test_non_existent_user(cliente):
    cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    response = cliente.post(
        "/api/v1.0/auth/login",
        data={"username": "non_existentusername", "password": "contrasenaincorrecta"},
    )

    assert response.status_code == 401


def test_login_inexinting_user(cliente):
    response = cliente.post(
        "/api/v1.0/auth/login",
        data={"username": "fakeusername", "password": "fakepassword"},
    )
    assert response.status_code == 401


def test_duplicated_email(cliente):
    cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    response = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusernamenew",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    assert response.status_code == 409


#############################################################################################
# TESTS WORKSPACE ENDPOINTS
#############################################################################################
def test_endpoint_create_workspace(cliente):
    peyload = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    access_token = peyload.json()["access_token"]
    response = cliente.post(
        "/api/v1.0/workspaces",
        json={
            "name": "fakenombre",
            "description": "fakedescriopansd",
            "created_at": "2026-06-25",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 201
    assert response.json() is not None
    assert response.json()["name"] == "fakenombre"


def test_get_workspaces(cliente):
    peyload_registrarse = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )

    access_token = peyload_registrarse.json()["access_token"]
    cliente.post(
        "/api/v1.0/workspaces",
        json={
            "name": "fakenombre",
            "description": "fakedescriopansd",
            "created_at": "2026-06-25",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response = cliente.get(
        "/api/v1.0/workspaces", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json() is not None
    assert isinstance(response.json()["workspaces"], list)


def test_delete_workspace(cliente):
    peyload_registrarse = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    access_token = peyload_registrarse.json()["access_token"]
    workspace = cliente.post(
        "/api/v1.0/workspaces",
        json={
            "name": "fakenombre",
            "description": "fakedescription",
            "created_at": "2026-06-25",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response = cliente.delete(
        f"/api/v1.0/workspaces/{workspace.json()['id']}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 204


def test_get_workspaces_by_id(cliente):
    registrarse = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    access_token = registrarse.json()["access_token"]
    workspace = cliente.post(
        "/api/v1.0/workspaces",
        json={
            "name": "fakenombre",
            "description": "fakedescription",
            "created_at": "2026-06-25",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    payload = cliente.get(
        f"/api/v1.0/workspaces/{workspace.json()['id']}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert payload is not None
    assert payload.status_code == 200
    assert payload.json()["name"] == "fakenombre"
    assert payload.json()["description"] == "fakedescription"


def test_update_workspaces(cliente):
    registrarse = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    access_token = registrarse.json()["access_token"]
    workspace = cliente.post(
        "/api/v1.0/workspaces",
        json={
            "name": "fakenombre",
            "description": "fakedescription",
            "created_at": "2026-06-25",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    payload = cliente.put(
        f"/api/v1.0/workspaces/{workspace.json()['id']}",
        json={
            "name": "fakenewnombre",
            "description": "fakenewdescripcion",
            "created_at": "2026-06-25",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert payload.json()["description"] == "fakenewdescripcion"
    assert payload is not None
    assert payload.status_code == 200


def test_create_workspace_without_token(cliente):
    response = cliente.post(
        "/api/v1.0/workspaces",
        json={
            "name": "fakenombre",
            "description": "fakedescripcion",
            "created_at": "2026-06-25",
        },
    )

    assert response.status_code == 401


def test_get_workspaces_without_token(cliente):
    response = cliente.get("/api/v1.0/workspaces")

    assert response.status_code == 401


def test_get_non_existing_workspace(cliente):
    peyload_register = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    access_token = peyload_register.json()["access_token"]
    cliente.post(
        "/api/v1.0/workspaces",
        json={
            "username": "fakenombre",
            "description": "fakedescription",
            "created_at": "2026-06-25",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response = cliente.get(
        f"/api/v1.0/workspaces{9999}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404


def test_userA_cannot_delete_userB_workspace(cliente):
    usuarioA = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    tokenusuarioA = usuarioA.json()["access_token"]
    usuarioB = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusernameusuarioB",
            "email": "fakeemailusuarioB@gmail.com",
            "password": "fakepassword",
        },
    )
    tokenUsuarioB = usuarioB.json()["access_token"]
    workspaceUsuarioB = cliente.post(
        "/api/v1.0/workspaces",
        json={
            "name": "fakenombre",
            "description": "fakedescription",
            "created_at": "2026-06-25",
        },
        headers={"Authorization": f"Bearer {tokenUsuarioB}"},
    )
    response = cliente.delete(
        f"/api/v1.0/workspaces/{workspaceUsuarioB.json()['id']}",
        headers={"Authorization": f"Bearer {tokenusuarioA}"},
    )
    assert response.status_code == 404


def test_delete_non_existing_workspace(cliente):
    peyload_register = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )

    access_token = peyload_register.json()["access_token"]
    response = cliente.delete(
        f"/api/v1.0/workspaces/{9999999}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404


def test_userA_cannot_get_userB_workspace(cliente):
    usuarioA = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    tokenusuarioA = usuarioA.json()["access_token"]
    usuarioB = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusernameusuarioB",
            "email": "fakeemailusuarioB@gmail.com",
            "password": "fakepassword",
        },
    )
    tokenUsuarioB = usuarioB.json()["access_token"]
    workspaceUsuarioB = cliente.post(
        "/api/v1.0/workspaces",
        json={
            "name": "fakenombre",
            "description": "fakedescription",
            "created_at": "2026-06-25",
        },
        headers={"Authorization": f"Bearer {tokenUsuarioB}"},
    )
    UsuarioA_payload = cliente.get(
        f"/api/v1.0/workspaces{workspaceUsuarioB.json()['id']}",
        headers={"Authorization": f"Bearer {tokenusuarioA}"},
    )
    assert UsuarioA_payload.status_code == 404


def test_userA_cannor_update_userB_workspace(cliente):
    usuarioA = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    tokenusuarioA = usuarioA.json()["access_token"]
    usuarioB = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusernameusuarioB",
            "email": "fakeemailusuarioB@gmail.com",
            "password": "fakepassword",
        },
    )
    tokenUsuarioB = usuarioB.json()["access_token"]
    workspaceUsuarioB = cliente.post(
        "/api/v1.0/workspaces",
        json={
            "name": "fakenombre",
            "description": "fakedescription",
            "created_at": "2026-06-25",
        },
        headers={"Authorization": f"Bearer {tokenUsuarioB}"},
    )
    response = cliente.put(
        f"/api/v1.0/workspaces{workspaceUsuarioB.json()['id']}",
        json={
            "username": "fakenewnombre",
            "deadline": "2027-09-29",
            "description": "fakenewdescripcion",
            "created_at": "2026-06-25",
        },
        headers={"Authorization": f"Bearer {tokenusuarioA}"},
    )
    assert response.status_code == 404


def test_invalid__workspace_token(cliente):
    token_falso = "tokenfalsoparatestdeaopi"
    response = cliente.get(
        "/api/v1.0/workspaces", headers={"Authorization": f"Bearer {token_falso}"}
    )

    assert response.status_code == 401


def test_user_without_workspaces(cliente):
    peyload = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )

    access_token = peyload.json()["access_token"]

    response = cliente.get(
        "/api/v1.0/workspaces", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.json()["workspaces"] == []


#############################################################################################
# TESTS TASKS ENDPOINTS
#############################################################################################


def test_endpoint_create_task(cliente):
    peyload = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    access_token = peyload.json()["access_token"]
    workspace = cliente.post(
        "/api/v1.0/workspaces",
        json={
            "name": "fakenombre",
            "description": "fakedescriopansd",
            "created_at": "2026-02-25",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    response = cliente.post(
        "/api/v1.0/tasks",
        json={
            "title": "fakenombre",
            "description": "fakedescription",
            "created_at": "2026-02-25",
            "status": "todo",
            "workspace_id": int(workspace.json()["id"]),
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    assert response.json() is not None
    assert response.json()["title"] == "fakenombre"


def test_get_tasks(cliente):
    peyload_registrarse = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )

    access_token = peyload_registrarse.json()["access_token"]
    workspace = cliente.post(
        "/api/v1.0/workspaces",
        json={
            "name": "fakenombre",
            "description": "fakedescriopansd",
            "created_at": "2026-06-25",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    cliente.post(
        "/api/v1.0/tasks",
        json={
            "title": "fakenombre",
            "description": "fakedescription",
            "created_at": "2026-02-25",
            "status": "todo",
            "workspace_id": int(workspace.json()["id"]),
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response = cliente.get(
        "/api/v1.0/tasks", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json() is not None
    assert isinstance(response.json()["tasks"], list)


def test_delete_tasks(cliente):
    peyload_registrarse = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    access_token = peyload_registrarse.json()["access_token"]

    workspace = cliente.post(
        "/api/v1.0/workspaces",
        json={
            "name": "fakenombre",
            "description": "fakedescriopansd",
            "created_at": "2026-06-25",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    tarea = cliente.post(
        "/api/v1.0/tasks",
        json={
            "title": "fakenombre",
            "description": "fakedescription",
            "created_at": "2026-02-25",
            "status": "todo",
            "workspace_id": int(workspace.json()["id"]),
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response = cliente.delete(
        f"/api/v1.0/tasks/{tarea.json()['id']}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 204


def test_get_tasks_by_id(cliente):
    registrarse = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    access_token = registrarse.json()["access_token"]
    workspace = cliente.post(
        "/api/v1.0/workspaces",
        json={
            "name": "fakenombre",
            "description": "fakedescriopansd",
            "created_at": "2026-06-25",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    tarea = cliente.post(
        "/api/v1.0/tasks",
        json={
            "title": "fakenombre",
            "description": "fakedescription",
            "created_at": "2026-02-25",
            "status": "todo",
            "workspace_id": int(workspace.json()["id"]),
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    payload = cliente.get(
        f"/api/v1.0/tasks/{tarea.json()['id']}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert payload is not None
    assert payload.status_code == 200
    assert payload.json()["title"] == "fakenombre"
    assert payload.json()["status"] == "todo"


def test_update_tasks(cliente):
    registrarse = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )

    access_token = registrarse.json()["access_token"]
    workspace = cliente.post(
        "/api/v1.0/workspaces",
        json={
            "name": "fakenombre",
            "description": "fakedescriopansd",
            "created_at": "2026-06-25",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    tarea = cliente.post(
        "/api/v1.0/tasks",
        json={
            "title": "fakenombre",
            "description": "fakedescription",
            "created_at": "2026-02-25",
            "status": "todo",
            "workspace_id": int(workspace.json()["id"]),
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    payload = cliente.put(
        f"/api/v1.0/tasks/{tarea.json()['id']}",
        json={
            "title": "fakenewnombre",
            "description": "fakenewdescription",
            "created_at": "2026-02-25",
            "status": "todo",
            "workspace_id": int(workspace.json()["id"]),
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert payload.json()["description"] == "fakenewdescription"
    assert payload is not None
    assert payload.status_code == 200


def test_create_task_without_token(cliente):
    tarea = cliente.post(
        "/api/v1.0/tasks",
        json={
            "title": "fakenombre",
            "description": "fakedescription",
            "created_at": "2026-02-25",
            "status": "todo",
            "workspace_id": 1,
        },
    )

    assert tarea.status_code == 401


def test_get_tasks_without_token(cliente):
    response = cliente.get("/api/v1.0/tasks")

    assert response.status_code == 401


def test_get_non_existing_tasks(cliente):
    peyload_register = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    access_token = peyload_register.json()["access_token"]

    response = cliente.get(
        f"/api/v1.0/tasks/{9999}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404


def test_userA_cannot_delete_userB_tasks(cliente):
    usuarioA = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    tokenusuarioA = usuarioA.json()["access_token"]

    usuarioB = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusernameusuarioB",
            "email": "fakeemailusuarioB@gmail.com",
            "password": "fakepassword",
        },
    )
    tokenUsuarioB = usuarioB.json()["access_token"]
    workspace = cliente.post(
        "/api/v1.0/workspaces",
        json={
            "name": "fakenombre",
            "description": "fakedescriopansd",
            "created_at": "2026-06-25",
        },
        headers={"Authorization": f"Bearer {tokenUsuarioB}"},
    )
    tasksauserB = cliente.post(
        "/api/v1.0/tasks",
        json={
            "title": "fakenombre",
            "description": "fakedescription",
            "created_at": "2026-02-25",
            "status": "todo",
            "workspace_id": int(workspace.json()["id"]),
        },
        headers={"Authorization": f"Bearer {tokenUsuarioB}"},
    )
    response = cliente.delete(
        f"/api/v1.0/tasks/{tasksauserB.json()['id']}",
        headers={"Authorization": f"Bearer {tokenusuarioA}"},
    )
    assert response.status_code == 404


def test_delete_non_existing_task(cliente):
    peyload_register = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )

    access_token = peyload_register.json()["access_token"]

    response = cliente.delete(
        f"/api/v1.0/tasks/{9999999}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404


def test_userA_cannot_get_userB_task(cliente):
    usuarioA = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    tokenusuarioA = usuarioA.json()["access_token"]
    usuarioB = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusernameusuarioB",
            "email": "fakeemailusuarioB@gmail.com",
            "password": "fakepassword",
        },
    )
    tokenUsuarioB = usuarioB.json()["access_token"]
    workspace = cliente.post(
        "/api/v1.0/workspaces",
        json={
            "name": "fakenombre",
            "description": "fakedescriopansd",
            "created_at": "2026-06-25",
        },
        headers={"Authorization": f"Bearer {tokenUsuarioB}"},
    )
    tasksauserB = cliente.post(
        "/api/v1.0/tasks",
        json={
            "title": "fakenombre",
            "description": "fakedescription",
            "created_at": "2026-02-25",
            "status": "todo",
            "workspace_id": int(workspace.json()["id"]),
        },
        headers={"Authorization": f"Bearer {tokenUsuarioB}"},
    )
    UsuarioA_payload = cliente.get(
        f"/api/v1.0/workspaces/{tasksauserB.json()['id']}",
        headers={"Authorization": f"Bearer {tokenusuarioA}"},
    )
    assert UsuarioA_payload.status_code == 404


def test_userA_cannor_update_userB_tasks(cliente):
    usuarioA = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )
    tokenusuarioA = usuarioA.json()["access_token"]

    usuarioB = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusernameusuarioB",
            "email": "fakeemailusuarioB@gmail.com",
            "password": "fakepassword",
        },
    )
    tokenUsuarioB = usuarioB.json()["access_token"]
    workspace = cliente.post(
        "/api/v1.0/workspaces",
        json={
            "name": "fakenombre",
            "description": "fakedescriopansd",
            "created_at": "2026-06-25",
        },
        headers={"Authorization": f"Bearer {tokenUsuarioB}"},
    )
    tasksauserB = cliente.post(
        "/api/v1.0/tasks",
        json={
            "title": "fakenombre",
            "description": "fakedescription",
            "created_at": "2026-02-25",
            "status": "todo",
            "workspace_id": int(workspace.json()["id"]),
        },
        headers={"Authorization": f"Bearer {tokenUsuarioB}"},
    )

    response = cliente.put(
        f"/api/v1.0/workspaces{tasksauserB.json()['id']}",
        json={
            "username": "fakenewnombre",
            "deadline": "2027-09-29",
            "description": "fakenewdescripcion",
        },
        headers={"Authorization": f"Bearer {tokenusuarioA}"},
    )
    assert response.status_code == 404


def test_invalid_task_token(cliente):

    token_falso = "tokenfalsoparatestdeaopi"

    response = cliente.get(
        "/api/v1.0/tasks", headers={"Authorization": f"Bearer {token_falso}"}
    )

    assert response.status_code == 401


def test_user_without_tasks(cliente):
    peyload = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "fakeusername",
            "email": "fakeemail@gmail.com",
            "password": "fakepassword",
        },
    )

    access_token = peyload.json()["access_token"]

    response = cliente.get(
        "/api/v1.0/tasks", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.json()["tasks"] == []


def test_cannot_create_task_in_other_user_workspace(cliente):
    # Registrar Usuario A y crear workspace
    res_a = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "usera",
            "email": "usera@example.com",
            "password": "password123",
        },
    )
    token_a = res_a.json()["access_token"]
    ws_res = cliente.post(
        "/api/v1.0/workspaces",
        json={"name": "Workspace A", "description": "Desc A"},
        headers={"Authorization": f"Bearer {token_a}"},
    )
    workspace_a_id = ws_res.json()["id"]

    # Registrar Usuario B
    res_b = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "userb",
            "email": "userb@example.com",
            "password": "password123",
        },
    )
    token_b = res_b.json()["access_token"]

    # Usuario B intenta crear una tarea en el workspace de Usuario A (IDOR)
    task_res = cliente.post(
        "/api/v1.0/tasks",
        json={
            "title": "Hacked Task",
            "description": "Trying to write to another user workspace",
            "status": "todo",
            "workspace_id": workspace_a_id,
        },
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert task_res.status_code == 404


def test_delete_workspace_cascades_tasks(cliente):
    res = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "cascadeuser",
            "email": "cascade@example.com",
            "password": "password123",
        },
    )
    token = res.json()["access_token"]

    ws_res = cliente.post(
        "/api/v1.0/workspaces",
        json={"name": "Cascade WS", "description": "To be deleted"},
        headers={"Authorization": f"Bearer {token}"},
    )
    ws_id = ws_res.json()["id"]

    # Crear tarea en el workspace
    cliente.post(
        "/api/v1.0/tasks",
        json={
            "title": "Task in WS",
            "description": "Will be cascaded",
            "status": "todo",
            "workspace_id": ws_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    # Eliminar workspace
    del_res = cliente.delete(
        f"/api/v1.0/workspaces/{ws_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert del_res.status_code == 204

    # Las tareas del usuario deben quedar vacías
    tasks_res = cliente.get(
        "/api/v1.0/tasks",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert tasks_res.json()["tasks"] == []


def test_update_task_partial_status(cliente):
    res = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "updateuser",
            "email": "update@example.com",
            "password": "password123",
        },
    )
    token = res.json()["access_token"]

    ws_res = cliente.post(
        "/api/v1.0/workspaces",
        json={"name": "Update WS", "description": "WS Desc"},
        headers={"Authorization": f"Bearer {token}"},
    )
    ws_id = ws_res.json()["id"]

    task_res = cliente.post(
        "/api/v1.0/tasks",
        json={
            "title": "Original Title",
            "description": "Original Desc",
            "status": "todo",
            "workspace_id": ws_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    task_id = task_res.json()["id"]

    # Actualizar solo el estado
    put_res = cliente.put(
        f"/api/v1.0/tasks/{task_id}",
        json={"status": "completed"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert put_res.status_code == 200
    assert put_res.json()["status"] == "completed"
    assert put_res.json()["title"] == "Original Title"


def test_filter_tasks_by_workspace(cliente):
    res = cliente.post(
        "/api/v1.0/auth/register",
        json={
            "username": "filteruser",
            "email": "filter@example.com",
            "password": "password123",
        },
    )
    token = res.json()["access_token"]

    ws1 = cliente.post(
        "/api/v1.0/workspaces",
        json={"name": "WS1", "description": "Desc1"},
        headers={"Authorization": f"Bearer {token}"},
    ).json()["id"]

    ws2 = cliente.post(
        "/api/v1.0/workspaces",
        json={"name": "WS2", "description": "Desc2"},
        headers={"Authorization": f"Bearer {token}"},
    ).json()["id"]

    cliente.post(
        "/api/v1.0/tasks",
        json={
            "title": "Task 1",
            "description": "In WS1",
            "status": "todo",
            "workspace_id": ws1,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    cliente.post(
        "/api/v1.0/tasks",
        json={
            "title": "Task 2",
            "description": "In WS2",
            "status": "todo",
            "workspace_id": ws2,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    # Filtrar por ws1
    res_filter = cliente.get(
        f"/api/v1.0/tasks?workspace_id={ws1}",
        headers={"Authorization": f"Bearer {token}"},
    )
    tasks = res_filter.json()["tasks"]
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Task 1"

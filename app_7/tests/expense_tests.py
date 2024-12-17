def test_no_expenses_list(test_client, init_database, second_user_token):
    response = test_client.get(
        "/expenses/",
        headers={"Authorization": f"Bearer {second_user_token}"},
    )

    assert response.status_code == 200
    assert response.json == []


def test_expenses_list(test_client, init_database, default_user_token):
    response = test_client.get(
        "/expenses/",
        headers={"Authorization": f"Bearer {default_user_token}"},
    )

    assert response.status_code == 200
    assert len(response.json) > 0


def test_full_expense_flow(test_client, init_database, default_user_token):
    created_expense_res = test_client.post(
        "/expenses/",
        json={
            "title": "Expense",
            "amount": 100,
        },
        headers={"Authorization": f"Bearer {default_user_token}"},
    )
    assert created_expense_res.status_code == 201
    assert created_expense_res.json["title"] == "Expense"

    created_expense_res_id = created_expense_res.json["id"]

    received_expense_res = test_client.get(
        f"/expenses/{created_expense_res_id}",
        headers={"Authorization": f"Bearer {default_user_token}"},
    )
    assert received_expense_res.status_code == 200
    assert received_expense_res.json["title"] == "Expense"

    updated_expense_res = test_client.patch(
        f"/expenses/{created_expense_res_id}",
        json={
            "title": "Updated Expense",
        },
        headers={"Authorization": f"Bearer {default_user_token}"},
    )
    assert updated_expense_res.status_code == 200
    assert updated_expense_res.json["title"] == "Updated Expense"

    deleted_expense_res = test_client.delete(
        f"/expenses/{created_expense_res_id}",
        headers={"Authorization": f"Bearer {default_user_token}"},
    )
    assert deleted_expense_res.status_code == 204
    assert deleted_expense_res.json == None

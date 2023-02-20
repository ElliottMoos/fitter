import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.models.models import StoreRead


def test_non_lead_fitter_cannot_delete_stores(
    app: FastAPI,
    expert_client: TestClient,
    test_store: StoreRead,
):
    response = expert_client.get(
        app.url_path_for("store-delete:delete-store", store_id=test_store.id)
    )
    assert response.status_code == 403


def test_lead_fitter_can_delete_stores(
    app: FastAPI,
    lead_client: TestClient,
    test_store: StoreRead,
):
    response = lead_client.get(
        app.url_path_for("store-delete:delete-store", store_id=test_store.id)
    )
    # This route redirects the user to the stores
    # page on success
    assert response.status_code == 307

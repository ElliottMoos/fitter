import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_non_lead_fitter_cannot_access_create_fitter_page(
    app: FastAPI,
    expert_client: TestClient,
):
    response = expert_client.get(app.url_path_for("fitter-create:create-fitter-page"))
    assert response.status_code == 403


def test_lead_fitter_can_access_create_fitter_page(
    app: FastAPI,
    lead_client: TestClient,
):
    response = lead_client.get(app.url_path_for("fitter-create:create-fitter-page"))
    assert response.status_code == 200

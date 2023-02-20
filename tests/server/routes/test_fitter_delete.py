import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.models.models import FitterRead


def test_non_lead_fitter_cannot_delete_fitters(
    app: FastAPI,
    expert_client: TestClient,
    test_lead_fitter: FitterRead,
):
    response = expert_client.get(
        app.url_path_for("fitter-delete:delete-fitter", fitter_id=test_lead_fitter.id)
    )
    assert response.status_code == 403


def test_lead_fitter_can_delete_fitters(
    app: FastAPI,
    lead_client: TestClient,
    test_expert_fitter: FitterRead,
):
    response = lead_client.get(
        app.url_path_for("fitter-delete:delete-fitter", fitter_id=test_expert_fitter.id)
    )
    # This route redirects the user to the fitters
    # page on success
    assert response.status_code == 307

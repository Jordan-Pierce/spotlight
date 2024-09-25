"""
    Tests for the renumics spotlight app and in mem data frame serving
"""

import json
from typing import Any, List
import os
import tempfile

import requests

from renumics import spotlight


def _column_by_name(columns: List, col_name: str) -> Any:
    return [col for col in columns if col["name"] == col_name][0]


def test_read_table(viewer_csv_df: spotlight.Viewer) -> None:
    """test full table can be read an returns data"""

    app_url = f"http://{viewer_csv_df.host}:{viewer_csv_df.port}"

    response = requests.get(app_url + "/api/table/", timeout=5)
    assert response.status_code == 200
    assert len(response.text) > 1000
    json_data = json.loads((response.text))
    assert _column_by_name(json_data["columns"], "bool")["dtype"]["name"] == "bool"
    assert _column_by_name(json_data["columns"], "float")["dtype"]["name"] == "float"
    assert _column_by_name(json_data["columns"], "audio")["dtype"]["name"] == "Audio"
    assert (
        _column_by_name(json_data["columns"], "embedding")["dtype"]["name"]
        == "Embedding"
    )
    assert _column_by_name(json_data["columns"], "video")["dtype"]["name"] == "Video"


def test_save_dataframe(viewer_csv_df: spotlight.Viewer) -> None:
    """test saving the dataframe to a specified file format"""

    app_url = f"http://{viewer_csv_df.host}:{viewer_csv_df.port}"

    with tempfile.TemporaryDirectory() as temp_dir:
        save_path = os.path.join(temp_dir, "saved_dataframe.csv")
        response = requests.post(
            app_url + "/save_dataframe",
            json={"path": save_path, "file_format": "csv"},
            timeout=5,
        )
        assert response.status_code == 200
        assert response.json()["detail"] == "Dataframe saved successfully."
        assert os.path.exists(save_path)
        saved_df = pd.read_csv(save_path)
        assert not saved_df.empty

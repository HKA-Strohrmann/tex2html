import logging
import tempfile
from pathlib import Path

import pytest

from conversion.domain.conversion import LaTeXMLOutput, SubmissionConversionPayload
from conversion.services.latexml import latexml


def call_bare_latexml(app, config=dict | None) -> LaTeXMLOutput:
    """Call bare latexml without any additional configuration (no ar5iv paths or additions)."""
    with app.app_context():
        with tempfile.TemporaryDirectory() as workdir:
            app.config["LOCAL_CONVERSION_DIR"] = workdir
            app.config["LOCAL_PUBLISH_DIR"] = f"{workdir}/html"
            app.config["LATEXML_LOG_FILE"] = f"{workdir}/__stdout.txt"
            # Empty, we do not have the dockerized ar5iv additions here
            app.config["LATEXML_PATHS"] = []
            app.config["LATEXML_PRELOADS"] = []
            for key, value in config.items():
                app.config[key] = value
            latexml_log_path = Path(app.config["LATEXML_LOG_FILE"])
            with open(f"{workdir}/test.tex", "w") as file:
                file.write(config["TEST_TEX_CONTENT"])
            result = latexml(SubmissionConversionPayload(identifier=123, single_file=None), Path(workdir))
            assert latexml_log_path.exists()
            with open(latexml_log_path) as latexml_log_file:
                result.log = latexml_log_file.read()
            return result


@pytest.mark.call_latexml_tests
def test_latexml_timeout(app):
    config = {
        "LATEXML_TIMEOUT_SEC": 1,
        "TEST_TEX_CONTENT": r"\def\oops{test \oops here}\oops\bye",
    }
    result = call_bare_latexml(app, config)
    logging.warning(f"RESULT: {result}")
    assert "Fatal:timeout:timedout" in result.log
    assert result.returncode == 1

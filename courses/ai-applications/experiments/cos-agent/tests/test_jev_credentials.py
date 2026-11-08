from poc.jev import test_jev_text as cli


def setup_paths(monkeypatch, tmp_path):
    root, legacy = tmp_path / 'root.env', tmp_path / 'legacy.env'
    monkeypatch.setattr(cli, 'ENV_FILE', root)
    monkeypatch.setattr(cli, 'PROJECT_ENV_FILE', legacy)
    monkeypatch.delenv('TYPESAFE_API_KEY', raising=False)
    return root, legacy


def test_root_key_is_independent_of_working_directory(monkeypatch, tmp_path):
    root, legacy = setup_paths(monkeypatch, tmp_path)
    root.write_text('\ufeffjev-key="synthetic-root"\n', encoding='utf-8')
    legacy.write_text('jev-key=synthetic-legacy', encoding='utf-8')
    monkeypatch.chdir(tmp_path.parent)
    assert cli.get_api_key() == 'synthetic-root'


def test_environment_takes_precedence(monkeypatch, tmp_path):
    root, _ = setup_paths(monkeypatch, tmp_path)
    root.write_text('jev-key=synthetic-file', encoding='utf-8')
    monkeypatch.setenv('TYPESAFE_API_KEY', ' synthetic-env ')
    assert cli.get_api_key() == 'synthetic-env'


def test_blank_values_fall_back_to_legacy_and_alternate_name(monkeypatch, tmp_path):
    root, legacy = setup_paths(monkeypatch, tmp_path)
    monkeypatch.setenv('TYPESAFE_API_KEY', '   ')
    root.write_text('jev-key=""', encoding='utf-8')
    legacy.write_text("TYPESAFE_API_KEY='synthetic-legacy'", encoding='utf-8')
    assert cli.get_api_key() == 'synthetic-legacy'


def test_missing_key_returns_none(monkeypatch, tmp_path):
    setup_paths(monkeypatch, tmp_path)
    assert cli.get_api_key() is None

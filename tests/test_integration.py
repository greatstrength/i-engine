"""I Ching Engine Integration Tests"""

# *** imports

# ** core
import copy
import shutil

# ** infra
import pytest
import yaml

# ** app
from tiferet import App
from tiferet.contexts.cache import CacheContext

# *** constants

# ** constant: config_template
CONFIG_TEMPLATE = None  # Loaded from app/assets/config.yml at fixture time.

# *** fixtures

# ** fixture: config_yaml
@pytest.fixture
def config_yaml(tmp_path):
    '''
    Create a temp config.yml pointing to a temp HDF5 file.

    :param tmp_path: pytest temp directory.
    :type tmp_path: pathlib.Path
    :return: Path to the temp config file.
    :rtype: str
    '''

    # Load the real config.
    with open('app/assets/config.yml', 'r') as f:
        config = yaml.safe_load(f)

    # Point HDF5 to a temp file.
    h5_path = str(tmp_path / 'test.h5')
    for svc in config['services'].values():
        if isinstance(svc, dict) and svc.get('params', {}).get('h5_file'):
            svc['params']['h5_file'] = h5_path

    # Point all yaml file constants to the temp config.
    config_path = str(tmp_path / 'config.yml')
    iface = config['interfaces']['i_engine']
    if 'constants' in iface:
        for key in ('feature_yaml_file', 'error_yaml_file', 'di_yaml_file', 'logging_yaml_file'):
            if key in iface['constants']:
                iface['constants'][key] = config_path

    # Copy seed data to temp.
    seed_dest = tmp_path / 'seed'
    seed_dest.mkdir()
    shutil.copy('data/seed/hexagrams.yml', str(seed_dest / 'hexagrams.yml'))

    # Update the ingest feature to use the temp seed path.
    ingest_cmd = config['features']['kb']['ingest']['commands'][0]
    ingest_cmd['params']['seed_file'] = str(seed_dest / 'hexagrams.yml')

    # Write the temp config.
    with open(config_path, 'w') as f:
        yaml.safe_dump(config, f, sort_keys=False)

    # Return the path.
    return config_path


# ** fixture: i_engine
@pytest.fixture
def i_engine(config_yaml):
    '''
    Build the i_engine app interface from the temp config.

    :param config_yaml: Path to the temp config file.
    :type config_yaml: str
    :return: The app interface context.
    '''

    # Build the app.
    app = App('i_engine', app_yaml_file=config_yaml)

    # Replace shared mutable-default caches with fresh per-test caches.
    app.features.cache = CacheContext({})
    app.features.services.cache = CacheContext({})

    # Return the isolated app.
    return app


# *** tests

# ** test: ingest_hexagram_data
def test_ingest_hexagram_data(i_engine):
    '''
    Test that seed hexagrams are ingested into the KB.
    '''

    # Run the ingest feature.
    count = i_engine.run('kb.ingest')

    # Assert all 64 hexagrams were ingested.
    assert count == 64, f'Expected 64 hexagrams, got {count}'


# ** test: get_hexagram_after_ingest
def test_get_hexagram_after_ingest(i_engine):
    '''
    Test retrieving a hexagram by number after ingestion.
    '''

    # Ingest first.
    i_engine.run('kb.ingest')

    # Get hexagram 1 (The Creative).
    result = i_engine.run('hexagram.get', data={'number': 1})

    # Assert basic fields.
    assert result.number == 1
    assert result.name == 'The Creative'
    assert len(result.judgement) > 0
    assert len(result.image) > 0
    assert len(result.changing_lines) == 6
    assert result.changing_lines[0].line_number == 1
    assert result.changing_lines[0].yarrow_value == 9
    assert result.changing_lines[0].type == 'warning'


# ** test: list_hexagrams_after_ingest
def test_list_hexagrams_after_ingest(i_engine):
    '''
    Test listing all hexagrams after ingestion.
    '''

    # Ingest first.
    i_engine.run('kb.ingest')

    # List all.
    result = i_engine.run('hexagram.list')

    # Assert 64 hexagrams returned.
    assert len(result) == 64

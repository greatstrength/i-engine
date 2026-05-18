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


# ** test: save_and_get_reading
def test_save_and_get_reading(i_engine):
    '''
    Test saving a reading and retrieving it by ID.
    '''

    # Save a reading with result lines and hexagram references.
    reading = i_engine.run('reading.save', data=dict(
        name='Morning Meditation',
        dimension='2',
        frequency='daily',
        type='general',
        result_lines=[
            dict(position=1, heaven_line=3, man_line=3, earth_line=3, line_value=9),
            dict(position=2, heaven_line=2, man_line=2, earth_line=2, line_value=6),
            dict(position=3, heaven_line=3, man_line=2, earth_line=3, line_value=8),
            dict(position=4, heaven_line=2, man_line=3, earth_line=2, line_value=7),
            dict(position=5, heaven_line=3, man_line=3, earth_line=3, line_value=9),
            dict(position=6, heaven_line=2, man_line=2, earth_line=2, line_value=6),
        ],
        current_or_previous=dict(name='The Creative', number=1),
        next=dict(name='The Receptive', number=2),
    ))

    # Assert the reading was created with an auto-generated ID.
    assert reading.id is not None
    assert reading.name == 'Morning Meditation'
    assert reading.dimension == '2'
    assert len(reading.result_lines) == 6

    # Retrieve the reading by ID.
    fetched = i_engine.run('reading.get', data=dict(id=reading.id))

    # Assert round-trip fidelity.
    assert fetched.id == reading.id
    assert fetched.name == 'Morning Meditation'
    assert fetched.dimension == '2'
    assert fetched.frequency == 'daily'
    assert fetched.type == 'general'
    assert len(fetched.result_lines) == 6
    assert fetched.result_lines[0].position == 1
    assert fetched.result_lines[0].line_value == 9
    assert fetched.result_lines[5].position == 6
    assert fetched.result_lines[5].line_value == 6
    assert fetched.current_or_previous is not None
    assert fetched.current_or_previous.name == 'The Creative'
    assert fetched.current_or_previous.number == 1
    assert fetched.next is not None
    assert fetched.next.name == 'The Receptive'
    assert fetched.next.number == 2


# ** test: list_readings
def test_list_readings(i_engine):
    '''
    Test listing readings and filtering by type.
    '''

    # Save two readings with different types.
    i_engine.run('reading.save', data=dict(
        name='General Reading',
        dimension='2',
        type='general',
    ))
    i_engine.run('reading.save', data=dict(
        name='Elemental Reading',
        dimension='6',
        type='elemental',
    ))

    # List all readings.
    all_readings = i_engine.run('reading.list')
    assert len(all_readings) == 2

    # List filtered by type.
    general_only = i_engine.run('reading.list', data=dict(reading_type='general'))
    assert len(general_only) == 1
    assert general_only[0].type == 'general'


# ** test: delete_reading
def test_delete_reading(i_engine):
    '''
    Test deleting a reading by ID.
    '''

    # Save a reading.
    reading = i_engine.run('reading.save', data=dict(
        name='To Delete',
        dimension='2',
    ))
    reading_id = reading.id

    # Confirm it exists.
    fetched = i_engine.run('reading.get', data=dict(id=reading_id))
    assert fetched is not None

    # Delete it.
    i_engine.run('reading.delete', data=dict(id=reading_id))

    # Confirm it no longer exists via list.
    remaining = i_engine.run('reading.list')
    assert all(r.id != reading_id for r in remaining)


# ** test: save_reading_minimal
def test_save_reading_minimal(i_engine):
    '''
    Test saving a reading with only required fields (no result lines or hexagram refs).
    '''

    # Save with minimal data.
    reading = i_engine.run('reading.save', data=dict(
        name='Bare Reading',
        dimension='49',
    ))

    # Assert defaults are applied.
    assert reading.id is not None
    assert reading.name == 'Bare Reading'
    assert reading.dimension == '49'
    assert reading.frequency == 'daily'
    assert reading.type == 'general'
    assert reading.date is not None
    assert reading.created_at is not None
    assert len(reading.result_lines) == 0
    assert reading.current_or_previous is None
    assert reading.next is None

    # Verify round-trip.
    fetched = i_engine.run('reading.get', data=dict(id=reading.id))
    assert fetched.name == 'Bare Reading'
    assert fetched.dimension == '49'
    assert len(fetched.result_lines) == 0


# ** test: embed_hexagrams
def test_embed_hexagrams(i_engine):
    '''
    Test embedding all hexagram sections after ingestion.
    '''

    # Ingest hexagrams first.
    i_engine.run('kb.ingest')

    # Embed all hexagram sections.
    count = i_engine.run('kb.embed')

    # Each hexagram has ~8 sections (judgement + image + 6 lines).
    # 64 hexagrams × 8 sections = ~512 embeddings.
    assert count >= 64 * 2, f'Expected at least 128 embeddings (judgement + image), got {count}'


# ** test: search_hexagrams
def test_search_hexagrams(i_engine):
    '''
    Test semantic search over embedded hexagram content.
    '''

    # Ingest and embed.
    i_engine.run('kb.ingest')
    i_engine.run('kb.embed')

    # Search for a concept.
    results = i_engine.run('hexagram.search', data=dict(
        query='creative power and heaven',
        limit=3,
    ))

    # Assert we get results back.
    assert len(results) > 0
    assert len(results) <= 3

    # Each result should have enriched hexagram context.
    first = results[0]
    assert 'hexagram_number' in first
    assert 'hexagram_name' in first
    assert 'section_title' in first
    assert 'content' in first
    assert 'score' in first
    assert first['score'] > 0


# ** test: search_empty_kb
def test_search_empty_kb(i_engine):
    '''
    Test that search returns empty results when no embeddings exist.
    '''

    # Search without any data ingested.
    results = i_engine.run('hexagram.search', data=dict(
        query='anything',
        limit=5,
    ))

    # Assert empty results.
    assert results == []

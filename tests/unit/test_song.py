"""
Unit Test Module for the class Song in the audiofiles package
Test Framework: pyTest
"""
import pytest
import datetime
from audiofiles import Song
from audiofiles import MetadataValueError


def test_Song():
    """
    **GIVEN** a valid metadata dictionary for Song\n
    **WHEN** a new Song is created\n
    **THEN** check the type of Song attributes and their values.
    """
    # Test for valid metadata
    song = Song(metadata={"name": "sample-song", "duration": 45})

    assert isinstance(song.ID, int)
    assert isinstance(song.name, str)
    assert isinstance(song.duration, int)
    assert isinstance(song.metadata, dict)
    assert isinstance(song.uploadtime, datetime.datetime)

    assert song.ID == abs(hash(f"sample-song-45-{song.uploadtime.isoformat()}"))
    assert song.name == "sample-song"
    assert song.duration == 45
    assert song.metadata['type'] == 'Song'


def test_Song_missing_metadata():
    """
    **GIVEN** an invalid metadata dictionary for Song that is missing a key\n
    **WHEN** a new Song is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate error
    """
    # Test for 'duration' field missing
    with pytest.raises(MetadataValueError) as error:
        Song(metadata={"name": "sample-song"})

    assert str(error.value) == "metadata value is missing for 'duration'"

    # Test for 'name' field missing
    with pytest.raises(MetadataValueError) as error:
        Song(metadata={"duration": 45})

    assert str(error.value) == "metadata value is missing for 'name'"


def test_Song_invalid_name():
    """
    **GIVEN** an invalid metadata dictionary for Song that has an invalid 'name' parameter\n
    **WHEN** a new Song is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate error
    """
    # Test for 'name' field not an str
    with pytest.raises(MetadataValueError) as error:
        Song(metadata={"name": 20, "duration": 45})

    assert str(error.value) == "metadata value is invalid for 'name' - not an str"

    # Test for 'name' field too long
    with pytest.raises(MetadataValueError) as error:
        Song(metadata={"name": "sample-song" * 20, "duration": 45})

    assert str(error.value) == "metadata value is invalid for 'name' - str too long"


def test_Song_invalid_duration():
    """
    **GIVEN* an invalid metadata dictionary for Song that has an invalid 'duration' parameter\n
    **WHEN* a new Song is created\n
    **THEN* check that the constructor raises a MetadataValueError with the appropriate error
    """
    # Test for 'duration' field not an int
    with pytest.raises(MetadataValueError) as error:
        Song(metadata={"name": "sample-song", "duration": 45.3})

    assert str(error.value) == "metadata value is invalid for 'duration' - not an int"

    # Test for 'duration' field not positive
    with pytest.raises(MetadataValueError) as error:
        Song(metadata={"name": "sample-song", "duration": -45})

    assert str(error.value) == "metadata value is invalid for 'duration' - not positive"


def test_Song_extra_uploadtime():
    """
    **GIVEN** a metadata dictionary for Song that has an 'uploadtime' parameter\n
    **WHEN** a new Song is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate
    error for invalid values and check attribute type and values for valid values
    """
    # Test for valid 'uploadtime'
    song = Song(metadata={"name": "sample-song", "duration": 45, "uploadtime": "2021-01-01"})

    assert isinstance(song.ID, int)
    assert isinstance(song.name, str)
    assert isinstance(song.duration, int)
    assert isinstance(song.metadata, dict)
    assert isinstance(song.uploadtime, datetime.datetime)

    assert song.ID == abs(hash(f"sample-song-45-2021-01-01T00:00:00"))
    assert song.name == "sample-song"
    assert song.duration == 45
    assert song.uploadtime == datetime.datetime.fromisoformat("2021-01-01")

    # Test for 'uploadtime' not an str
    with pytest.raises(MetadataValueError) as error:
        Song(metadata={"name": "sample-song", "duration": 45, "uploadtime": 3453})

    assert str(error.value) == "metadata value is invalid for 'uploadtime' - not an str"

    # Test for 'uploadtime' not an ISO8601 string
    with pytest.raises(MetadataValueError) as error:
        Song(metadata={"name": "sample-song", "duration": 45, "uploadtime": "3453"})

    assert str(error.value) == "metadata value is invalid for 'uploadtime' - not ISO8601"


def test_Audio_extra_ID():
    """
    **GIVEN** a metadata dictionary for Song that has an 'ID' parameter\n
    **WHEN** a new Song is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate
    error for invalid values and check attribute type and values for valid values
    """
    # Test for valid '_id'
    song = Song(metadata={"name": "sample-song", "duration": 45, "_id": 23214241})

    assert isinstance(song.ID, int)
    assert isinstance(song.name, str)
    assert isinstance(song.duration, int)
    assert isinstance(song.metadata, dict)
    assert isinstance(song.uploadtime, datetime.datetime)

    assert song.ID == 23214241
    assert song.name == "sample-song"
    assert song.duration == 45

    # Test for '_id' not an int
    with pytest.raises(MetadataValueError) as error:
        Song(metadata={"name": "sample-song", "duration": 45, "_id": "3453"})

    assert str(error.value) == "metadata value is invalid for '_id' - not an int"


def test_Audio_extra_type():
    """
    **GIVEN** a metadata dictionary for Song that has an 'type' parameter\n
    **WHEN** a new Song is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate
    error for invalid values and check attribute type and values for valid values
    """
    # Test Case 1 - valid 'Song' type
    song = Song(metadata={"name": "sample-song", "duration": 45, "type": "Song"})

    assert isinstance(song.ID, int)
    assert isinstance(song.name, str)
    assert isinstance(song.duration, int)
    assert isinstance(song.metadata, dict)
    assert isinstance(song.uploadtime, datetime.datetime)

    assert song.ID == abs(hash(f"sample-song-45-{song.uploadtime.isoformat()}"))
    assert song.name == "sample-song"
    assert song.duration == 45

    assert isinstance(song.metadata['type'], str)
    assert song.metadata['type'] == "Song"

    # Test Case 2 - invalid 'Album' type - Song() will overwrite
    Song(metadata={"name": "sample-song", "duration": 45, "type": "Album"})

    assert isinstance(song.ID, int)
    assert isinstance(song.name, str)
    assert isinstance(song.duration, int)
    assert isinstance(song.metadata, dict)
    assert isinstance(song.uploadtime, datetime.datetime)

    assert song.ID == abs(hash(f"sample-song-45-{song.uploadtime.isoformat()}"))
    assert song.name == "sample-song"
    assert song.duration == 45

    assert isinstance(song.metadata['type'], str)
    assert song.metadata['type'] == "Song"

    # Test Case 3 - invalid value and type 3423  - Song() will overwrite
    Song(metadata={"name": "sample-song", "duration": 45, "type": 342})

    assert isinstance(song.ID, int)
    assert isinstance(song.name, str)
    assert isinstance(song.duration, int)
    assert isinstance(song.metadata, dict)
    assert isinstance(song.uploadtime, datetime.datetime)

    assert song.ID == abs(hash(f"sample-song-45-{song.uploadtime.isoformat()}"))
    assert song.name == "sample-song"
    assert song.duration == 45

    assert isinstance(song.metadata['type'], str)
    assert song.metadata['type'] == "Song"


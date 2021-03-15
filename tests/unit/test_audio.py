"""
Unit Test Module for the class Audio in the audiofiles package
Test Framework: pyTest
"""
import pytest
import datetime
from audiofiles import Audio
from audiofiles import MetadataValueError


def test_Audio():
    """
    **GIVEN** a valid metadata dictionary for Audio\n
    **WHEN** a new Audio is created\n
    **THEN** check the type of Audio attributes and their values.
    """
    # Test for valid metadata
    audio = Audio(metadata={"name": "sample-audio", "duration": 45})

    assert isinstance(audio.ID, int)
    assert isinstance(audio.name, str)
    assert isinstance(audio.duration, int)
    assert isinstance(audio.metadata, dict)
    assert isinstance(audio.uploadtime, datetime.datetime)

    assert audio.ID == abs(hash(f"sample-audio-45-{audio.uploadtime.isoformat()}"))
    assert audio.name == "sample-audio"
    assert audio.duration == 45


def test_Audio_missing_metadata():
    """
    **GIVEN** an invalid metadata dictionary for Audio that is missing a key\n
    **WHEN** a new Audio is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate error
    """
    # Test for 'duration' field missing
    with pytest.raises(MetadataValueError) as error:
        Audio(metadata={"name": "sample-audio"})

    assert str(error.value) == "metadata value is missing for 'duration'"

    # Test for 'name' field missing
    with pytest.raises(MetadataValueError) as error:
        Audio(metadata={"duration": 45})

    assert str(error.value) == "metadata value is missing for 'name'"


def test_Audio_invalid_name():
    """
    **GIVEN** an invalid metadata dictionary for Audio that has an invalid 'name' parameter\n
    **WHEN** a new Audio is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate error
    """
    # Test for 'name' field not an str
    with pytest.raises(MetadataValueError) as error:
        Audio(metadata={"name": 20, "duration": 45})

    assert str(error.value) == "metadata value is invalid for 'name' - not an str"

    # Test for 'name' field too long
    with pytest.raises(MetadataValueError) as error:
        Audio(metadata={"name": "sample-audio" * 20, "duration": 45})

    assert str(error.value) == "metadata value is invalid for 'name' - str too long"


def test_Audio_invalid_duration():
    """
    **GIVEN* an invalid metadata dictionary for Audio that has an invalid 'duration' parameter\n
    **WHEN* a new Audio is created\n
    **THEN* check that the constructor raises a MetadataValueError with the appropriate error
    """
    # Test for 'duration' field not an int
    with pytest.raises(MetadataValueError) as error:
        Audio(metadata={"name": "sample-audio", "duration": 45.3})

    assert str(error.value) == "metadata value is invalid for 'duration' - not an int"

    # Test for 'duration' field not positive
    with pytest.raises(MetadataValueError) as error:
        Audio(metadata={"name": "sample-audio", "duration": -45})

    assert str(error.value) == "metadata value is invalid for 'duration' - not positive"


def test_Audio_extra_uploadtime():
    """
    **GIVEN** a metadata dictionary for Audio that has an 'uploadtime' parameter\n
    **WHEN** a new Audio is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate
    error for invalid values and check attribute type and values for valid values
    """
    # Test for valid 'uploadtime'
    audio = Audio(metadata={"name": "sample-audio", "duration": 45, "uploadtime": "2021-01-01"})

    assert isinstance(audio.ID, int)
    assert isinstance(audio.name, str)
    assert isinstance(audio.duration, int)
    assert isinstance(audio.metadata, dict)
    assert isinstance(audio.uploadtime, datetime.datetime)

    assert audio.ID == abs(hash(f"sample-audio-45-2021-01-01T00:00:00"))
    assert audio.name == "sample-audio"
    assert audio.duration == 45
    assert audio.uploadtime == datetime.datetime.fromisoformat("2021-01-01")

    # Test for 'uploadtime' not an str
    with pytest.raises(MetadataValueError) as error:
        Audio(metadata={"name": "sample-audio", "duration": 45, "uploadtime": 3453})

    assert str(error.value) == "metadata value is invalid for 'uploadtime' - not an str"

    # Test for 'uploadtime' not an ISO8601 string
    with pytest.raises(MetadataValueError) as error:
        Audio(metadata={"name": "sample-audio", "duration": 45, "uploadtime": "3453"})

    assert str(error.value) == "metadata value is invalid for 'uploadtime' - not ISO8601"


def test_Audio_extra_ID():
    """
    **GIVEN** a metadata dictionary for Audio that has an 'ID' parameter\n
    **WHEN** a new Audio is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate
    error for invalid values and check attribute type and values for valid values
    """
    # Test for valid '_id'
    audio = Audio(metadata={"name": "sample-audio", "duration": 45, "_id": 23214241})

    assert isinstance(audio.ID, int)
    assert isinstance(audio.name, str)
    assert isinstance(audio.duration, int)
    assert isinstance(audio.metadata, dict)
    assert isinstance(audio.uploadtime, datetime.datetime)

    assert audio.ID == 23214241
    assert audio.name == "sample-audio"
    assert audio.duration == 45

    # Test for '_id' not an int
    with pytest.raises(MetadataValueError) as error:
        Audio(metadata={"name": "sample-audio", "duration": 45, "_id": "3453"})

    assert str(error.value) == "metadata value is invalid for '_id' - not an int"


def test_Audio_extra_type():
    """
    **GIVEN** a metadata dictionary for Audio that has an 'type' parameter\n
    **WHEN** a new Audio is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate
    error for invalid values and check attribute type and values for valid values
    """
    # Test Case 1 - valid 'Song' type
    audio = Audio(metadata={"name": "sample-audio", "duration": 45, "type": "Audio"})

    assert isinstance(audio.ID, int)
    assert isinstance(audio.name, str)
    assert isinstance(audio.duration, int)
    assert isinstance(audio.metadata, dict)
    assert isinstance(audio.uploadtime, datetime.datetime)

    assert audio.ID == abs(hash(f"sample-audio-45-{audio.uploadtime.isoformat()}"))
    assert audio.name == "sample-audio"
    assert audio.duration == 45

    assert isinstance(audio.metadata['type'], str)
    assert audio.metadata['type'] == "Audio"

    # Test Case 2 - valid 'Song' type
    audio = Audio(metadata={"name": "sample-audio", "duration": 45, "type": "Song"})

    assert isinstance(audio.ID, int)
    assert isinstance(audio.name, str)
    assert isinstance(audio.duration, int)
    assert isinstance(audio.metadata, dict)
    assert isinstance(audio.uploadtime, datetime.datetime)

    assert audio.ID == abs(hash(f"sample-audio-45-{audio.uploadtime.isoformat()}"))
    assert audio.name == "sample-audio"
    assert audio.duration == 45

    assert isinstance(audio.metadata['type'], str)
    assert audio.metadata['type'] == "Song"

    # Test Case 3 - invalid 'Album' type - Audio() will raise error
    with pytest.raises(MetadataValueError) as error:
        Audio(metadata={"name": "sample-audio", "duration": 45, "type": "Album"})

    assert str(error.value) == "metadata value is invalid for 'type' - not supported"

    # Test Case 4 - invalid value and type 3423  - Audio() will raise error
    with pytest.raises(MetadataValueError) as error:
        Audio(metadata={"name": "sample-audio", "duration": 45, "type": 342})

    assert str(error.value) == "metadata value is invalid for 'type' - not an str"

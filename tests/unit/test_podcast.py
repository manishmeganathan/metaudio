"""
Unit Test Module for the class Podcast in the audiofiles package
Test Framework: pyTest
"""
import pytest
import datetime
from audiofiles import Podcast
from audiofiles import MetadataValueError


def test_Podcast():
    """
    **GIVEN** a valid metadata dictionary for Podcast\n
    **WHEN** a new Podcast is created\n
    **THEN** check the type of Podcast attributes and their values.
    """
    # Test for valid metadata without a 'participants' field
    podcast = Podcast(metadata={"name": "sample-podcast", "duration": 45, "host": "Manish"})

    assert isinstance(podcast.ID, int)
    assert isinstance(podcast.name, str)
    assert isinstance(podcast.host, str)
    assert isinstance(podcast.participants, list)
    assert isinstance(podcast.duration, int)
    assert isinstance(podcast.metadata, dict)
    assert isinstance(podcast.uploadtime, datetime.datetime)

    assert podcast.ID == abs(hash(f"sample-podcast-45-{podcast.uploadtime.isoformat()}"))
    assert podcast.name == "sample-podcast"
    assert podcast.host == "Manish"
    assert podcast.participants == []
    assert podcast.duration == 45


def test_Podcast_participants():
    """
    **GIVEN** a valid metadata dictionary for Podcast\n
    **WHEN** a new Podcast is created\n
    **THEN** check the type of Podcast attributes and their values.
    """
    # Test for valid metadata with a 'participants' field
    podcast = Podcast(metadata={"name": "sample-podcast", "duration": 45,
                                "host": "host1", "participants": ["cast1", "cast2"]})

    assert isinstance(podcast.ID, int)
    assert isinstance(podcast.name, str)
    assert isinstance(podcast.host, str)
    assert isinstance(podcast.participants, list)
    assert isinstance(podcast.duration, int)
    assert isinstance(podcast.metadata, dict)
    assert isinstance(podcast.uploadtime, datetime.datetime)

    assert podcast.ID == abs(hash(f"sample-podcast-45-{podcast.uploadtime.isoformat()}"))
    assert podcast.name == "sample-podcast"
    assert podcast.host == "host1"
    assert podcast.participants == ["cast1", "cast2"]
    assert podcast.duration == 45


def test_Podcast_missing_metadata():
    """
    **GIVEN** an invalid metadata dictionary for Podcast that is missing a key\n
    **WHEN** a new Podcast is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate error
    """
    # Test for 'name' field missing
    with pytest.raises(MetadataValueError) as error:
        Podcast(metadata={"duration": 45, "host": "host1"})

    assert str(error.value) == "metadata value is missing for 'name'"

    # Test for 'duration' field missing
    with pytest.raises(MetadataValueError) as error:
        Podcast(metadata={"name": "sample-podcast", "host": "host1"})

    assert str(error.value) == "metadata value is missing for 'duration'"

    # Test for 'host' field missing
    with pytest.raises(MetadataValueError) as error:
        Podcast(metadata={"name": "sample-podcast", "duration": 45})

    assert str(error.value) == "metadata value is missing for 'host'"


def test_Podcast_invalid_name():
    """
    **GIVEN** an invalid metadata dictionary for Podcast that has an invalid 'name' parameter\n
    **WHEN** a new Podcast is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate error
    """
    # Test for 'name' field not an str
    with pytest.raises(MetadataValueError) as error:
        Podcast(metadata={"name": 20, "duration": 45, "host": "host1"})

    assert str(error.value) == "metadata value is invalid for 'name' - not an str"

    # Test for 'name' field too long
    with pytest.raises(MetadataValueError) as error:
        Podcast(metadata={"name": "sample-podcast" * 20, "duration": 45, "host": "host1"})

    assert str(error.value) == "metadata value is invalid for 'name' - str too long"


def test_Podcast_invalid_duration():
    """
    **GIVEN* an invalid metadata dictionary for Podcast that has an invalid 'duration' parameter\n
    **WHEN* a new Podcast is created\n
    **THEN* check that the constructor raises a MetadataValueError with the appropriate error
    """
    # Test for 'duration' field not an int
    with pytest.raises(MetadataValueError) as error:
        Podcast(metadata={"name": "sample-podcast", "duration": 45.3, "host": "host1"})

    assert str(error.value) == "metadata value is invalid for 'duration' - not an int"

    # Test for 'duration' field not positive
    with pytest.raises(MetadataValueError) as error:
        Podcast(metadata={"name": "sample-podcast", "duration": -45, "host": "host1"})

    assert str(error.value) == "metadata value is invalid for 'duration' - not positive"


def test_Podcast_invalid_host():
    """
    **GIVEN** an invalid metadata dictionary for Podcast that has an invalid 'host' parameter\n
    **WHEN** a new Podcast is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate error
    """
    # Test for 'host' field not an str
    with pytest.raises(MetadataValueError) as error:
        Podcast(metadata={"name": "sample-podcast", "duration": 45, "host": 1})

    assert str(error.value) == "metadata value is invalid for 'host' - not an str"

    # Test for 'host' field too long
    with pytest.raises(MetadataValueError) as error:
        Podcast(metadata={"name": "sample-podcast", "duration": 45, "host": "host1" * 40})

    assert str(error.value) == "metadata value is invalid for 'host' - str too long"


def test_Podcast_invalid_participants():
    """
    **GIVEN** an invalid metadata dict for Podcast that has an invalid 'participants' parameter\n
    **WHEN** a new Podcast is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate error
    """
    # Test for 'participants' field not a list
    with pytest.raises(MetadataValueError) as error:
        Podcast(metadata={"name": "sample-podcast", "duration": 45,
                          "host": "host1", "participants": "cast1"})

    assert str(error.value) == "metadata value is invalid for 'participants' - not a list"

    # Test for 'participants' field too long
    with pytest.raises(MetadataValueError) as error:
        Podcast(metadata={"name": "sample-podcast", "duration": 45,
                          "host": "host1", "participants": ["cast1"]*15})

    expected = "metadata value is invalid for 'participants' - too many participants"
    assert str(error.value) == expected

    # Test for 'participants' for a single participant str too long
    with pytest.raises(MetadataValueError) as error:
        Podcast(metadata={"name": "sample-podcast", "duration": 45,
                          "host": "host1", "participants": ["cast1", "cast2"*30]})

    expected = "metadata value is invalid for 'participants' - participant 2 - str too long"
    assert str(error.value) == expected

    # Test for 'participants' for a single participant not an str
    with pytest.raises(MetadataValueError) as error:
        Podcast(metadata={"name": "sample-podcast", "duration": 45,
                          "host": "host1", "participants": ["cast1", 40]})

    expected = "metadata value is invalid for 'participants' - participant 2 - not an str"
    assert str(error.value) == expected


def test_Podcast_extra_uploadtime():
    """
    **GIVEN** a metadata dictionary for Podcast that has an 'uploadtime' parameter\n
    **WHEN** a new Podcast is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate
    error for invalid values and check attribute type and values for valid values
    """
    # Test for valid 'uploadtime'
    podcast = Podcast(metadata={"name": "sample-podcast", "duration": 45,
                                "uploadtime": "2021-01-01", "host": "host1"})

    assert isinstance(podcast.ID, int)
    assert isinstance(podcast.name, str)
    assert isinstance(podcast.host, str)
    assert isinstance(podcast.participants, list)
    assert isinstance(podcast.duration, int)
    assert isinstance(podcast.metadata, dict)
    assert isinstance(podcast.uploadtime, datetime.datetime)

    assert podcast.ID == abs(hash(f"sample-podcast-45-2021-01-01T00:00:00"))
    assert podcast.name == "sample-podcast"
    assert podcast.host == "host1"
    assert podcast.participants == []
    assert podcast.duration == 45
    assert podcast.uploadtime == datetime.datetime.fromisoformat("2021-01-01")

    # Test for 'uploadtime' not an str
    with pytest.raises(MetadataValueError) as error:
        Podcast(metadata={"name": "sample-podcast", "duration": 45, "uploadtime": 3453})

    assert str(error.value) == "metadata value is invalid for 'uploadtime' - not an str"

    # Test for 'uploadtime' not an ISO8601 string
    with pytest.raises(MetadataValueError) as error:
        Podcast(metadata={"name": "sample-podcast", "duration": 45,
                          "uploadtime": "3453", "host": "host1"})

    assert str(error.value) == "metadata value is invalid for 'uploadtime' - not ISO8601"


def test_Podcast_extra_ID():
    """
    **GIVEN** a metadata dictionary for Podcast that has an 'ID' parameter\n
    **WHEN** a new Podcast is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate
    error for invalid values and check attribute type and values for valid values
    """
    # Test for valid '_id'
    podcast = Podcast(metadata={"name": "sample-podcast", "duration": 45,
                                "_id": 23214241, "host": "host1"})

    assert isinstance(podcast.ID, int)
    assert isinstance(podcast.name, str)
    assert isinstance(podcast.host, str)
    assert isinstance(podcast.participants, list)
    assert isinstance(podcast.duration, int)
    assert isinstance(podcast.metadata, dict)
    assert isinstance(podcast.uploadtime, datetime.datetime)

    assert podcast.ID == 23214241
    assert podcast.name == "sample-podcast"
    assert podcast.host == "host1"
    assert podcast.participants == []
    assert podcast.duration == 45

    # Test for '_id' not an int
    with pytest.raises(MetadataValueError) as error:
        Podcast(metadata={"name": "sample-podcast", "duration": 45,
                          "_id": "3453", "host": "host1"})

    assert str(error.value) == "metadata value is invalid for '_id' - not an int"


def test_Podcast_extra_type():
    """
    **GIVEN** a metadata dictionary for Podcast that has an 'type' parameter\n
    **WHEN** a new Podcast is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate
    error for invalid values and check attribute type and values for valid values
    """
    # Test Case 1 - valid 'Podcast' type
    podcast = Podcast(metadata={"name": "sample-podcast", "duration": 45,
                                "type": "Podcast", "host": "host1"})

    assert isinstance(podcast.ID, int)
    assert isinstance(podcast.name, str)
    assert isinstance(podcast.host, str)
    assert isinstance(podcast.participants, list)
    assert isinstance(podcast.duration, int)
    assert isinstance(podcast.metadata, dict)
    assert isinstance(podcast.uploadtime, datetime.datetime)

    assert podcast.ID == abs(hash(f"sample-podcast-45-{podcast.uploadtime.isoformat()}"))
    assert podcast.name == "sample-podcast"
    assert podcast.host == "host1"
    assert podcast.participants == []
    assert podcast.duration == 45

    assert isinstance(podcast.metadata['type'], str)
    assert podcast.metadata['type'] == "Podcast"

    # Test Case 2 - invalid 'Album' type - Podcast() will overwrite
    podcast = Podcast(metadata={"name": "sample-podcast", "duration": 45,
                                "type": "Album", "host": "host1"})

    assert isinstance(podcast.ID, int)
    assert isinstance(podcast.name, str)
    assert isinstance(podcast.duration, int)
    assert isinstance(podcast.metadata, dict)
    assert isinstance(podcast.uploadtime, datetime.datetime)

    assert podcast.ID == abs(hash(f"sample-podcast-45-{podcast.uploadtime.isoformat()}"))
    assert podcast.name == "sample-podcast"
    assert podcast.host == "host1"
    assert podcast.participants == []
    assert podcast.duration == 45

    assert isinstance(podcast.metadata['type'], str)
    assert podcast.metadata['type'] == "Podcast"

    # Test Case 3 - invalid value and type 3423 - Podcast() will overwrite
    podcast = Podcast(metadata={"name": "sample-podcast", "duration": 45,
                                "type": 3423, "host": "host1"})

    assert isinstance(podcast.ID, int)
    assert isinstance(podcast.name, str)
    assert isinstance(podcast.duration, int)
    assert isinstance(podcast.metadata, dict)
    assert isinstance(podcast.uploadtime, datetime.datetime)

    assert podcast.ID == abs(hash(f"sample-podcast-45-{podcast.uploadtime.isoformat()}"))
    assert podcast.name == "sample-podcast"
    assert podcast.duration == 45

    assert isinstance(podcast.metadata['type'], str)
    assert podcast.metadata['type'] == "Podcast"

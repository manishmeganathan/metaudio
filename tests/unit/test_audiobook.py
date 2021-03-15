"""
Unit Test Module for the class Audiobook in the audiofiles package
Test Framework: pyTest
"""
import pytest
import datetime
from audiofiles import Audiobook
from audiofiles import MetadataValueError


def test_Audiobook():
    """
    **GIVEN** a valid metadata dictionary for Audiobook\n
    **WHEN** a new Audiobook is created\n
    **THEN** check the type of Audiobook attributes and their values.
    """
    # Test for valid metadata
    audiobook = Audiobook(metadata={"name": "sample-book", "duration": 45,
                                    "author": "author1", "narrator": "narrator1"})

    assert isinstance(audiobook.ID, int)
    assert isinstance(audiobook.name, str)
    assert isinstance(audiobook.author, str)
    assert isinstance(audiobook.narrator, str)
    assert isinstance(audiobook.duration, int)
    assert isinstance(audiobook.metadata, dict)
    assert isinstance(audiobook.uploadtime, datetime.datetime)

    assert audiobook.ID == abs(hash(f"sample-book-45-{audiobook.uploadtime.isoformat()}"))
    assert audiobook.name == "sample-book"
    assert audiobook.author == "author1"
    assert audiobook.narrator == "narrator1"
    assert audiobook.duration == 45
    assert audiobook.metadata['type'] == 'Audiobook'


def test_Song_missing_metadata():
    """
    **GIVEN** an invalid metadata dictionary for Audiobook that is missing a key\n
    **WHEN** a new Audiobook is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate error
    """
    # Test for 'duration' field missing
    with pytest.raises(MetadataValueError) as error:
        Audiobook(metadata={"name": "sample-book", "author": "author1", "narrator": "narrator1"})

    assert str(error.value) == "metadata value is missing for 'duration'"

    # Test for 'name' field missing
    with pytest.raises(MetadataValueError) as error:
        Audiobook(metadata={"duration": 45, "author": "author1", "narrator": "narrator1"})

    assert str(error.value) == "metadata value is missing for 'name'"

    # Test for 'author' field missing
    with pytest.raises(MetadataValueError) as error:
        Audiobook(metadata={"duration": 45, "name": "sample-book", "narrator": "narrator1"})

    assert str(error.value) == "metadata value is missing for 'author'"

    # Test for 'author' field missing
    with pytest.raises(MetadataValueError) as error:
        Audiobook(metadata={"duration": 45, "name": "sample-book", "author": "author1"})

    assert str(error.value) == "metadata value is missing for 'narrator'"


def test_Audiobook_invalid_name():
    """
    **GIVEN** an invalid metadata dict for Audiobook that has an invalid 'name' parameter\n
    **WHEN** a new Audiobook is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate error
    """
    # Test for 'name' field not an str
    with pytest.raises(MetadataValueError) as error:
        Audiobook(metadata={"name": 20, "author": "author1",
                            "duration": 45, "narrator": "narrator1"})

    assert str(error.value) == "metadata value is invalid for 'name' - not an str"

    # Test for 'name' field too long
    with pytest.raises(MetadataValueError) as error:
        Audiobook(metadata={"name": "sample-book" * 20, "author": "author1",
                            "duration": 45, "narrator": "narrator1"})

    assert str(error.value) == "metadata value is invalid for 'name' - str too long"


def test_Song_invalid_duration():
    """
    **GIVEN* an invalid metadata dict for Audiobook that has an invalid 'duration' parameter\n
    **WHEN* a new Audiobook is created\n
    **THEN* check that the constructor raises a MetadataValueError with the appropriate error
    """
    # Test for 'duration' field not an int
    with pytest.raises(MetadataValueError) as error:
        Audiobook(metadata={"name": "sample-book", "duration": 45.3,
                            "author": "author1", "narrator": "narrator1"})

    assert str(error.value) == "metadata value is invalid for 'duration' - not an int"

    # Test for 'duration' field not positive
    with pytest.raises(MetadataValueError) as error:
        Audiobook(metadata={"name": "sample-book", "duration": -45,
                            "author": "author1", "narrator": "narrator1"})

    assert str(error.value) == "metadata value is invalid for 'duration' - not positive"


def test_Audiobook_invalid_author():
    """
    **GIVEN** an invalid metadata dict for Audiobook that has an invalid 'author' parameter\n
    **WHEN** a new Audiobook is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate error
    """
    # Test for 'author' field not an str
    with pytest.raises(MetadataValueError) as error:
        Audiobook(metadata={"name": "sample-book", "author": 1,
                            "duration": 45, "narrator": "narrator1"})

    assert str(error.value) == "metadata value is invalid for 'author' - not an str"

    # Test for 'author' field too long
    with pytest.raises(MetadataValueError) as error:
        Audiobook(metadata={"name": "sample-book", "author": "author1" * 20,
                            "duration": 45, "narrator": "narrator1"})

    assert str(error.value) == "metadata value is invalid for 'author' - str too long"


def test_Audiobook_invalid_narrator():
    """
    **GIVEN** an invalid metadata dict for Audiobook that has an invalid 'narrator' parameter\n
    **WHEN** a new Audiobook is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate error
    """
    # Test for 'narrator' field not an str
    with pytest.raises(MetadataValueError) as error:
        Audiobook(metadata={"name": "sample-book", "author": "author1",
                            "duration": 45, "narrator": 1})

    assert str(error.value) == "metadata value is invalid for 'narrator' - not an str"

    # Test for 'narrator' field too long
    with pytest.raises(MetadataValueError) as error:
        Audiobook(metadata={"name": "sample-book", "author": "author1",
                            "duration": 45, "narrator": "narrator1" * 20})

    assert str(error.value) == "metadata value is invalid for 'narrator' - str too long"


def test_Audiobook_extra_uploadtime():
    """
    **GIVEN** a metadata dictionary for Audiobook that has an 'uploadtime' parameter\n
    **WHEN** a new Audiobook is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate
    error for invalid values and check attribute type and values for valid values
    """
    # Test for valid 'uploadtime'
    audiobook = Audiobook(metadata={"name": "sample-book", "duration": 45, "narrator": "narrator1",
                                    "uploadtime": "2021-01-01", "author": "author1"})

    assert isinstance(audiobook.ID, int)
    assert isinstance(audiobook.name, str)
    assert isinstance(audiobook.author, str)
    assert isinstance(audiobook.narrator, str)
    assert isinstance(audiobook.duration, int)
    assert isinstance(audiobook.metadata, dict)
    assert isinstance(audiobook.uploadtime, datetime.datetime)

    assert audiobook.ID == abs(hash(f"sample-book-45-2021-01-01T00:00:00"))
    assert audiobook.name == "sample-book"
    assert audiobook.author == "author1"
    assert audiobook.narrator == "narrator1"
    assert audiobook.duration == 45
    assert audiobook.uploadtime == datetime.datetime.fromisoformat("2021-01-01")

    # Test for 'uploadtime' not an str
    with pytest.raises(MetadataValueError) as error:
        Audiobook(metadata={"name": "sample-song", "duration": 45, "author": "author1",
                            "uploadtime": 3453, "narrator": "narrator1"})

    assert str(error.value) == "metadata value is invalid for 'uploadtime' - not an str"

    # Test for 'uploadtime' not an ISO8601 string
    with pytest.raises(MetadataValueError) as error:
        Audiobook(metadata={"name": "sample-song", "duration": 45, "author": "author1",
                            "uploadtime": "3453", "narrator": "narrator1"})

    assert str(error.value) == "metadata value is invalid for 'uploadtime' - not ISO8601"


def test_Audiobook_extra_ID():
    """
    **GIVEN** a metadata dictionary for Audiobook that has an 'ID' parameter\n
    **WHEN** a new Audiobook is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate
    error for invalid values and check attribute type and values for valid values
    """
    # Test for valid '_id'
    audiobook = Audiobook(metadata={"name": "sample-book", "duration": 45, "_id": 23214241,
                                    "author": "author1", "narrator": "narrator1"})

    assert isinstance(audiobook.ID, int)
    assert isinstance(audiobook.name, str)
    assert isinstance(audiobook.author, str)
    assert isinstance(audiobook.narrator, str)
    assert isinstance(audiobook.duration, int)
    assert isinstance(audiobook.metadata, dict)
    assert isinstance(audiobook.uploadtime, datetime.datetime)

    assert audiobook.ID == 23214241
    assert audiobook.name == "sample-book"
    assert audiobook.author == "author1"
    assert audiobook.narrator == "narrator1"
    assert audiobook.duration == 45

    # Test for '_id' not an int
    with pytest.raises(MetadataValueError) as error:
        Audiobook(metadata={"name": "sample-song", "duration": 45, "_id": "3453",
                            "author": "author1", "narrator": "narrator1"})

    assert str(error.value) == "metadata value is invalid for '_id' - not an int"


def test_Audiobook_extra_type():
    """
    **GIVEN** a metadata dictionary for Audiobook that has an 'type' parameter\n
    **WHEN** a new Audiobook is created\n
    **THEN** check that the constructor raises a MetadataValueError with the appropriate
    error for invalid values and check attribute type and values for valid values
    """
    # Test Case 1 - valid 'Audiobook' type
    audiobook = Audiobook(metadata={"name": "sample-book", "duration": 45, "type": "Audiobook",
                                    "author": "author1", "narrator": "narrator1"})

    assert isinstance(audiobook.ID, int)
    assert isinstance(audiobook.name, str)
    assert isinstance(audiobook.author, str)
    assert isinstance(audiobook.narrator, str)
    assert isinstance(audiobook.duration, int)
    assert isinstance(audiobook.metadata, dict)
    assert isinstance(audiobook.uploadtime, datetime.datetime)

    assert audiobook.ID == abs(hash(f"sample-book-45-{audiobook.uploadtime.isoformat()}"))
    assert audiobook.name == "sample-book"
    assert audiobook.author == "author1"
    assert audiobook.narrator == "narrator1"
    assert audiobook.duration == 45

    assert isinstance(audiobook.metadata['type'], str)
    assert audiobook.metadata['type'] == "Audiobook"

    # Test Case 2 - invalid 'Album' type - Audiobook() will overwrite
    audiobook = Audiobook(metadata={"name": "sample-book", "duration": 45, "type": "Album",
                                    "author": "author1", "narrator": "narrator1"})

    assert isinstance(audiobook.ID, int)
    assert isinstance(audiobook.name, str)
    assert isinstance(audiobook.author, str)
    assert isinstance(audiobook.narrator, str)
    assert isinstance(audiobook.duration, int)
    assert isinstance(audiobook.metadata, dict)
    assert isinstance(audiobook.uploadtime, datetime.datetime)

    assert audiobook.ID == abs(hash(f"sample-book-45-{audiobook.uploadtime.isoformat()}"))
    assert audiobook.name == "sample-book"
    assert audiobook.author == "author1"
    assert audiobook.narrator == "narrator1"
    assert audiobook.duration == 45

    assert isinstance(audiobook.metadata['type'], str)
    assert audiobook.metadata['type'] == "Audiobook"

    # Test Case 3 - invalid value and type 3423  - Audiobook() will overwrite
    audiobook = Audiobook(metadata={"name": "sample-book", "duration": 45, "type": 3423,
                                    "author": "author1", "narrator": "narrator1"})

    assert isinstance(audiobook.ID, int)
    assert isinstance(audiobook.name, str)
    assert isinstance(audiobook.author, str)
    assert isinstance(audiobook.narrator, str)
    assert isinstance(audiobook.duration, int)
    assert isinstance(audiobook.metadata, dict)
    assert isinstance(audiobook.uploadtime, datetime.datetime)

    assert audiobook.ID == abs(hash(f"sample-book-45-{audiobook.uploadtime.isoformat()}"))
    assert audiobook.name == "sample-book"
    assert audiobook.author == "author1"
    assert audiobook.narrator == "narrator1"
    assert audiobook.duration == 45

    assert isinstance(audiobook.metadata['type'], str)
    assert audiobook.metadata['type'] == "Audiobook"

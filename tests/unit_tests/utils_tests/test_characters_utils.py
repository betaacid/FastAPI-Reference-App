import pytest

from app.utils.characters_utils import format_star_wars_name


def test_format_star_wars_name_with_spaces():
    result = format_star_wars_name("Darth Vader")
    assert result == "Darth_Vader_from_the_starwars_universe"


def test_format_star_wars_name_no_spaces():
    result = format_star_wars_name("Yoda")
    assert result == "Yoda_from_the_starwars_universe"


def test_format_star_wars_name_multiple_spaces():
    result = format_star_wars_name("Obi Wan Kenobi")
    assert result == "Obi_Wan_Kenobi_from_the_starwars_universe"


def test_format_star_wars_name_empty_string():
    result = format_star_wars_name("")
    assert result == "_from_the_starwars_universe"

'''
Helper Functions
'''
from structure import Data, SECRET
from error import InputError, AccessError
import helper
import pytest
from other import clear

def test_encode_token():
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6MX0.qRA0hDG23-8dyEyZBpai40AvL_GEa76xGM4d3tM1rsA"
    assert helper.encode_token(1) == token

def test_decode_token():
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6MX0.qRA0hDG23-8dyEyZBpai40AvL_GEa76xGM4d3tM1rsA"
    assert helper.decode_token(token) == 1

def test_length_short():
    with pytest.raises(InputError):
        assert helper.length("profile_type", "", 10, 100)
        
def test_length_long():
    name = "aaaaaaaaaa"
    with pytest.raises(InputError):
        assert helper.length("profile_type", name, 1, 5)

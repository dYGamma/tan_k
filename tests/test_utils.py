from utils.data_validator import validate_product

def test_validate_product():
    assert validate_product("A","kg",10)
    assert not validate_product("","kg",10)
    assert not validate_product("A","",10)
    assert validate_product("X","l",0)

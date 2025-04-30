import pytest
from database import initialize_db, get_connection
from models.user import User
from models.product import Product
from models.supplier import Supplier
from models.operation import Operation

@pytest.fixture(autouse=True)
def setup_db(tmp_path, monkeypatch):
    db_file = tmp_path / "test.db"
    monkeypatch.setenv("CONFIG_PATH", str(db_file))  # если используем окружение
    initialize_db()
    yield

def test_user_auth():
    u = User.authenticate("admin","admin")
    assert u and u["role"] == "admin"

def test_product_crud():
    Product.add("Test","pcs",30)
    prods = Product.all()
    assert any(p[1]=="Test" for p in prods)

def test_supplier_and_operation():
    Supplier.add("Sup","cont")
    sups = Supplier.all()
    sid = sups[-1][0]
    prods = Product.all()
    pid = prods[0][0]
    Operation.add(pid, sid, "WH1", 10, "in")
    ops = Operation.all()
    assert ops and ops[-1][5] in ("in","out")

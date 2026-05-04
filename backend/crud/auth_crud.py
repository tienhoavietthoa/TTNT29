from sqlalchemy.orm import Session
from models.auth_models import Login, Level
from models.user_models import Account
from core.security import hash_password, verify_password

def create_login(
    db: Session,
    code_login: str,
    password: str,
    id_level: int,
    status_login: str = "OFF"
) -> Login:
    """Create new login account"""
    hashed_password = hash_password(password)
    db_login = Login(
        code_login=code_login,
        pass_login=hashed_password,
        id_level=id_level,
        status_login=status_login
    )
    db.add(db_login)
    db.commit()
    db.refresh(db_login)
    return db_login

def get_login_by_code(db: Session, code_login: str) -> Login:
    """Get login by code"""
    return db.query(Login).filter(Login.code_login == code_login).first()

def get_login_by_id(db: Session, id_login: int) -> Login:
    """Get login by id"""
    return db.query(Login).filter(Login.id_login == id_login).first()

def authenticate_login(
    db: Session,
    code_login: str,
    password: str
) -> Login:
    """Authenticate login"""
    user = get_login_by_code(db, code_login)
    if not user:
        return None
    if not verify_password(password, user.pass_login):
        return None
    return user

def update_login_password(
    db: Session,
    id_login: int,
    new_password: str
) -> Login:
    """Update login password"""
    db_login = get_login_by_id(db, id_login)
    if not db_login:
        return None
    db_login.pass_login = hash_password(new_password)
    db.commit()
    db.refresh(db_login)
    return db_login

def update_login_status(
    db: Session,
    id_login: int,
    status: str
) -> Login:
    """Update login status"""
    db_login = get_login_by_id(db, id_login)
    if not db_login:
        return None
    db_login.status_login = status
    db.commit()
    db.refresh(db_login)
    return db_login

def get_all_levels(db: Session):
    """Get all levels"""
    return db.query(Level).all()

def create_account(
    db: Session,
    name_account: str,
    email_account: str,
    phone_account: str,
    id_login: int
) -> Account:
    """Create account"""
    db_account = Account(
        name_account=name_account,
        email_account=email_account,
        phone_account=phone_account,
        id_login=id_login
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def get_account_by_id(db: Session, id_account: int) -> Account:
    """Get account by id"""
    return db.query(Account).filter(Account.id_account == id_account).first()

def get_account_by_login_id(db: Session, id_login: int) -> Account:
    """Get account by login id"""
    return db.query(Account).filter(Account.id_login == id_login).first()

def update_account(
    db: Session,
    id_account: int,
    name_account: str = None,
    phone_account: str = None
) -> Account:
    """Update account"""
    db_account = get_account_by_id(db, id_account)
    if not db_account:
        return None
    if name_account:
        db_account.name_account = name_account
    if phone_account:
        db_account.phone_account = phone_account
    db.commit()
    db.refresh(db_account)
    return db_account
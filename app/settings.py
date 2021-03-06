from app import db
from app.models import Setting


def getSetting(name: str, default: str = "") -> str:
    value = Setting.query.filter_by(name=name).first()
    if value is None:
        value = default
    return str(value)


def saveSetting(name: str, value: str) -> bool:
    setting = Setting.query.filter_by(name=name).first()
    if setting is None:
        setting = Setting(name=name, value=value)
    else:
        setting.value = value
    db.session.add(setting)
    db.session.commit()
    return True

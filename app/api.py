from flask import current_app
import requests
from requests.exceptions import RequestException
from requests.models import HTTPBasicAuth
from app import db
from app.models import GlobalQueue, Domain, DomainQueue
from app.settings import getSetting, saveSetting
from datetime import datetime
import json


def testConnection(username: str, password: str) -> dict:
    base_url = current_app.config['EQAPI_URL']
    url = base_url + 'stats'
    try:
        r = requests.get(url, auth=HTTPBasicAuth(username, password))
    except RequestException as e:
        return {'status': False, 'message': f"Error {e}"}

    if r.status_code == 200:
        return {'status': True}
    elif r.status_code == 401:
        return {'status': False, 'message': 'Invalid username or password'}
    elif r.status_code == 403:
        return {'status': False, 'message': 'User not authorized to use API'}
    elif r.status_code == 500:
        return {'status': False, 'message': 'Remote server error'}
    else:
        return {'status': False, 'message': f"Error {r.status_code}"}


def queryQueue() -> bool:
    base_url = current_app.config['EQAPI_URL']
    url = base_url + 'stats'
    username = getSetting('api_username')
    password = getSetting('api_password')
    utcdatestr = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
    utcdate = datetime.utcnow()

    try:
        r = requests.get(url, auth=HTTPBasicAuth(username, password))
    except RequestException as e:
        saveSetting('lastError', f"{utcdatestr}: {e}")
        return False

    if r.status_code == 401:
        saveSetting('lastError', f"{utcdatestr}: Invalid username or password")
        return False
    elif r.status_code == 403:
        saveSetting('lastError', f"{utcdatestr}: User unauthorized to use API")
        return False
    elif r.status_code == 500:
        saveSetting('lastError', f"{utcdatestr}: Remote server error")
        return False
    elif r.status_code != 200:
        saveSetting('lastError', f"{utcdatestr}: Error {r.status_code}")
        return False

    data = json.loads(r.content)

    # Global

    gq = GlobalQueue(
        datetime=utcdate,
        TotalMessagesInbound=data['TotalMessagesInbound'],
        TotalMessagesOutbound=data['TotalMessagesOutbound'],
        MeanTimeInQueueInbound=data['MeanTimeInQueueInbound'],
        MeanTimeInQueueOutbound=data['MeanTimeInQueueOutbound'],
        LongestTimeInInbound=data['LongestTimeInInbound'],
        LongestTimeInOutbound=data['LongestTimeInOutbound'],
    )

    db.session.add(gq)
    db.session.commit()

    # Domains

    for qdomain in data['Domains']:
        domain = Domain.query.filter_by(domainname=qdomain['Name']).first()

        if domain is None:
            domain = Domain(domainname=qdomain['Name'])

        dq = DomainQueue(
            domain=domain.id,
            datetime=utcdate,
            ReceiveQueueCountInbound=qdomain['ReceiveQueueCountInbound'],
            ReceiveQueueCountOutbound=qdomain['ReceiveQueueCountOutbound'],
            DeliveryQueueCountInbound=qdomain['DeliveryQueueCountInbound'],
            DeliveryQueueCountOutbound=qdomain['DeliveryQueueCountOutbound'],
            LongestTimeInReceiveQueueInbound=qdomain['LongestTimeInReceiveQueueInbound'],  # noqa E501
            LongestTimeInReceiveQueueOutbound=qdomain['LongestTimeInReceiveQueueOutbound'],  # noqa E501
            LongestTimeInDeliveryQueueInbound=qdomain['LongestTimeInDeliveryQueueInbound'],  # noqa E501
            LongestTimeInDeliveryQueueOutbound=qdomain['LongestTimeInDeliveryQueueOutbound'],  # noqa E501
            MeanTimeInReceiveQueueInbound=qdomain['MeanTimeInReceiveQueueInbound'],  # noqa E501
            MeanTimeInReceiveQueueOutbound=qdomain['MeanTimeInReceiveQueueOutbound'],  # noqa E501
            MeanTimeInDeliveryQueueInbound=qdomain['MeanTimeInDeliveryQueueInbound'],  # noqa E501
            MeanTimeInDeliveryQueueOutbound=qdomain['MeanTimeInDeliveryQueueOutbound'],  # noqa E501
        )

        domain.stats.append(dq)
        db.session.add(domain)
        db.session.commit()

    return True

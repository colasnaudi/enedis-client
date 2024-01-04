import os
from dotenv import load_dotenv
import datetime
import lowatt_enedis
import lowatt_enedis.services

load_dotenv()

config = {
    'login': os.environ.get("ENEDIS_LOGIN"),
    'certificateFile': os.environ.get("ENEDIS_CERT_FILE"),
    'keyFile': os.environ.get("ENEDIS_KEY_FILE"),
    'prm': os.environ.get("ENEDIS_CONTRAT"),
}
# get client for the 'details' service using appropriate client
# certificate and key
client = lowatt_enedis.get_client(
    lowatt_enedis.COMMAND_SERVICE['details'][0],
    config['certificateFile'], config['keyFile'],
)

print(client)
# actually call the web to get values for the past week
resp = lowatt_enedis.services.point_detailed_measures(client, {
    'login': config['login'],
    'prm': config['prm'],
    'type': 'COURBE',
    'courbe_type': 'PA',
    'corrigee': True,
    'from': datetime.date.today() - datetime.timedelta(days=7),
    'to': datetime.date.today(),
})
# get a list of (UTC timestamp, value(W))
data = lowatt_enedis.services.measures_resp2py(resp)
cd F:\portableSoftware\google-cloud-sdk\platform\google_appengine
python dev_appserver.py --clear_datastore=yes C:\Users\servill7\git\GAE\MadMeteo\app.yaml

cd C:\Users\servill7\git\GAE\MadMeteo
pip install -t lib/ beautifulsoup4


gcloud --verbosity debug app deploy app.yaml --project testendpoint-162810
gcloud --verbosity debug app deploy app.yaml --project mad-meteo

CLEAR Local Datastore
cd F:\portableSoftware\google-cloud-sdk\platform\google_appengine
python dev_appserver.py --clear_datastore=yes C:\Users\servill7\git\GAE\MadMeteo\app.yaml


TODO
Aggregazione Previsioni
- AccuWeather
- Windy
- Forecast.io
- OpenWeatherMap
- Yahoo

Visualizzazione previsioni pi� dinamica

Aggiustare Web Scraping 3bmeteo

Grafici pioggia/temperatura

Statistiche visualizzazione

Tasto condividi
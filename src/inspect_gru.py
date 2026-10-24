# src/inspect_gru.py
import zipfile, json

for f in ['models/gru_next_purchase.keras', 'models/gru_sales_forecast.keras']:
    print(f'\n=== {f} ===')
    with zipfile.ZipFile(f) as z:
        with z.open('config.json') as c:
            config = json.load(c)
            for layer in config['config']['layers']:
                name = layer['class_name']
                cfg = layer['config']
                if name == 'InputLayer':
                    print('InputLayer - batch_shape:', cfg.get('batch_shape'))
                elif name == 'GRU':
                    print('GRU - units:', cfg.get('units'), '| return_sequences:', cfg.get('return_sequences'))
                elif name == 'Dropout':
                    print('Dropout - rate:', cfg.get('rate'))
                elif name == 'Dense':
                    print('Dense - units:', cfg.get('units'), '| activation:', cfg.get('activation'))
                elif name == 'Masking':
                    print('Masking - mask_value:', cfg.get('mask_value'))
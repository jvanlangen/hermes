import json, os, pathlib, secrets, time, urllib.request
root = pathlib.Path('/opt/data')
root.mkdir(parents=True, exist_ok=True)
base = f"http://{os.environ['SPARK_IP']}:{os.getenv('SPARK_PORT', '8000')}/v1"
key = os.getenv('SPARK_API_KEY') or 'local-no-key'
for attempt in range(30):
    try:
        req = urllib.request.Request(base + '/models', headers={'Authorization': 'Bearer ' + key})
        with urllib.request.urlopen(req, timeout=10) as response:
            models = json.load(response)['data']
        break
    except Exception as exc:
        if attempt == 29:
            raise SystemExit(f'Spark niet bereikbaar: {base}/models ({exc})')
        time.sleep(2)
selected = os.getenv('SPARK_MODEL')
if selected:
    model = next((m for m in models if m['id'] == selected), None)
    if model is None:
        raise SystemExit('SPARK_MODEL niet gevonden op de Spark')
else:
    if len(models) != 1:
        raise SystemExit('Meerdere modellen gevonden: stel SPARK_MODEL in')
    model = models[0]
context = int(os.getenv('SPARK_CONTEXT') or model.get('max_model_len') or 16384)
config_path = root / 'config.yaml'
# JSON is a valid YAML subset; keep other user settings on subsequent starts.
if config_path.exists():
    import yaml
    config = yaml.safe_load(config_path.read_text()) or {}
else:
    config = {}
config['model'] = {'default': model['id'], 'provider': 'custom', 'base_url': base, 'context_length': context}
config.setdefault('terminal', {}).update({'backend': 'local', 'cwd': '/opt/data/workspace'})
config.setdefault('auxiliary', {})['compression'] = {'provider': 'main', 'timeout': 300}
config_path.write_text(json.dumps(config, indent=2) + '\n')
secret_path = root / '.env'
existing = secret_path.read_text().splitlines() if secret_path.exists() else []
values = {}
for line in existing:
    if '=' in line and not line.startswith('#'):
        k, v = line.split('=', 1)
        values[k] = v
values.update({'OPENAI_BASE_URL': base, 'OPENAI_API_KEY': key, 'API_SERVER_ENABLED': 'true', 'API_SERVER_HOST': '0.0.0.0', 'API_SERVER_PORT': '8642', 'API_SERVER_MODEL_NAME': 'hermes-agent'})
values.setdefault('API_SERVER_KEY', secrets.token_hex(32))
secret_path.write_text(''.join(f'{k}={v}\n' for k, v in values.items()))
secret_path.chmod(0o600)
(root / 'workspace').mkdir(exist_ok=True)
web = pathlib.Path('/web-config'); web.mkdir(exist_ok=True)
(web / 'hermes.key').write_text(values['API_SERVER_KEY'])
for path in [root, config_path, secret_path, root / 'workspace']:
    os.chown(path, 10000, 10000)
print(f'Geconfigureerd: {model["id"]}, context {context}, endpoint {base}')

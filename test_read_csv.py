import sys

path = 'phishing_email.csv'
try:
    with open(path, 'rb') as f:
        data = f.read()
    print('Bytes read:', len(data))
    preview = data[:400]
    print(preview.decode('utf-8', errors='replace'))
except Exception as e:
    print('Error reading file:', e)
    sys.exit(1)

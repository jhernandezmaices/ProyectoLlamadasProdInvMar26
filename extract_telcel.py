import re
import csv
import subprocess

result = subprocess.run(['pdftotext', '-layout', 'Telcel Unisem.pdf', '-'], capture_output=True, text=True)
text = result.stdout

calls = []
lines = text.split('\n')

current_phone = ''

for line in lines:
    phone_match = re.search(r'Tel[eé]fono:\s*(\d{10,})', line)
    if phone_match:
        current_phone = phone_match.group(1)
        continue
    
    if not current_phone:
        continue
    
    if not line.strip():
        continue
    
    match = re.match(r'^\s*(\d{2}-[A-Za-z]{3})\s+(\d{2}:\d{2}:\d{2})', line)
    if not match:
        continue
    
    fecha = match.group(1)
    hora = match.group(2)
    
    rest = line[match.end():].strip()
    
    if rest.startswith('ENTRANTE'):
        continue
    
    phone_matches = re.findall(r'(\d{10,})', rest)
    if not phone_matches:
        continue
    
    destino = phone_matches[0]
    
    duracion_match = re.search(r'\s+(\d+)\s+\d+\s+\$', line)
    if not duracion_match:
        continue
    
    duracion = duracion_match.group(1)
    
    calls.append({
        'NumeroOrigen': current_phone,
        'NumeroDestino': destino,
        'Fecha': fecha,
        'Hora': hora,
        'Duracion': duracion
    })

print(f"Total llamadas extraídas: {len(calls)}")

unique_phones = set(c['NumeroOrigen'] for c in calls)
print(f"Números origen encontrados: {len(unique_phones)}")

with open('TelcelConcentradoLlamadas.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['NumeroOrigen', 'NumeroDestino', 'Fecha', 'Hora', 'Duracion'])
    writer.writeheader()
    writer.writerows(calls)

print(f"Archivo guardado: TelcelConcentradoLlamadas.csv")
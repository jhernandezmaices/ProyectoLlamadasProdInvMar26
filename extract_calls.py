import re
import csv

def extract_calls_from_pdf(pdf_path, numero_origen):
    import subprocess
    result = subprocess.run(['pdftotext', '-layout', pdf_path, '-'], capture_output=True, text=True)
    text = result.stdout
    
    calls = []
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
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
        
        destino = ''
        origen = numero_origen
        
        phone_matches = re.findall(r'(\d{10,})', rest)
        if phone_matches:
            destino = phone_matches[0]
        else:
            continue
        
        duracion_match = re.search(r'\s+(\d+)\s+\d+\s+\$', line)
        if not duracion_match:
            continue
        
        duracion = duracion_match.group(1)
        
        calls.append({
            'NumeroOrigen': numero_origen,
            'NumeroDestino': destino,
            'Fecha': fecha,
            'Hora': hora,
            'Duracion': duracion
        })
    
    return calls

pdfs = [
    ("Jaime 6871200911.pdf", "6871200911"),
    ("Mario Delgado 3757560275.pdf", "3757560275"),
    ("Mario Samuel 3321831266.pdf", "3321831266")
]

all_calls = []

for pdf, numero in pdfs:
    calls = extract_calls_from_pdf(pdf, numero)
    all_calls.extend(calls)
    print(f"{pdf}: {len(calls)} llamadas extraídas")

with open('ConcentradoLlamadas.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['NumeroOrigen', 'NumeroDestino', 'Fecha', 'Hora', 'Duracion'])
    writer.writeheader()
    writer.writerows(all_calls)

print(f"\nTotal: {len(all_calls)} llamadas guardadas en ConcentradoLlamadas.csv")
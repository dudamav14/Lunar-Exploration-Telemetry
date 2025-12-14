FROM python:3.11-slim
WORKDIR /app

ENV PYTHONUNBUFFERED=1     
# ¿?

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
 
# copia este archivo dentro del contenedor
COPY producer_mobility.py .
COPY producer_eclss.py .           
COPY producer_hga.py .

CMD ["python", "-u", "producer_mobility.py"]   
# ¿? Usamos -u principalmente con uso de buensa prácticas para depurar que datos se están enviando en tiempo real a la DB y printearlos todos cuando el buffer se llena

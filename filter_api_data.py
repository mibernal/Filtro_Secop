import pandas as pd
from sodapy import Socrata

def render_table(data):
    table = pd.DataFrame.from_records(data)
    print(table)

# Autenticación del cliente con el token de la aplicación y las credenciales de usuario
client = Socrata("www.datos.gov.co", "qrWbZ9mhsAXj6S0L2U3LMV2YF", username="miguelangelbernal1991@gmail.com", password="Mid@910625")

# Obtener los resultados de la consulta
results = client.get("f789-7hwg", where="fecha_de_firma_del_contrato BETWEEN '2019-01-01' AND '" + pd.Timestamp.now().strftime('%Y-%m-%d') + "'", municipio_entidad="Cachipay", limit=5000)

# Renderizar la tabla
render_table(results)

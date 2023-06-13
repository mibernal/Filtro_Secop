import pandas as pd
from sodapy import Socrata

# Autenticación del cliente con el token de la aplicación y las credenciales de usuario
client = Socrata("www.datos.gov.co", "qrWbZ9mhsAXj6S0L2U3LMV2YF", username="miguelangelbernal1991@gmail.com", password="Mid@910625")

# Obtener los resultados de la consulta
results = client.get("f789-7hwg", nombre_entidad="CUNDINAMARCA ALCALDIA MUNICIPIO DE CACHIPAY", limit=2000)

# Convertir los resultados en un DataFrame de pandas
results_df = pd.DataFrame.from_records(results)

# Imprimir el DataFrame
print(results_df)

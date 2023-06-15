import pandas as pd
from sodapy import Socrata
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def render_table(data, output_format, sheet_name, workbook):
    table = pd.DataFrame.from_records(data)

    if output_format == 'csv':
        table.to_csv('output.csv', index=False)
        print("Datos guardados en output.csv")
    elif output_format == 'excel':
        sheet = workbook.create_sheet(title=sheet_name)

        columns_with_dicts = [col for col in table.columns if table[col].apply(lambda x: isinstance(x, dict)).any()]
        table = table.drop(columns=columns_with_dicts)

        for row in dataframe_to_rows(table, index=False, header=True):
            sheet.append(row)

        print(f"Datos guardados en {sheet_name}")
    else:
        print("Formato de salida no válido. Use 'csv' o 'excel'.")

# Autenticación del cliente con el token de la aplicación y las credenciales de usuario
client = Socrata("www.datos.gov.co", "qrWbZ9mhsAXj6S0L2U3LMV2YF", username="miguelangelbernal1991@gmail.com", password="Mid@910625")

# Diccionario de criterios de búsqueda para cada API
search_criteria = {
    "https://dev.socrata.com/foundry/www.datos.gov.co/f789-7hwg": {
        "sheet_name": "SECOPI-CompraPública",
        "filter": "municipio_entidad = 'Cachipay' AND fecha_de_firma_del_contrato BETWEEN '2019-01-01' AND '" + pd.Timestamp.now().strftime('%Y-%m-%d') + "'"
    },
    "https://dev.socrata.com/foundry/www.datos.gov.co/jbjy-vk9h": {
        "sheet_name": "SECOPII-ContratosElectrónicos",
        "filter": "nit_entidad = '800081091' AND fecha_de_firma BETWEEN '2019-01-01' AND '" + pd.Timestamp.now().strftime('%Y-%m-%d') + "'"
    },
    "https://dev.socrata.com/foundry/www.datos.gov.co/p6dx-8zbt":
     {
        "sheet_name": "SECOPII-ProcesosdeContratación",
        "filter": "ciudad_entidad = 'Cachipay' AND fecha_de_publicacion_del BETWEEN '2019-01-01' AND '" + pd.Timestamp.now().strftime('%Y-%m-%d') + "'"
    },
    "https://dev.socrata.com/foundry/www.datos.gov.co/wi7w-2nvm": {
        "sheet_name": "SECOPII-OfertasPorProceso",
        "filter": "nit_entidad_compradora = '800081091' AND fecha_de_registro BETWEEN '2019-01-01' AND '" + pd.Timestamp.now().strftime('%Y-%m-%d') + "'"
    },
    "https://dev.socrata.com/foundry/www.datos.gov.co/rpmr-utcd": {
        "sheet_name": "SECOPIntegrado",
        "filter": "nit_de_la_entidad = '890981567-1'"
    }
}

# Crear un nuevo libro de trabajo (workbook)
workbook = Workbook()

# Realizar la consulta en cada API y guardar los resultados en hojas separadas
for api_url, criteria in search_criteria.items():
    dataset_id = api_url.split("/")[-1]
    sheet_name = criteria["sheet_name"]
    filter = criteria["filter"]

    results = client.get(dataset_id, where=filter, limit=5000)

    render_table(results, output_format='excel', sheet_name=sheet_name, workbook=workbook)

# Eliminar la hoja inicial que se crea por defecto
workbook.remove(workbook.active)

# Guardar el libro de trabajo (workbook) en el archivo
workbook.save('output.xlsx')
print("Archivo guardado correctamente.")

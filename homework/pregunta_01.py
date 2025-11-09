"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
  """
  Construya y retorne un dataframe de Pandas a partir del archivo
  'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

  - El dataframe tiene la misma estructura que el archivo original.
  - Los nombres de las columnas deben ser en minusculas, reemplazando los
    espacios por guiones bajos.
  - Las palabras clave deben estar separadas por coma y con un solo
    espacio entre palabra y palabra.

  """
  import pandas as pd
  import re

  path = "files/input/clusters_report.txt"
  records = []

  with open(path, encoding="utf-8") as f:
    lines = f.readlines()

  data_lines = []
  dashed_found = False
  for ln in lines:
    if re.match(r"^-{5,}", ln):
      dashed_found = True
      continue
    if not dashed_found:
      continue
    data_lines.append(ln.rstrip("\n"))

  current = None
  for ln in data_lines:
    m = re.match(r"^\s*(\d+)\s+(\d+)\s+([\d,]+\s*%)\s*(.*)$", ln)
    if m:
      if current is not None:
        kw = " ".join(current["keywords_lines"]).strip()
        kw = re.sub(r"\s+", " ", kw)
        kw = re.sub(r"\s*,\s*", ", ", kw)
        current["principales_palabras_clave"] = kw.strip()
        por = current["porcentaje"].strip().replace("%", "").replace(" ", "").replace(",", ".")
        por = float(por)
        records.append({
          "cluster": int(current["cluster"]),
          "cantidad_de_palabras_clave": int(current["cantidad"]),
          "porcentaje_de_palabras_clave": por,
          "principales_palabras_clave": current["principales_palabras_clave"],
        })

      current = {
        "cluster": m.group(1),
        "cantidad": m.group(2),
        "porcentaje": m.group(3),
        "keywords_lines": [],
      }
      rest = m.group(4)
      if rest:
        current["keywords_lines"].append(rest)
    else:
      if ln.strip() == "":
        continue
      if current is not None:
        current["keywords_lines"].append(ln.strip())

  if current is not None:
    kw = " ".join(current["keywords_lines"]).strip()
    kw = re.sub(r"\s+", " ", kw)
    kw = re.sub(r"\s*,\s*", ", ", kw)
    current["principales_palabras_clave"] = kw.strip()
    por = current["porcentaje"].strip().replace("%", "").replace(" ", "").replace(",", ".")
    por = float(por)
    records.append({
      "cluster": int(current["cluster"]),
      "cantidad_de_palabras_clave": int(current["cantidad"]),
      "porcentaje_de_palabras_clave": por,
      "principales_palabras_clave": current["principales_palabras_clave"],
    })

  df = pd.DataFrame(records)

  df.columns = [c.lower().replace(" ", "_") for c in df.columns]

  df["principales_palabras_clave"] = df["principales_palabras_clave"].str.rstrip('.')

  return df

"""Pruebas automáticas con unittest (incluido en Python)."""
import unittest
from pathlib import Path
from src.pipeline import extraer, limpiar_clientes, transformar_ventas, integrar, validar, guardar_procesados

ROOT = Path(__file__).resolve().parents[1]


class TestPipeline(unittest.TestCase):
    def setUp(self):
        clientes, enero, febrero = extraer(ROOT / "data" / "raw")
        self.clientes, _ = limpiar_clientes(clientes)
        self.ventas = transformar_ventas(enero, febrero)
        self.resultado = integrar(self.ventas, self.clientes)

    def test_conserva_registros_y_total(self):
        r = validar(self.resultado, self.ventas)
        self.assertEqual(r["ventas_entrada"], 6)
        self.assertEqual(r["ventas_salida"], 6)
        self.assertEqual(r["total_reportado"], 739000)

    def test_detecta_anomalias(self):
        r = validar(self.resultado, self.ventas)
        self.assertEqual(r["ventas_sin_cliente"], 1)
        self.assertEqual(r["fechas_invalidas"], 1)
        self.assertEqual(r["totales_inconsistentes"], 1)

    def test_guarda_procesados(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as temporal:
            carpeta = Path(temporal)
            guardar_procesados(self.clientes, self.ventas, carpeta)
            self.assertTrue((carpeta / "clientes_limpios.csv").exists())
            self.assertTrue((carpeta / "ventas_transformadas.csv").exists())

    def test_normaliza_ciudades_y_clientes(self):
        self.assertEqual(len(self.clientes), 3)
        self.assertEqual(set(self.clientes["ciudad"]), {"IBAGUE", "BOGOTA"})


if __name__ == "__main__":
    unittest.main()

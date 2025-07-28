class Statistics:
    def __init__(self, datos):
        self.datos = datos.copy()

    def calcular_estadisticas(self):
        self.datos['precio_m2'] = self.datos['precio'] / self.datos['area']

        def clasificar_tipo(desc):
            if isinstance(desc, str):
                if 'casa' in desc.lower():
                    return 'Casa'
                elif 'apartamento' in desc.lower():
                    return 'Apartamento'
            return 'Otro'
        
        self.datos['tipo_vivienda'] = self.datos['descripcion'].apply(clasificar_tipo)
        conteo_tipo = self.datos['tipo_vivienda'].value_counts()

        estadisticas = {
            'total_viviendas': len(self.datos),
            'precio_promedio': f"{self.datos['precio'].mean():,.0f}",
            'area_promedio': f"{self.datos['area'].mean():,.0f}",
            'precio_m2_promedio': f"{self.datos['precio_m2'].mean():,.0f}",
            'casas_count': conteo_tipo.get('Casa', 0),
            'apartamentos_count': conteo_tipo.get('Apartamento', 0),
            'otros_count': conteo_tipo.get('Otro', 0),
            'precio_min': f"{self.datos['precio'].min():,.0f}",
            'precio_max': f"{self.datos['precio'].max():,.0f}",
        }
        return estadisticas

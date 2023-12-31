def load_quarters():
    from ..models import Quarters
    BARRIOS = [
        ("Altamira", "Altamira",""),
        ("Barrio Bonito", "Barrio Bonito",""),
        ("Bellavista", "Bellavista",""),
        ("Betania", "Betania",""),
        ("Brisas del Llano", "Brisas del Llano",""),
        ("Cataluña", "Cataluña",""),
        ("Daniel Jordan y Minuto de Dios", "Daniel Jordan y Minuto de Dios",""),
        ("Doce de Octubre", "Doce de Octubre",""),
        ("El Chaparral", "El Chaparral",""),
        ("El limonar", "El limonar",""),
        ("El Mirador", "El Mirador",""),
        ("El Portal de Los Patios", "El Portal de Los Patios",""),
        ("El Sol", "El Sol",""),
        ("Iscaligua I", "Iscaligua I",""),
        ("Iscaligua II", "Iscaligua II",""),
        ("Juana Paula", "Juana Paula",""),
        ("Kilometro Nueve", "Kilometro Nueve",""),
        ("Kilometro Ocho", "Kilometro Ocho",""),
        ("La Arboleda", "La Arboleda",""),
        ("La Campiña", "La Campiña",""),
        ("La Cordialidad", "La Cordialidad",""),
        ("La Esperanza", "La Esperanza",""),
        ("La Floresta", "La Floresta",""),
        ("La Sabana", "La Sabana",""),
        ("Las Cumbres", "Las Cumbres",""),
        ("Llanitos", "Llanitos",""),
        ("Llano Grande", "Llano Grande",""),
        ("Los Colorados", "Los Colorados",""),
        ("Miradores del Pamplonita", "Miradores del Pamplonita",""),
        ("Nazaret", "Nazaret",""),
        ("Once de Noviembre", "Once de Noviembre",""),
        ("Patio Antiguo", "Patio Antiguo",""),
        ("Patios Centro", "Patios Centro",""),
        ("Pensilvania", "Pensilvania",""),
        ("Pinar del rio", "Pinar del rio",""),
        ("Pisarreal", "Pisarreal",""),
        ("San Carlos", "San Carlos",""),
        ("San Fernando", "San Fernando",""),
        ("San Francisco", "San Francisco",""),
        ("San Remo", "San Remo",""),
        ("San Victorino", "San Victorino",""),
        ("Santa Ana", "Santa Ana",""),
        ("Santa Clara", "Santa Clara",""),
        ("Santa Rosa de Lima", "Santa Rosa de Lima",""),
        ("Sinai", "Sinai",""),
        ("Tasajero", "Tasajero",""),
        ("Tierra Linda", "Tierra Linda",""),
        ("Valles del Mirador", "Valles del Mirador",""),
        ("Videlso", "Videlso",""),
        ("Villa Betania", "Villa Betania",""),
        ("Villa Camila", "Villa Camila",""),
        ("Villa Celina", "Villa Celina",""),
        ("Villa Esperanza", "Villa Esperanza",""),
        ("Villa Sonia", "Villa Sonia",""),
        ("Villa Verde", "Villa Verde","")
    ]

    VEREDAS = [
        ("Agualinda", "Agualinda",""),
        ("California", "California",""),
        ("Colchones", "Colchones",""),
        ("Corozal", "Corozal",""),
        ("Helechal Alto", "Helechal Alto",""),
        ("Helechal Bajo", "Helechal Bajo",""),
        ("La Mutis", "La Mutis",""),
        ("Los Vados", "Los Vados",""),
        ("Trapiches", "Trapiches",""),
        ("Veinte de Julio", "Veinte de Julio",""),
        ("Villas de Corozal", "Villas de Corozal","")
    ]

    QUARTERS = BARRIOS + VEREDAS

    for item in QUARTERS:
        Quarters.objects.get_or_create(name=item[0], commune=item[2])
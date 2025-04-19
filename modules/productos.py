class Producto:
    def __init__(self,id_producto,n_producto,descripcion,cantidad,categoria,marca,color,medida,cv,pvp,imagen):
        self.id_producto=id_producto
        self.n_producto=n_producto
        self.descripcion=descripcion
        self.cantidad= cantidad
        self.categoria=categoria
        self.marca=marca
        self.color=color
        self.medida=medida
        self.cv=cv
        self.pvp=pvp
        self.imagen=imagen

        


    def ProductoDBCollection(self):
        return{
            "id_producto":self.id_producto,
            "n_producto":self.n_producto,
            "descripcion":self.descripcion,
            "cantidad":self.cantidad,
            "categoria":self.categoria,
            "marca":self.marca,
            "color":self.color,
            "medida":self.medida,
            "cv":self.cv,
            "pvp":self.pvp,
            "imagen":self.imagen
            
        }
class Stock:
    def __init__(self, st_id,fecha,producto,id_producto,c_producto,precio,cantidad,total,usuario,comentario):
        self.st_id = st_id
        self.fecha=fecha
        self.producto=producto
        self.id_producto=id_producto
        self.c_producto=c_producto
        self.precio=precio
        self.cantidad=cantidad
        self.total=total
        self.usuario=usuario
        self.comentario=comentario
        

    def StockDBCollection(self):
        return{
            "st_id":self.st_id,
            "fecha":self.fecha,
            "producto":self.producto,
            "id_producto":self.id_producto,
            "c_producto":self.c_producto,
            "precio":self.precio,
            "cantidad":self.cantidad,
            "total":self.total,
            "usuario":self.usuario,
            "comentario":self.comentario
            
        }
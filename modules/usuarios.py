class Usuario:
    def __init__(self, cedula,user,correo,direccion,contraseña, rol,imagen):
        self.cedula=cedula
        self.user=user
        self.correo=correo
        self.direccion=direccion
        self.contraseña=contraseña
        self.rol = rol
        self.imagen=imagen
        

    def UsuarioDBCollection(self):
        return{
            "cedula":self.cedula,
            "user":self.user,
            "correo":self.correo,
            "direccion":self.direccion,
            "contraseña":self.contraseña,
            "rol": self.rol,
            "imagen":self.imagen
        }
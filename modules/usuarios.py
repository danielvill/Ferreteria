class Usuario:
    def __init__(self, cedula,user,correo,contraseña, rol="usuario"):
        self.cedula=cedula
        self.user=user
        self.correo=correo
        self.contraseña=contraseña
        self.rol = rol
        

    def UsuarioDBCollection(self):
        return{
            "cedula":self.cedula,
            "user":self.user,
            "correo":self.correo,
            "contraseña":self.contraseña,
            "rol": self.rol
        }
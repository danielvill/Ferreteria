class Admin:
    def __init__(self, user,contraseña):
        self.user = user
        self.contraseña = contraseña
        

    def AdminDBCollection(self):
        return{
            "user":self.user,
            "contraseña":self.contraseña,
            
        }
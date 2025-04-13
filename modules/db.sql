
create table producto(
    id_producto int primary key auto_increment,
    n_producto varchar(50) not null,
    descripcion varchar(200) not null,
    cantidad int not null,
    categoria varchar(50) ,
    marca  varchar(50) ,
    color varchar(50) ,
    medida decimal(50) ,
    cv decimal(10,2) ,
    pvp decimal(10,2) ,
),


create table stock(
    st_id int primary key auto_increment,
    fecha date not null,
    producto varchar(50) ,
    id_producto int not null,
    c_producto int not null,
    precio decimal(10,2) ,
    cantidad int not null,
    total decimal(10,2) ,
    usuario varchar(50) ,
    foreign key (id_producto) references producto(id_producto),
),

create table usuarios(
    cedula int primary key ,
    user varchar(50) not null,
    correo varchar(50) not null,
    contrasena varchar(50) not null,
    rol varchar(50) not null,

)


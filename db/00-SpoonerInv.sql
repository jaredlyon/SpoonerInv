drop database if exists `SpoonerInv`;
create database if not exists `SpoonerInv`;

use SpoonerInv;

grant all privileges on SpoonerInv.* to 'webapp'@'%';
flush privileges;

create table if not exists Ingredient
(
    ingredient_id   int primary key,
    name            varchar(50)        not null,
    quantity        int                not null,
    expiration_date date               not null
);

create table if not exists Stock
(
    stock_id        int primary key,
    order_date_time datetime           not null,
    name            varchar(50)        not null,
    quantity        int                not null
);

create table if not exists Supplier
(
    supplier_id int primary key,
    name        varchar(50) unique not null,
    street      varchar(50)        not null,
    city        varchar(50)        not null,
    zip         int                not null
);

create table if not exists Customer
(
    customer_id    int primary key,
    loyalty_points int,
    free_drink     boolean not null
);

create table if not exists Employee
(
    employee_id int primary key,
    phone       varchar(12),
    email       varchar(50),
    first_name  varchar(25),
    last_name   varchar(25),
    store_id    int not null
);

create table if not exists Region
(
    name       varchar(50) unique not null,
    region_id  int primary key
);

create table if not exists Store
(
    store_id  int primary key,
    hours     varchar(100),
    region_id int                not null,
    street varchar(75),
    city varchar(50),
    zip int,
    name      varchar(50) unique not null
);

create table if not exists `Order`
(
    order_id    int primary key,
    total_price float not null,
    store_id    int   not null,
    customer_id int   not null
);

create table if not exists Drink
(
    drink_id  int primary key,
    size      char  not null,
    sugar_lvl varchar(5),
    ice_lvl   varchar(15),
    price     float not null,
    order_id  int   not null
);

# generate foreign keys
alter table Employee
    add CONSTRAINT fk_1_employee
        FOREIGN KEY (store_id) references Store (store_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE;

alter table Store
    add CONSTRAINT fk_1_store
        FOREIGN KEY (region_id) references Region (region_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE;

alter table `Order`
    add CONSTRAINT fk_1_order
        FOREIGN KEY (store_id) references Store (store_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    add CONSTRAINT fk_2_order
        FOREIGN KEY (customer_id) references Customer (customer_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE;

alter table Drink
    add CONSTRAINT fk_1_drink
        FOREIGN KEY (order_id) references `Order` (order_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE;

# generate M:N relationship tables
create table if not exists Store_Stock
(
    store_id int not null,
    stock_id int not null,
    CONSTRAINT fk_1_store_stock FOREIGN KEY (store_id) references Store (store_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_2_store_stock FOREIGN KEY (stock_id) references Stock (stock_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

create table if not exists Drink_Recipe
(
    drink_id      int not null,
    ingredient_id int not null,
    CONSTRAINT fk_1_drink_recipe FOREIGN KEY (drink_id) references Drink (drink_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_2_drink_recipe FOREIGN KEY (ingredient_id) references Ingredient (ingredient_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

create table if not exists Ingredient_Recipe
(
    ingredient_id int not null,
    stock_id      int not null,
    CONSTRAINT fk_1_ingredient_recipe FOREIGN KEY (ingredient_id) references Ingredient (ingredient_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_2_ingredient_recipe FOREIGN KEY (stock_id) references Stock (stock_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

create table if not exists Stock_Order
(
    supplier_id int not null,
    stock_id    int not null,
    CONSTRAINT fk_1_stock_order FOREIGN KEY (supplier_id) references Supplier (supplier_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_2_stock_order FOREIGN KEY (stock_id) references Stock (stock_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
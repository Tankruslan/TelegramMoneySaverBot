create table budget(
    name varchar(255) primary key,
    daily_limit integer
);

create table category(
    name varchar(255) primary key,
    is_primary_expense boolean,
    aliases text
);

create table expense(
    id integer primary key,
    amount integer,
    created datetime,
    category_name integer,
    raw_text text,
    FOREIGN KEY(category_name) REFERENCES category(name)
);

insert into category (name, is_primary_expense, aliases)
values
    ("products", true, "food"),
    ("coffee", true, ""),
    ("dinner", true, ""),
    ("cafe", true, "kfc"),
    ("transport", false, "metro"),
    ("taxi", false, "yandex"),
    ("phone", false, "communication"),
    ("books", false, ""),
    ("internet", false, "inet, net"),
    ("subscriptions", false, ""),
    ("other", true, "");

insert into budget(name, daily_limit) values ('base', 100);
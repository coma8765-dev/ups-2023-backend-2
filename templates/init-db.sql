create table authors
(
	id serial,
	name varchar(200) not null,
	image_link varchar(500),
	birthdate timestamp not null,
	death_date timestamp,
	constraint authors_pkey
		primary key (id)
);

alter table authors owner to postgres;

create table books
(
	id serial,
	title varchar(500) not null,
	rental_limit interval,
	image_link varchar(300),
	author_id integer not null,
	constraint books_pkey
		primary key (id),
	constraint books_authors_id_fk
		foreign key (author_id) references authors
			on delete cascade
);

alter table books owner to postgres;

create table readers
(
	id serial,
	name varchar(100) not null,
	email varchar(200) not null,
	constraint readers_pkey
		primary key (id),
	constraint readers_email_key
		unique (email)
);

alter table readers owner to postgres;

create table rentals
(
	id serial,
	book_id integer not null,
	reader_id integer not null,
	start timestamp default now() not null,
	"end" timestamp,
	fine_amount integer not null,
	constraint rentals_pkey
		primary key (id),
	constraint rentals_books_id_fk
		foreign key (book_id) references books
			on delete cascade,
	constraint rentals_readers_id_fk
		foreign key (reader_id) references readers
			on delete cascade
);

alter table rentals owner to postgres;


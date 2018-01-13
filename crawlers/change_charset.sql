alter table job modify column state VARCHAR(256) character set utf8mb4 collate utf8mb4_unicode_ci not null;
alter table job modify column city VARCHAR(256) character set utf8mb4 collate utf8mb4_unicode_ci not null;
alter table job modify column title VARCHAR(256) character set utf8mb4 collate utf8mb4_unicode_ci not null;
alter table job modify column author VARCHAR(256) character set utf8mb4 collate utf8mb4_unicode_ci not null;
alter table job modify column description TEXT character set utf8mb4 collate utf8mb4_unicode_ci not null;

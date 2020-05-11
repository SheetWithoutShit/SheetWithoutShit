/*
    Table that stores user`s budget data.

    * id: incremental integer id.
    * income: user`s income for certain month.
    * savings: user`s savings for certain month in percents.
    * year: year of certain budget.
    * month: month of certain budget.
    * spreadsheet: spreadsheet id.
    * user_id: foreign key to budget owner.
*/

create table "BUDGET" (
	id serial constraint budget_pk primary key,
	income numeric(12, 2) default 0.00,
	savings smallint default 0,
	year smallint not null,
	month smallint not null,
	spreadsheet varchar,
	user_id int constraint budget_user_fk references "USER" on delete cascade not null
);

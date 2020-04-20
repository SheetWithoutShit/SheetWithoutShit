/*
    Table that stores Merchant Categories Codes.

    * code: category's code.
    * category: merchant category.
    * info: additional information about category.
*/

create table "MCC" (
	code int constraint mcc_pk primary key,
	category varchar not null,
	info varchar
);

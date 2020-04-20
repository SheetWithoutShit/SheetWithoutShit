/*
    Table that stores user data.

    * telegram_id: chat id in the telegram messenger.
    * first_name: user's first name.
    * last_name: user's last name.
    * monobank_token: token to interact with monobank API.
    * spreadsheet_refresh_token: token to refresh access token for interactions with google spreadsheet API.
*/

create table "USER"(
	telegram_id int constraint user_pk primary key,
	first_name varchar,
	last_name varchar,
	monobank_token varchar,
	spreadsheet_refresh_token varchar
);

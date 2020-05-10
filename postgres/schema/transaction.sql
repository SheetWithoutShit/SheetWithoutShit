/*
    Table that stores user`s transactions.

    * id: unique transaction id.
    * user_id: foreign key to transaction owner.
    * amount: amount of costs in the transaction.
    * balance: current user's balance after transaction.
    * cashback: amount of cashback for the transaction.
    * mcc: merchant category code of transaction.
    * timestamp: transaction time.
    * info: additional information about transaction.
*/

create table "TRANSACTION" (
    id varchar constraint transaction_pk primary key,
	user_id int constraint transaction_user_fk references "USER" on delete cascade not null,
	amount numeric(12, 2) not null,
	balance numeric(12, 2),
	cashback numeric(12, 2) default 0,
	mcc smallint constraint transaction_mcc_fk references "MCC" on delete set default default -1,
	timestamp timestamp default now(),
	info varchar
);

CREATE INDEX transaction_user_timestamp_idx ON "TRANSACTION" (user_id, timestamp);

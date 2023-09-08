CREATE TABLE "public.users" (
	"id" serial NOT NULL,
	"pass_hash" TEXT NOT NULL,
	"email" TEXT NOT NULL UNIQUE,
	"login" integer NOT NULL UNIQUE,
	CONSTRAINT "users_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);


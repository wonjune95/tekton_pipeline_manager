// ORM 의 안전한 사용 — 탐지되면 안 된다
import { Sequelize, QueryTypes } from "sequelize";
import { PrismaClient } from "@prisma/client";
import { DataSource } from "typeorm";

const sequelize = new Sequelize("sqlite::memory:");
const prisma = new PrismaClient();
declare const dataSource: DataSource;
declare const knex: any;

export async function find(req: any) {
  const q = req.query.q;
  // ok: mois-1-01-sql-injection-js replacements 로 값 전달
  await sequelize.query("SELECT * FROM Products WHERE name LIKE :q", { replacements: { q: `%${q}%` }, type: QueryTypes.SELECT });
  // ok: mois-1-01-sql-injection-js Prisma 태그 템플릿은 값을 바인딩한다
  await prisma.$queryRaw`SELECT * FROM post WHERE title = ${q}`;
  // ok: mois-1-01-sql-injection-js Knex 바인딩
  await knex("users").whereRaw("name = ?", [q]);
  // ok: mois-1-01-sql-injection-js Knex where 는 값을 바인딩한다
  await knex("users").where("name", q);
  // ok: mois-1-01-sql-injection-js TypeORM 이름 있는 매개변수
  await dataSource.createQueryBuilder().select("u").from("user", "u").where("u.name = :name", { name: q }).getMany();
  // ok: mois-1-01-sql-injection-js 정규식의 exec 는 SQL 이 아니다
  return /^(\d+)$/.exec(q);
}

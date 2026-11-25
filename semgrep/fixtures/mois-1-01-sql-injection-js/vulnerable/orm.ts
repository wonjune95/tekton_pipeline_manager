// ORM 의 원문 SQL 기능
import { Controller, Get, Query } from "@nestjs/common";
import { Sequelize } from "sequelize";
import { PrismaClient } from "@prisma/client";
import { DataSource } from "typeorm";

const sequelize = new Sequelize("sqlite::memory:");
const prisma = new PrismaClient();
declare const dataSource: DataSource;
declare const knex: any;

@Controller("search")
export class SearchController {
  @Get()
  async find(@Query("q") q: string, @Query("order") order: string) {
    // ruleid: mois-1-01-sql-injection-js
    await sequelize.query(`SELECT * FROM Products WHERE name LIKE '%${q}%'`);
    // ruleid: mois-1-01-sql-injection-js
    await prisma.$queryRawUnsafe("SELECT * FROM post WHERE title = '" + q + "'");
    // ruleid: mois-1-01-sql-injection-js
    await knex("users").whereRaw("name = '" + q + "'");
    // ruleid: mois-1-01-sql-injection-js
    await knex.raw(`select * from users order by ${order}`);
    // ruleid: mois-1-01-sql-injection-js
    await dataSource.getRepository("User").createQueryBuilder("u").where("u.name = '" + q + "'").getMany();
    const qb = dataSource.createQueryBuilder();
    // ruleid: mois-1-01-sql-injection-js
    qb.select("u").from("user", "u").orderBy(order);
    // ruleid: mois-1-01-sql-injection-js
    return sequelize.models.User.findAll({ where: Sequelize.literal("id = " + q) });
  }
}

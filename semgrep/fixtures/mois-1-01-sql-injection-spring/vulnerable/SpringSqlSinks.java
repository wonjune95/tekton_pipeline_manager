package demo;

import java.util.HashMap;
import org.hibernate.Session;
import org.hibernate.StatelessSession;
import org.springframework.jdbc.core.JdbcOperations;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcOperations;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.jdbc.core.support.JdbcDaoSupport;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

// sink 가지마다 한 줄씩: 수신 객체 타입별, 메서드별, 이름으로 잡는 형태(getJdbcTemplate() 등)
@RestController
public class SpringSqlSinks extends JdbcDaoSupport {
    private JdbcTemplate jdbc;
    private JdbcOperations jdbcOps;
    private NamedParameterJdbcTemplate named;
    private NamedParameterJdbcOperations namedOps;
    private javax.persistence.EntityManager em;
    private jakarta.persistence.EntityManager jakartaEm;
    private Session session;
    private StatelessSession statelessSession;
    private LegacyDao legacyDao;

    // JdbcTemplate 메서드별
    @GetMapping("/template")
    public void template(@RequestParam String keyword) {
        String sql = "SELECT name FROM owners WHERE last_name = '" + keyword + "'";
        // ruleid: mois-1-01-sql-injection-spring
        jdbc.query(sql, (rs, i) -> rs.getString(1));
        // ruleid: mois-1-01-sql-injection-spring
        jdbc.queryForObject(sql, String.class);
        // ruleid: mois-1-01-sql-injection-spring
        jdbc.queryForMap(sql);
        // ruleid: mois-1-01-sql-injection-spring
        jdbc.queryForRowSet(sql);
        // ruleid: mois-1-01-sql-injection-spring
        jdbc.queryForStream(sql, String.class);
        // ruleid: mois-1-01-sql-injection-spring
        jdbc.queryForLong(sql);
        // ruleid: mois-1-01-sql-injection-spring
        jdbc.queryForInt(sql);
        // ruleid: mois-1-01-sql-injection-spring
        jdbc.update(sql);
        // ruleid: mois-1-01-sql-injection-spring
        jdbc.execute(sql);
        // ruleid: mois-1-01-sql-injection-spring
        jdbc.batchUpdate(sql);
    }

    // 수신 객체 타입별: JdbcOperations, NamedParameterJdbcTemplate, NamedParameterJdbcOperations
    @GetMapping("/receivers")
    public void receivers(@RequestParam String keyword) {
        String sql = "SELECT name FROM owners WHERE last_name = '" + keyword + "'";
        // ruleid: mois-1-01-sql-injection-spring
        jdbcOps.queryForList(sql);
        // 이름 있는 파라미터를 쓰는 API 라도 질의문을 이어 붙이면 같다
        // ruleid: mois-1-01-sql-injection-spring
        named.queryForList(sql, new HashMap<String, Object>());
        // ruleid: mois-1-01-sql-injection-spring
        namedOps.update(sql, new HashMap<String, Object>());
    }

    // 타입을 알 수 없는 수신 객체: 이름에 jdbcTemplate·jdbcOperations 가 있는 경우
    @GetMapping("/by-name")
    public void byName(@RequestParam String keyword) {
        String sql = "SELECT name FROM owners WHERE last_name = '" + keyword + "'";
        // ruleid: mois-1-01-sql-injection-spring
        getJdbcTemplate().queryForList(sql);
        // ruleid: mois-1-01-sql-injection-spring
        legacyDao.jdbcTemplate.update(sql);
        // ruleid: mois-1-01-sql-injection-spring
        named.getJdbcOperations().execute(sql);
    }

    // JPA: javax·jakarta 네임스페이스, JPQL·네이티브 질의
    @GetMapping("/jpa")
    public void jpa(@RequestParam String keyword) {
        String jpql = "SELECT o FROM Owner o WHERE o.lastName = '" + keyword + "'";
        // ruleid: mois-1-01-sql-injection-spring
        em.createQuery(jpql);
        // ruleid: mois-1-01-sql-injection-spring
        em.createQuery(jpql, Object.class);
        // ruleid: mois-1-01-sql-injection-spring
        jakartaEm.createQuery(jpql);
        // ruleid: mois-1-01-sql-injection-spring
        jakartaEm.createNativeQuery("SELECT * FROM owners WHERE last_name = '" + keyword + "'", Object.class);
    }

    // Hibernate: Session·StatelessSession, 메서드별
    @GetMapping("/hibernate")
    public void hibernate(@RequestParam String keyword) {
        String hql = "from Owner where lastName = '" + keyword + "'";
        // ruleid: mois-1-01-sql-injection-spring
        session.createSQLQuery(hql);
        // ruleid: mois-1-01-sql-injection-spring
        session.createNativeQuery(hql);
        // ruleid: mois-1-01-sql-injection-spring
        session.createSelectionQuery(hql, Object.class);
        // ruleid: mois-1-01-sql-injection-spring
        session.createMutationQuery(hql);
        // ruleid: mois-1-01-sql-injection-spring
        session.createNativeMutationQuery(hql);
        // ruleid: mois-1-01-sql-injection-spring
        statelessSession.createQuery(hql);
    }

    // 숫자로 변환하긴 했지만 변환한 값을 쓰지 않는다
    @GetMapping("/ignored")
    public void conversionResultIgnored(@RequestParam String id, @RequestParam String seq) {
        Integer.parseInt(id);
        // ruleid: mois-1-01-sql-injection-spring
        jdbc.queryForList("SELECT * FROM pets WHERE id = " + id);
        Long.parseLong(seq);
        // ruleid: mois-1-01-sql-injection-spring
        jdbc.queryForList("SELECT * FROM pets WHERE seq = " + seq);
    }

    // 숫자 변환의 "인자 안"에서 실행되는 질의문: 변환 결과가 숫자라는 것은 안쪽 질의문이 안전하다는 증명이 아니다
    @GetMapping("/nested")
    public boolean sinkInsideConversion(@RequestParam String table) {
        // ruleid: mois-1-01-sql-injection-spring
        int count = Integer.parseInt(em.createNativeQuery("SELECT COUNT(*) FROM " + table).getSingleResult().toString());
        // ruleid: mois-1-01-sql-injection-spring
        long total = Long.parseLong(String.valueOf(jdbc.queryForMap("SELECT COUNT(*) cnt FROM " + table).get("cnt")));
        // ruleid: mois-1-01-sql-injection-spring
        return count > total || Long.parseLong(jdbc.queryForObject("SELECT MAX(id) FROM " + table, String.class)) > 0;
    }

    // 변환 식의 인자 안에서 대입한 변수는 문자열 그대로다 (숫자인 것은 변환 "결과"뿐)
    @GetMapping("/assigned")
    public void assignedInsideConversion(@RequestParam String raw) {
        String id;
        long n = Long.parseLong(id = raw.trim());
        // ruleid: mois-1-01-sql-injection-spring
        jdbc.queryForList("SELECT * FROM pets WHERE id = " + id);
    }

    // batchUpdate(String... sql): 첫 인자가 상수여도 두 번째부터의 인자 역시 질의문이다
    @GetMapping("/batch")
    public void batchVarargs(@RequestParam String table) {
        // ruleid: mois-1-01-sql-injection-spring
        jdbc.batchUpdate("SET FOREIGN_KEY_CHECKS = 0", "TRUNCATE TABLE " + table);
        // ruleid: mois-1-01-sql-injection-spring
        jdbcOps.batchUpdate("SET FOREIGN_KEY_CHECKS = 0", "TRUNCATE TABLE " + table, "SET FOREIGN_KEY_CHECKS = 1");
        // ruleid: mois-1-01-sql-injection-spring
        getJdbcTemplate().batchUpdate("SET FOREIGN_KEY_CHECKS = 0", "SET UNIQUE_CHECKS = 0", "TRUNCATE TABLE " + table);
        // ruleid: mois-1-01-sql-injection-spring
        named.getJdbcOperations().batchUpdate("SET FOREIGN_KEY_CHECKS = 0", "TRUNCATE TABLE " + table);
        // 타입을 알 수 없는 두 번째 인자(메서드 호출 결과)는 바인딩 값이라는 증명이 없다 — 질의문일 수 있다
        // ruleid: mois-1-01-sql-injection-spring
        jdbc.batchUpdate("SET FOREIGN_KEY_CHECKS = 0", truncateSql(table));
    }

    private String truncateSql(String table) {
        return "TRUNCATE TABLE " + table;
    }

    public static class LegacyDao {
        public Object jdbcTemplate;
    }
}

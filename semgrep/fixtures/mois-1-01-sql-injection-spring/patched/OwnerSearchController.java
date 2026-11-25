package demo;

import java.util.Collection;
import java.util.List;
import java.util.Map;
import javax.persistence.EntityManager;
import org.hibernate.Session;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.jdbc.core.namedparam.SqlParameterSource;
import org.springframework.jdbc.core.namedparam.SqlParameterSourceUtils;
import org.springframework.jdbc.core.support.JdbcDaoSupport;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

// 탐지되면 안 되는 경우: 바인딩 변수·이름 있는 파라미터 사용, 숫자형 파라미터, 숫자로 변환한 값
@RestController
public class OwnerSearchController extends JdbcDaoSupport {
    private final JdbcTemplate jdbcTemplate;
    private final NamedParameterJdbcTemplate named;
    private final EntityManager em;
    private final Session session;
    private NamedParameterJdbcTemplate namedParameterJdbcTemplate;

    public OwnerSearchController(JdbcTemplate jdbcTemplate, NamedParameterJdbcTemplate named, EntityManager em, Session session) {
        this.jdbcTemplate = jdbcTemplate;
        this.named = named;
        this.em = em;
        this.session = session;
    }

    @GetMapping("/owners")
    public List<Map<String, Object>> byLastName(@RequestParam("lastName") String lastName) {
        // ok: mois-1-01-sql-injection-spring — 질의문은 상수, 입력값은 바인딩 인자
        return jdbcTemplate.queryForList("SELECT * FROM owners WHERE last_name LIKE ?", lastName + "%");
    }

    @GetMapping("/owners/city")
    public List<Map<String, Object>> byCity(@RequestParam String city) {
        // ok: mois-1-01-sql-injection-spring — 이름으로 잡는 형태(getJdbcTemplate())도 질의문 인자만 본다
        return getJdbcTemplate().queryForList("SELECT * FROM owners WHERE city = ?", city);
    }

    @GetMapping("/owners/phone")
    public List<Map<String, Object>> byPhone(@RequestParam String phone) {
        // ok: mois-1-01-sql-injection-spring — 이름 있는 파라미터(:phone)로 바인딩
        return named.queryForList("SELECT * FROM owners WHERE telephone = :phone", new MapSqlParameterSource("phone", phone));
    }

    @GetMapping("/items/{name}")
    public List<?> items(@PathVariable String name) {
        // ok: mois-1-01-sql-injection-spring — 위치 파라미터(?1)로 바인딩
        return em.createNativeQuery("SELECT * FROM item WHERE name = ?1").setParameter(1, name).getResultList();
    }

    @GetMapping("/students")
    public List<?> students(@RequestParam String name) {
        // ok: mois-1-01-sql-injection-spring — 이름 있는 파라미터(:name)로 바인딩
        return session.createQuery("from Student where studentName = :name").setParameter("name", name).list();
    }

    // 숫자형 파라미터는 문자열을 끼워 넣을 수 없다
    @GetMapping("/pets/{id}")
    public List<Map<String, Object>> pet(@PathVariable int id) {
        // ok: mois-1-01-sql-injection-spring — int 파라미터
        return jdbcTemplate.queryForList("SELECT * FROM pets WHERE id = " + id);
    }

    // 문자열로 받았더라도 숫자로 변환한 값을 쓴다
    @GetMapping("/visits")
    public List<Map<String, Object>> visits(@RequestParam String petId, @RequestParam String vetId) {
        int pet = Integer.parseInt(petId);
        long vet = Long.parseLong(vetId);
        // ok: mois-1-01-sql-injection-spring — 숫자로 변환한 값
        return jdbcTemplate.queryForList("SELECT * FROM visits WHERE pet_id = " + pet + " AND vet_id = " + vet);
    }

    // 변환 식을 질의문에 바로 이어 붙여도 들어가는 것은 숫자(변환 결과)뿐이다
    @GetMapping("/visits/inline")
    public List<Map<String, Object>> visitsInline(@RequestParam String petId, @RequestParam String vetId) {
        // ok: mois-1-01-sql-injection-spring — 변환 결과만 질의문에 들어간다
        return jdbcTemplate.queryForList("SELECT * FROM visits WHERE pet_id = " + Integer.parseInt(petId) + " AND vet_id = " + Long.parseLong(vetId));
    }

    // 선언과 대입을 나눠 써도 같다
    @GetMapping("/visits/assigned")
    public List<Map<String, Object>> visitsAssigned(@RequestParam String petId, @RequestParam String vetId) {
        int pet;
        long vet;
        pet = Integer.parseInt(petId);
        vet = Long.parseLong(vetId);
        // ok: mois-1-01-sql-injection-spring — 숫자로 변환한 값
        return jdbcTemplate.queryForList("SELECT * FROM visits WHERE pet_id = " + pet + " AND vet_id = " + vet);
    }

    // batchUpdate(sql, 값 묶음, ...): 두 번째 인자가 바인딩 값 묶음으로 확인되면 질의문이 아니다
    @PostMapping("/owners/batch")
    public void batch(@RequestBody List<Object[]> rows) {
        // ok: mois-1-01-sql-injection-spring — List 로 선언된 값 묶음
        jdbcTemplate.batchUpdate("INSERT INTO owners(first_name, last_name) VALUES (?, ?)", rows);
        SqlParameterSource[] batch = SqlParameterSourceUtils.createBatch(rows);
        // ok: mois-1-01-sql-injection-spring — SqlParameterSource[] 로 선언된 값 묶음
        namedParameterJdbcTemplate.batchUpdate("INSERT INTO owners(first_name, last_name) VALUES (:first, :last)", batch);
        // ok: mois-1-01-sql-injection-spring — createBatch(...) 가 만든 값 묶음
        namedParameterJdbcTemplate.batchUpdate("INSERT INTO owners(first_name, last_name) VALUES (:first, :last)", SqlParameterSourceUtils.createBatch(rows));
    }

    @PostMapping("/tags/batch")
    public void tags(@RequestParam Collection<String> names) {
        // ok: mois-1-01-sql-injection-spring — Collection 으로 선언된 값 묶음 + setter
        jdbcTemplate.batchUpdate("INSERT INTO tags(name) VALUES (?)", names, 100, (ps, name) -> ps.setString(1, name));
    }

    @PostMapping("/owners/batch-named")
    public void batchNamed(@RequestBody Map<String, Object>[] rows) {
        // ok: mois-1-01-sql-injection-spring — Map[] 로 선언된 값 묶음
        namedParameterJdbcTemplate.batchUpdate("INSERT INTO owners(first_name, last_name) VALUES (:first, :last)", rows);
    }
}

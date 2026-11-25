package demo;

import javax.naming.NamingEnumeration;
import javax.naming.NamingException;
import javax.naming.directory.DirContext;
import javax.naming.directory.SearchControls;
import javax.naming.directory.SearchResult;
import javax.servlet.http.HttpServletRequest;
import org.owasp.esapi.ESAPI;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ldap.filter.EqualsFilter;
import org.springframework.ldap.filter.GreaterThanOrEqualsFilter;
import org.springframework.ldap.filter.LessThanOrEqualsFilter;
import org.springframework.ldap.support.LdapEncoder;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

// 탐지되면 안 되는 경우: 허용 문자 검증 후 사용(진단가이드 예), 필터 인자({0}) 사용, LDAP 필터 인코더 사용
@RestController
public class LdapSearch {
    private static final Logger log = LoggerFactory.getLogger(LdapSearch.class);
    private final DirContext dctx;

    public LdapSearch(DirContext dctx) {
        this.dctx = dctx;
    }

    // 진단가이드 안전한 코드 예: 허용 문자만 통과, 아니면 예외로 중단
    public NamingEnumeration<SearchResult> searchRecord(HttpServletRequest request) throws NamingException {
        String userSN = request.getParameter("sn");
        if (userSN == null || !userSN.matches("[\\w\\s]*")) {
            throw new IllegalArgumentException("Invalid input");
        }
        String filter = "(sn=" + userSN + ")";
        // ok: mois-1-10-ldap-injection — null 이거나 형식이 틀리면 위에서 끝난다
        return dctx.search("dc=example,dc=com", filter, new SearchControls());
    }

    @GetMapping("/mail")
    public NamingEnumeration<SearchResult> byMail(@RequestParam String mail) throws NamingException {
        if (!mail.matches("[\\w.@-]+")) {
            return null;
        }
        // ok: mois-1-10-ldap-injection — 검사에 실패하면 위에서 return 으로 끝난다
        return dctx.search("ou=People", "(mail=" + mail + ")", new SearchControls());
    }

    // 중괄호 없는 if (return / throw), `== false` 로 쓴 검사
    @GetMapping("/phone")
    public NamingEnumeration<SearchResult> byPhone(@RequestParam String phone) throws NamingException {
        if (!phone.matches("[0-9-]+")) return null;
        // ok: mois-1-10-ldap-injection
        return dctx.search("ou=People", "(telephoneNumber=" + phone + ")", new SearchControls());
    }

    @GetMapping("/dept")
    public NamingEnumeration<SearchResult> byDept(@RequestParam String dept) throws NamingException {
        if (dept.matches("[\\w-]+") == false) throw new IllegalArgumentException("Invalid input");
        // ok: mois-1-10-ldap-injection
        return dctx.search("ou=People", "(departmentNumber=" + dept + ")", new SearchControls());
    }

    // 실패 분기에서 기록을 남긴 뒤 중단한다 (마지막 문장이 return / throw)
    @GetMapping("/employee")
    public NamingEnumeration<SearchResult> byEmployeeNo(@RequestParam String no) throws NamingException {
        if (!no.matches("[0-9]+")) {
            log.warn("rejected employee number");
            return null;
        }
        // ok: mois-1-10-ldap-injection — 기록 후 return 으로 끝난다
        return dctx.search("ou=People", "(employeeNumber=" + no + ")", new SearchControls());
    }

    @GetMapping("/room")
    public NamingEnumeration<SearchResult> byRoom(@RequestParam String room) throws NamingException {
        if (!room.matches("[A-Z0-9-]+")) {
            log.warn("rejected room number");
            throw new IllegalArgumentException("Invalid input");
        }
        // ok: mois-1-10-ldap-injection — 기록 후 예외로 끝난다
        return dctx.search("ou=People", "(roomNumber=" + room + ")", new SearchControls());
    }

    // 검사를 통과한 분기 안에서만 검색한다
    @GetMapping("/uid")
    public NamingEnumeration<SearchResult> byUid(@RequestParam String uid) throws NamingException {
        if (uid.matches("[a-z0-9]+")) {
            // ok: mois-1-10-ldap-injection — 통과한 분기 안에서만 사용
            return dctx.search("ou=People", "(uid=" + uid + ")", new SearchControls());
        }
        return null;
    }

    // null 검사와 && 로 묶은 검사 (검사식을 감싸는 식이 && 뿐이다), 중괄호 없는 본문
    @GetMapping("/employee-type")
    public NamingEnumeration<SearchResult> byType(@RequestParam String type) throws NamingException {
        if (type != null && !type.isEmpty() && type.matches("[a-z]+")) {
            // ok: mois-1-10-ldap-injection — 세 조건이 모두 참일 때만 들어온다
            return dctx.search("ou=People", "(employeeType=" + type + ")", new SearchControls());
        }
        return null;
    }

    @GetMapping("/locality")
    public NamingEnumeration<SearchResult> byLocality(@RequestParam String l) throws NamingException {
        if (l != null && l.matches("[\\w ]+"))
            // ok: mois-1-10-ldap-injection
            return dctx.search("ou=People", "(l=" + l + ")", new SearchControls());
        return null;
    }

    // 필터는 상수, 값은 필터 인자로 넘긴다 (JNDI 가 이스케이프한다)
    @GetMapping("/managers")
    public NamingEnumeration<SearchResult> reports(@RequestParam String managerName) throws NamingException {
        // ok: mois-1-10-ldap-injection — 필터 문자열이 상수
        return dctx.search("ou=People", "(manager={0})", new Object[] {managerName}, new SearchControls());
    }

    // LDAP 필터용 인코더
    @GetMapping("/cn")
    public NamingEnumeration<SearchResult> byCn(@RequestParam String cn) throws NamingException {
        String filter = "(cn=" + LdapEncoder.filterEncode(cn) + ")";
        // ok: mois-1-10-ldap-injection — Spring LdapEncoder.filterEncode
        return dctx.search("ou=People", filter, new SearchControls());
    }

    @GetMapping("/ou")
    public NamingEnumeration<SearchResult> byOu(@RequestParam String ou) throws NamingException {
        String filter = "(ou=" + ESAPI.encoder().encodeForLDAP(ou) + ")";
        // ok: mois-1-10-ldap-injection — ESAPI encodeForLDAP
        return dctx.search("ou=People", filter, new SearchControls());
    }

    // Spring LDAP 필터 객체는 값을 이스케이프해서 필터 문자열을 만든다
    @GetMapping("/title")
    public NamingEnumeration<SearchResult> byTitle(@RequestParam String title) throws NamingException {
        String filter = new EqualsFilter("title", title).encode();
        // ok: mois-1-10-ldap-injection — EqualsFilter 가 값을 이스케이프
        return dctx.search("ou=People", filter, new SearchControls());
    }

    // ESAPI 인코더에 와일드카드(*)도 이스케이프하라고 명시한 경우
    @GetMapping("/ou-exact")
    public NamingEnumeration<SearchResult> byOuExact(@RequestParam String ou) throws NamingException {
        String filter = "(ou=" + ESAPI.encoder().encodeForLDAP(ou, true) + ")";
        // ok: mois-1-10-ldap-injection — ESAPI encodeForLDAP(값, true)
        return dctx.search("ou=People", filter, new SearchControls());
    }

    // 범위 필터 객체 (GreaterThanOrEquals·LessThanOrEquals)
    @GetMapping("/joined")
    public NamingEnumeration<SearchResult> byJoinedBetween(@RequestParam String from, @RequestParam String to) throws NamingException {
        String since = new GreaterThanOrEqualsFilter("createTimestamp", from).encode();
        String until = new LessThanOrEqualsFilter("createTimestamp", to).encode();
        // ok: mois-1-10-ldap-injection — 범위 필터 객체가 값을 이스케이프
        return dctx.search("ou=People", "(&" + since + until + ")", new SearchControls());
    }
}

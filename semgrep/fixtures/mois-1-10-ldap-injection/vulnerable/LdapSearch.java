package demo;

import javax.naming.NamingEnumeration;
import javax.naming.NamingException;
import javax.naming.directory.DirContext;
import javax.naming.directory.SearchControls;
import javax.naming.directory.SearchResult;
import javax.servlet.http.HttpServletRequest;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

// 탐지돼야 하는 경우 2건: 외부 입력을 LDAP 검색 필터에 이어 붙임
@RestController
public class LdapSearch {
    private final DirContext dctx;

    public LdapSearch(DirContext dctx) {
        this.dctx = dctx;
    }

    // 진단가이드 예: 검색 필터를 문자열로 조립
    public NamingEnumeration<SearchResult> searchRecord(HttpServletRequest request) throws NamingException {
        String userSN = request.getParameter("sn");
        String mail = request.getParameter("mail");
        String filter = "(&(sn=" + userSN + ")(mail=" + mail + "))";
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("dc=example,dc=com", filter, new SearchControls());
    }

    @GetMapping("/managers")
    public NamingEnumeration<SearchResult> reports(@RequestParam String managerName) throws NamingException {
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("ou=People", "(manager=" + managerName + ")", new SearchControls());
    }
}

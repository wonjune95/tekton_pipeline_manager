package demo;

import javax.naming.NamingEnumeration;
import javax.naming.NamingException;
import javax.naming.directory.DirContext;
import javax.naming.directory.SearchControls;
import javax.naming.directory.SearchResult;
import javax.servlet.http.HttpServletRequest;
import org.springframework.ldap.filter.HardcodedFilter;
import org.springframework.ldap.support.LdapEncoder;

// 검증·인코딩이 "있기만" 하고 막지는 못하는 경우: 모두 탐지되어야 한다
public class LdapCheckBypass {
    private DirContext dctx;

    // 검사 결과를 쓰지 않는다
    public NamingEnumeration<SearchResult> resultIgnored(HttpServletRequest request) throws NamingException {
        String sn = request.getParameter("sn");
        sn.matches("[\\w\\s]*");
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
    }

    // 실패해도 기록만 하고 계속 진행한다
    public NamingEnumeration<SearchResult> failureDoesNotExit(HttpServletRequest request) throws NamingException {
        String sn = request.getParameter("sn");
        if (sn == null || !sn.matches("[\\w\\s]*")) {
            System.err.println("invalid sn");
        }
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
    }

    // 검사를 통과하지 못한 쪽(else)에서 검색한다
    public NamingEnumeration<SearchResult> oppositeBranch(HttpServletRequest request) throws NamingException {
        String sn = request.getParameter("sn");
        if (sn.matches("[\\w\\s]*")) {
            return null;
        } else {
            // ruleid: mois-1-10-ldap-injection
            return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
        }
    }

    // 부정 조건 안에서 검색한다
    public NamingEnumeration<SearchResult> negatedCondition(HttpServletRequest request) throws NamingException {
        String sn = request.getParameter("sn");
        if (sn == null || !sn.matches("[\\w\\s]*")) {
            // ruleid: mois-1-10-ldap-injection
            return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
        }
        return null;
    }

    // 문자를 지우기는 하지만 무엇을 지우는지 알 수 없다 (임의의 replaceAll 은 인정하지 않는다)
    public NamingEnumeration<SearchResult> arbitraryReplace(HttpServletRequest request) throws NamingException {
        String sn = request.getParameter("sn").replaceAll("\\s", "");
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
    }

    // 인코딩한 결과를 버리고 원래 값을 쓴다
    public NamingEnumeration<SearchResult> encodedResultIgnored(HttpServletRequest request) throws NamingException {
        String sn = request.getParameter("sn");
        LdapEncoder.filterEncode(sn);
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
    }

    // DN 용 인코더는 필터 문자를 막지 못한다
    public NamingEnumeration<SearchResult> wrongEncoder(HttpServletRequest request) throws NamingException {
        String sn = LdapEncoder.nameEncode(request.getParameter("sn"));
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
    }

    // HardcodedFilter 는 문자열을 그대로 필터로 쓴다 (인코딩하지 않는다)
    public NamingEnumeration<SearchResult> hardcodedFilter(HttpServletRequest request) throws NamingException {
        String filter = new HardcodedFilter("(sn=" + request.getParameter("sn") + ")").encode();
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("dc=example,dc=com", filter, new SearchControls());
    }

    // 실패 분기 안의 또 다른 조건에서만 중단한다
    public NamingEnumeration<SearchResult> exitsOnlySometimes(HttpServletRequest request, boolean strict) throws NamingException {
        String sn = request.getParameter("sn");
        if (!sn.matches("[\\w\\s]*")) {
            if (strict) {
                return null;
            }
        }
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
    }

    // 통과한 분기 밖에서 검색한다
    public NamingEnumeration<SearchResult> usedAfterPositiveIf(HttpServletRequest request) throws NamingException {
        String sn = request.getParameter("sn");
        if (sn != null && sn.matches("[\\w\\s]*")) {
            System.out.println("valid sn");
        }
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
    }

    // `== false` 로 쓴 실패 분기 안에서 검색한다
    public NamingEnumeration<SearchResult> usedInFalseBranch(HttpServletRequest request) throws NamingException {
        String sn = request.getParameter("sn");
        if (sn.matches("[\\w\\s]*") == false) {
            // ruleid: mois-1-10-ldap-injection
            return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
        }
        return null;
    }

    // 검사한 뒤 다른 입력으로 바꿔 검색한다
    public NamingEnumeration<SearchResult> reassignedAfterCheck(HttpServletRequest request) throws NamingException {
        String sn = request.getParameter("sn");
        if (sn == null || !sn.matches("[\\w\\s]*")) {
            throw new IllegalArgumentException("Invalid input");
        }
        sn = request.getParameter("alias");
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
    }

    // 검사한 뒤 검사하지 않은 입력을 덧붙여 검색한다
    public NamingEnumeration<SearchResult> appendedAfterCheck(HttpServletRequest request) throws NamingException {
        String sn = request.getParameter("sn");
        if (sn == null || !sn.matches("[\\w\\s]*")) {
            throw new IllegalArgumentException("Invalid input");
        }
        sn += request.getParameter("suffix");
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
    }

    // 다른 조건이 거짓이면 검사 자체를 건너뛴다
    public NamingEnumeration<SearchResult> checkSkippedByAnd(HttpServletRequest request, boolean strict) throws NamingException {
        String sn = request.getParameter("sn");
        if (strict && !sn.matches("[\\w\\s]*")) {
            throw new IllegalArgumentException("Invalid input");
        }
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
    }
}

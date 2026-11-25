package demo;

import javax.naming.NamingEnumeration;
import javax.naming.NamingException;
import javax.naming.directory.DirContext;
import javax.naming.directory.SearchControls;
import javax.naming.directory.SearchResult;
import javax.servlet.http.HttpServletRequest;

// 검사식이 다른 식에 묶여 있어 "검사 실패 = 중단", "본문 진입 = 검사 통과" 가 성립하지 않는 경우: 모두 탐지되어야 한다
public class GuardOperatorBypass {
    private DirContext dctx;

    // & 는 && 와 같은 뜻이다: strict 가 false 면 검사에 실패해도 계속 진행한다
    public NamingEnumeration<SearchResult> bitwiseAnd(HttpServletRequest request, boolean strict) throws NamingException {
        String sn = request.getParameter("sn");
        if (!sn.matches("[\\w\\s]*") & strict) {
            return null;
        }
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
    }

    public NamingEnumeration<SearchResult> bitwiseAndEqFalse(HttpServletRequest request, boolean strict) throws NamingException {
        String sn = request.getParameter("sn");
        if (sn.matches("[\\w\\s]*") == false & strict) return null;
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
    }

    // 조건 연산자: strict 가 false 면 검사하지 않는다
    public NamingEnumeration<SearchResult> ternary(HttpServletRequest request, boolean strict) throws NamingException {
        String sn = request.getParameter("sn");
        if (strict ? !sn.matches("[\\w\\s]*") : false) {
            return null;
        }
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
    }

    // ^ : legacy 가 true 면 검사에 "통과한" 값에서 중단하고 실패한 값은 계속 진행한다
    public NamingEnumeration<SearchResult> xor(HttpServletRequest request, boolean legacy) throws NamingException {
        String sn = request.getParameter("sn");
        if (!sn.matches("[\\w\\s]*") ^ legacy) {
            return null;
        }
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
    }

    // 전체를 다시 부정: 검사에 통과하면 중단하고, 실패하면 계속 진행한다
    public NamingEnumeration<SearchResult> negatedWhole(HttpServletRequest request) throws NamingException {
        String sn = request.getParameter("sn");
        if (!(sn == null || !sn.matches("[\\w\\s]*"))) {
            return null;
        }
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
    }

    public NamingEnumeration<SearchResult> comparedWithFalse(HttpServletRequest request) throws NamingException {
        String sn = request.getParameter("sn");
        if (!sn.matches("[\\w\\s]*") == false) {
            return null;
        }
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
    }

    // 검사 결과를 다른 호출의 인자로 넘긴다: 조건의 참·거짓은 그 호출이 정한다
    public NamingEnumeration<SearchResult> passedToCall(HttpServletRequest request) throws NamingException {
        String sn = request.getParameter("sn");
        if (Boolean.FALSE.equals(!sn.matches("[\\w\\s]*"))) {
            return null;
        }
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
    }

    // 조건 안에서만 사용하는 형태: || · | 는 검사가 거짓이어도 본문에 들어온다
    public NamingEnumeration<SearchResult> positiveOr(HttpServletRequest request, boolean admin) throws NamingException {
        String sn = request.getParameter("sn");
        if (sn.matches("[\\w\\s]*") || admin) {
            // ruleid: mois-1-10-ldap-injection
            return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
        }
        return null;
    }

    public NamingEnumeration<SearchResult> positiveBitwiseOr(HttpServletRequest request, boolean admin) throws NamingException {
        String sn = request.getParameter("sn");
        if (sn.matches("[\\w\\s]*") | admin) {
            // ruleid: mois-1-10-ldap-injection
            return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
        }
        return null;
    }

    public NamingEnumeration<SearchResult> positiveTernary(HttpServletRequest request, boolean admin) throws NamingException {
        String sn = request.getParameter("sn");
        if (admin ? true : sn.matches("[\\w\\s]*")) {
            // ruleid: mois-1-10-ldap-injection
            return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
        }
        return null;
    }

    // 본문이 검사에 "실패한" 쪽이다
    public NamingEnumeration<SearchResult> positiveNotTrue(HttpServletRequest request) throws NamingException {
        String sn = request.getParameter("sn");
        if (sn.matches("[\\w\\s]*") != true) {
            // ruleid: mois-1-10-ldap-injection
            return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
        }
        return null;
    }

    public NamingEnumeration<SearchResult> positiveNegatedWhole(HttpServletRequest request) throws NamingException {
        String sn = request.getParameter("sn");
        if (!(sn != null && sn.matches("[\\w\\s]*"))) {
            // ruleid: mois-1-10-ldap-injection
            return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
        }
        return null;
    }

    public NamingEnumeration<SearchResult> positivePassedToCall(HttpServletRequest request) throws NamingException {
        String sn = request.getParameter("sn");
        if (Boolean.FALSE.equals(sn.matches("[\\w\\s]*"))) {
            // ruleid: mois-1-10-ldap-injection
            return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
        }
        return null;
    }

    // 조건식 안에서 먼저 검색하고 그 뒤에 검사한다
    public boolean usedInConditionBeforeCheck(HttpServletRequest request) throws NamingException {
        String sn = request.getParameter("sn");
        // ruleid: mois-1-10-ldap-injection
        if (dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls()).hasMore() && sn.matches("[\\w\\s]*")) {
            return true;
        }
        return false;
    }

    // 검사에 통과한 뒤 본문에서 다른 입력으로 바꾸거나 덧붙인다
    public NamingEnumeration<SearchResult> reassignedInBody(HttpServletRequest request) throws NamingException {
        String sn = request.getParameter("sn");
        if (sn.matches("[\\w\\s]*")) {
            sn = request.getParameter("alias");
            // ruleid: mois-1-10-ldap-injection
            return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
        }
        return null;
    }

    public NamingEnumeration<SearchResult> appendedInBody(HttpServletRequest request) throws NamingException {
        String sn = request.getParameter("sn");
        if (sn.matches("[\\w\\s]*")) {
            sn += request.getParameter("suffix");
            // ruleid: mois-1-10-ldap-injection
            return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
        }
        return null;
    }

    public NamingEnumeration<SearchResult> reassignedInNestedBlock(HttpServletRequest request, boolean useAlias) throws NamingException {
        String sn = request.getParameter("sn");
        if (sn.matches("[\\w\\s]*")) {
            if (useAlias) {
                sn = request.getParameter("alias");
            }
            // ruleid: mois-1-10-ldap-injection
            return dctx.search("dc=example,dc=com", "(sn=" + sn + ")", new SearchControls());
        }
        return null;
    }
}

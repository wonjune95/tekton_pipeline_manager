package demo;

import javax.naming.NamingEnumeration;
import javax.naming.NamingException;
import javax.naming.directory.DirContext;
import javax.naming.directory.SearchControls;
import javax.naming.directory.SearchResult;
import javax.servlet.http.HttpServletRequest;
import org.owasp.esapi.ESAPI;
import org.springframework.ldap.filter.EqualsFilter;
import org.springframework.ldap.filter.GreaterThanOrEqualsFilter;
import org.springframework.ldap.filter.LikeFilter;
import org.springframework.ldap.filter.WhitespaceWildcardsFilter;

// 탐지돼야 하는 경우: 인코더·필터 객체를 썼지만 그것이 이스케이프하지 않는 자리에 입력이 들어간다
public class EncoderLimits {
    private DirContext dctx;

    // 필터 객체는 값만 이스케이프한다. 속성 이름이 입력이면 필터 구조가 바뀐다
    public NamingEnumeration<SearchResult> attributeNameFromInput(HttpServletRequest request) throws NamingException {
        String field = request.getParameter("field");
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("ou=People", new EqualsFilter(field, "fixed").encode(), new SearchControls());
    }

    public NamingEnumeration<SearchResult> rangeAttributeFromInput(HttpServletRequest request) throws NamingException {
        String field = request.getParameter("field");
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("ou=People", new GreaterThanOrEqualsFilter(field, "2020").encode(), new SearchControls());
    }

    // LikeFilter 는 값의 * 를 그대로 둔다: uid=* 로 모든 사용자에 맞는다
    public NamingEnumeration<SearchResult> likeFilterWildcard(HttpServletRequest request) throws NamingException {
        String user = request.getParameter("user");
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("ou=People", new LikeFilter("uid", user).encode(), new SearchControls());
    }

    // WhitespaceWildcardsFilter 는 공백을 * 로 바꾼다: 빈 값·공백만 넣으면 모든 항목에 맞는다
    public NamingEnumeration<SearchResult> whitespaceWildcards(HttpServletRequest request) throws NamingException {
        String words = request.getParameter("words");
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("ou=People", new WhitespaceWildcardsFilter("cn", words).encode(), new SearchControls());
    }

    // encodeForLDAP(값, false) 는 * 를 이스케이프하지 않는다
    public NamingEnumeration<SearchResult> esapiWithoutWildcardEncoding(HttpServletRequest request) throws NamingException {
        String user = request.getParameter("user");
        String filter = "(uid=" + ESAPI.encoder().encodeForLDAP(user, false) + ")";
        // ruleid: mois-1-10-ldap-injection
        return dctx.search("ou=People", filter, new SearchControls());
    }
}

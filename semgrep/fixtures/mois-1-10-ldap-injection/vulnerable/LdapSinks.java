package demo;

import javax.naming.NamingException;
import javax.naming.directory.InitialDirContext;
import javax.naming.directory.SearchControls;
import javax.naming.ldap.InitialLdapContext;
import javax.naming.ldap.LdapContext;
import javax.servlet.http.HttpServletRequest;
import org.springframework.ldap.core.AttributesMapper;
import org.springframework.ldap.core.ContextMapper;
import org.springframework.ldap.core.LdapOperations;
import org.springframework.ldap.core.LdapTemplate;

// sink 가지마다 한 줄씩: JNDI 컨텍스트 종류별, Spring LDAP 메서드별
public class LdapSinks {
    private InitialDirContext initialDirContext;
    private LdapContext ldapContext;
    private InitialLdapContext initialLdapContext;
    private LdapTemplate ldapTemplate;
    private LdapOperations ldapOperations;
    private AttributesMapper<String> attributesMapper;
    private ContextMapper<String> contextMapper;

    public void jndi(HttpServletRequest request) throws NamingException {
        String filter = "(uid=" + request.getParameter("uid") + ")";
        SearchControls controls = new SearchControls();
        // ruleid: mois-1-10-ldap-injection
        initialDirContext.search("ou=People", filter, controls);
        // ruleid: mois-1-10-ldap-injection
        ldapContext.search("ou=People", filter, controls);
        // ruleid: mois-1-10-ldap-injection
        initialLdapContext.search("ou=People", filter, controls);
    }

    public void springLdap(HttpServletRequest request) {
        String filter = "(uid=" + request.getParameter("uid") + ")";
        // ruleid: mois-1-10-ldap-injection
        ldapTemplate.search("ou=People", filter, attributesMapper);
        // ruleid: mois-1-10-ldap-injection
        ldapTemplate.searchForObject("ou=People", filter, contextMapper);
        // ruleid: mois-1-10-ldap-injection
        ldapTemplate.authenticate("ou=People", filter, request.getParameter("password"));
        // ruleid: mois-1-10-ldap-injection
        ldapOperations.search("ou=People", filter, attributesMapper);
    }
}

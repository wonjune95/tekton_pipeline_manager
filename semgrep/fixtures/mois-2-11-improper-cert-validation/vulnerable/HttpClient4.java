package demo;

import javax.net.ssl.HostnameVerifier;
import org.apache.http.conn.ssl.AllowAllHostnameVerifier;
import org.apache.http.conn.ssl.NoopHostnameVerifier;
import org.apache.http.conn.ssl.SSLConnectionSocketFactory;
import org.apache.http.conn.ssl.TrustAllStrategy;
import org.apache.http.conn.ssl.TrustSelfSignedStrategy;
import org.apache.http.ssl.TrustStrategy;

// 탐지돼야 하는 경우: Apache HttpClient 4 의 "모두 허용" 구현체
public class HttpClient4 {
    public HostnameVerifier noop() {
        // ruleid: mois-2-11-improper-cert-validation
        return new NoopHostnameVerifier();
    }

    public Object allowAllConstant() {
        // ruleid: mois-2-11-improper-cert-validation
        return SSLConnectionSocketFactory.ALLOW_ALL_HOSTNAME_VERIFIER;
    }

    public Object allowAll() {
        // ruleid: mois-2-11-improper-cert-validation
        return new AllowAllHostnameVerifier();
    }

    public TrustStrategy trustAllInstance() {
        // ruleid: mois-2-11-improper-cert-validation
        return TrustAllStrategy.INSTANCE;
    }

    public TrustStrategy trustAll() {
        // ruleid: mois-2-11-improper-cert-validation
        return new TrustAllStrategy();
    }

    public TrustStrategy selfSignedInstance() {
        // ruleid: mois-2-11-improper-cert-validation
        return TrustSelfSignedStrategy.INSTANCE;
    }
}

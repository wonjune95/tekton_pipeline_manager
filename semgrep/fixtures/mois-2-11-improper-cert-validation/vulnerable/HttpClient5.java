package demo;

import javax.net.ssl.HostnameVerifier;
import org.apache.hc.client5.http.ssl.NoopHostnameVerifier;
import org.apache.hc.client5.http.ssl.TrustAllStrategy;
import org.apache.hc.client5.http.ssl.TrustSelfSignedStrategy;
import org.apache.hc.core5.ssl.TrustStrategy;

// 탐지돼야 하는 경우: Apache HttpClient 5 의 "모두 허용" 구현체
public class HttpClient5 {
    public HostnameVerifier noopInstance() {
        // ruleid: mois-2-11-improper-cert-validation
        return NoopHostnameVerifier.INSTANCE;
    }

    public HostnameVerifier noop() {
        // ruleid: mois-2-11-improper-cert-validation
        return new NoopHostnameVerifier();
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

    public TrustStrategy selfSigned() {
        // ruleid: mois-2-11-improper-cert-validation
        return new TrustSelfSignedStrategy();
    }
}

package demo;

import java.security.GeneralSecurityException;
import java.security.KeyStore;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;
import javax.net.ssl.HostnameVerifier;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManagerFactory;
import javax.net.ssl.X509TrustManager;

// 탐지되면 안 되는 경우: 신뢰 저장소로 인증서를 검증하고, 호스트 이름은 기본 검증기에 맡긴다
public class HttpsClient {
    public SSLContext withTrustStore(KeyStore trustStore) throws GeneralSecurityException {
        TrustManagerFactory tmf = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
        tmf.init(trustStore);
        SSLContext ctx = SSLContext.getInstance("TLSv1.3");
        // ok: mois-2-11-improper-cert-validation — 신뢰 저장소로 만든 기본 TrustManager 사용
        ctx.init(null, tmf.getTrustManagers(), null);
        return ctx;
    }

    public HostnameVerifier expectedHost(String expected) {
        HostnameVerifier defaultVerifier = HttpsURLConnection.getDefaultHostnameVerifier();
        // ok: mois-2-11-improper-cert-validation — 항상 true 가 아니라 기본 검증기의 결과를 쓴다
        return (hostname, session) -> expected.equalsIgnoreCase(hostname) && defaultVerifier.verify(hostname, session);
    }

    public void strictHost(HttpsURLConnection conn, HostnameVerifier pinned) {
        // ok: mois-2-11-improper-cert-validation — 항상 true 인 람다가 아닌 검증기를 설정
        conn.setHostnameVerifier(pinned);
    }

    public SSLContext privateCa(KeyStore trustStore) throws GeneralSecurityException {
        // ok: mois-2-11-improper-cert-validation — 사설 인증서를 신뢰 저장소로 등록 (전략 없이)
        return new org.apache.http.ssl.SSLContextBuilder().loadTrustMaterial(trustStore, null).build();
    }

    public HostnameVerifier defaultVerifier() {
        // ok: mois-2-11-improper-cert-validation — 호스트 이름을 실제로 검증하는 구현체
        return new org.apache.http.conn.ssl.DefaultHostnameVerifier();
    }

    // 검증은 기본 TrustManager 에 맡기는 위임형 TrustManager
    public static final class DelegatingTrustManager implements X509TrustManager {
        private final X509TrustManager delegate;

        public DelegatingTrustManager(X509TrustManager delegate) {
            this.delegate = delegate;
        }

        public X509Certificate[] getAcceptedIssuers() {
            return delegate.getAcceptedIssuers();
        }

        public void checkClientTrusted(X509Certificate[] chain, String authType) throws CertificateException {
            delegate.checkClientTrusted(chain, authType);
        }

        // ok: mois-2-11-improper-cert-validation — 본문이 비어 있지 않고 기본 TrustManager 에 검증을 맡긴다
        public void checkServerTrusted(X509Certificate[] chain, String authType) throws CertificateException {
            delegate.checkServerTrusted(chain, authType);
        }
    }
}

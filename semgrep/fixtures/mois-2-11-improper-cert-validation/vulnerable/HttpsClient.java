package demo;

import java.security.GeneralSecurityException;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;
import javax.net.ssl.HostnameVerifier;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSession;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;
import org.apache.http.conn.ssl.NoopHostnameVerifier;
import org.apache.http.conn.ssl.TrustSelfSignedStrategy;
import org.apache.http.ssl.SSLContextBuilder;

// 탐지돼야 하는 경우: 인증서·호스트 이름을 검증하지 않는다
public class HttpsClient {
    public SSLContext trustAll() throws GeneralSecurityException {
        TrustManager[] trustAll = new TrustManager[] {
            new X509TrustManager() {
                public X509Certificate[] getAcceptedIssuers() {
                    return new X509Certificate[0];
                }

                public void checkClientTrusted(X509Certificate[] chain, String authType) {
                }

                // ruleid: mois-2-11-improper-cert-validation
                public void checkServerTrusted(X509Certificate[] chain, String authType) {
                }
            }
        };
        SSLContext ctx = SSLContext.getInstance("TLS");
        ctx.init(null, trustAll, null);
        return ctx;
    }

    // throws 절이 있는 선언
    public static final class TrustEverything implements X509TrustManager {
        public X509Certificate[] getAcceptedIssuers() {
            return new X509Certificate[0];
        }

        public void checkClientTrusted(X509Certificate[] chain, String authType) throws CertificateException {
        }

        // ruleid: mois-2-11-improper-cert-validation
        @Override
        public void checkServerTrusted(X509Certificate[] chain, String authType) throws CertificateException {
        }
    }

    public void allowAllHosts() {
        // ruleid: mois-2-11-improper-cert-validation
        HttpsURLConnection.setDefaultHostnameVerifier((hostname, session) -> true);
    }

    // 연결 하나에만 설정, 타입을 적은 람다
    public void allowAllHostsOn(HttpsURLConnection conn) {
        // ruleid: mois-2-11-improper-cert-validation
        conn.setHostnameVerifier((String hostname, SSLSession session) -> true);
    }

    // 빌더 형태 (OkHttp 등): hostnameVerifier(...)
    public Object builder(ClientBuilder builder) {
        // ruleid: mois-2-11-improper-cert-validation
        return builder.hostnameVerifier((hostname, session) -> true).build();
    }

    public HostnameVerifier anyHost() {
        return new HostnameVerifier() {
            // ruleid: mois-2-11-improper-cert-validation
            @Override
            public boolean verify(String hostname, SSLSession session) {
                return true;
            }
        };
    }

    public HostnameVerifier noop() {
        // ruleid: mois-2-11-improper-cert-validation
        return NoopHostnameVerifier.INSTANCE;
    }

    public SSLContext selfSigned() throws GeneralSecurityException {
        // ruleid: mois-2-11-improper-cert-validation
        return new SSLContextBuilder().loadTrustMaterial(null, new TrustSelfSignedStrategy()).build();
    }

    // 무엇이든 신뢰하는 TrustStrategy 람다 (인자 2개·1개 형태)
    public SSLContext trustLambda() throws GeneralSecurityException {
        // ruleid: mois-2-11-improper-cert-validation
        return new SSLContextBuilder().loadTrustMaterial(null, (chain, authType) -> true).build();
    }

    public SSLContext trustLambdaOnly() throws GeneralSecurityException {
        // ruleid: mois-2-11-improper-cert-validation
        return new SSLContextBuilder().loadTrustMaterial((X509Certificate[] chain, String authType) -> true).build();
    }

    public interface ClientBuilder {
        ClientBuilder hostnameVerifier(HostnameVerifier verifier);

        Object build();
    }
}

package demo;

import java.security.MessageDigest;
import java.util.Properties;

// 탐지되면 안 되는 경우
public class Digest {
    // ok: mois-2-04-weak-hash — SHA-2 계열
    MessageDigest sha256() throws Exception { return MessageDigest.getInstance("SHA-256"); }
    // ok: mois-2-04-weak-hash — "SHA" 로 시작하지만 SHA-1 이 아니다
    MessageDigest sha3() throws Exception { return MessageDigest.getInstance("SHA3-512", "SUN"); }

    MessageDigest fromProps(Properties props) throws Exception {
        // ok: mois-2-04-weak-hash — 설정이 없을 때의 기본값이 안전한 알고리즘
        String alg = props.getProperty("hash.alg", "SHA-256");
        return MessageDigest.getInstance(alg);
    }

    MessageDigest fromPropsAssign() throws Exception {
        String alg;
        // ok: mois-2-04-weak-hash — 대입 형태, 기본값이 안전
        alg = System.getProperty("hash.alg", "SHA-512");
        return MessageDigest.getInstance(alg);
    }
}

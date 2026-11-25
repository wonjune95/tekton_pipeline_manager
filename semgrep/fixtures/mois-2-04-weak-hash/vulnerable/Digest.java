package demo;

import java.security.MessageDigest;
import java.util.Properties;

// 탐지돼야 하는 경우: 충돌이 알려진 해시
public class Digest {
    // ruleid: mois-2-04-weak-hash
    MessageDigest md5() throws Exception { return MessageDigest.getInstance("MD5"); }
    // ruleid: mois-2-04-weak-hash
    MessageDigest sha1() throws Exception { return MessageDigest.getInstance("SHA-1"); }

    // 다른 표기, 제공자 지정, 전체 이름
    // ruleid: mois-2-04-weak-hash
    MessageDigest sha1NoDash() throws Exception { return MessageDigest.getInstance("SHA1"); }
    // ruleid: mois-2-04-weak-hash
    MessageDigest sha() throws Exception { return MessageDigest.getInstance("SHA"); }
    // ruleid: mois-2-04-weak-hash
    MessageDigest md2() throws Exception { return MessageDigest.getInstance("md2"); }
    // ruleid: mois-2-04-weak-hash
    MessageDigest md4() throws Exception { return java.security.MessageDigest.getInstance("MD4", "BC"); }

    // 상수로 둔 알고리즘 이름
    private static final String ALG = "MD5";
    // ruleid: mois-2-04-weak-hash
    MessageDigest constant() throws Exception { return MessageDigest.getInstance(ALG); }

    // 설정에서 읽지만 기본값이 취약 (선언 형태)
    MessageDigest fromPropsDecl(Properties props) throws Exception {
        String alg = props.getProperty("hash.alg", "MD5");
        // ruleid: mois-2-04-weak-hash
        return MessageDigest.getInstance(alg);
    }

    // 설정에서 읽지만 기본값이 취약 (대입 형태)
    MessageDigest fromPropsAssign() throws Exception {
        String alg;
        alg = System.getProperty("hash.alg", "SHA-1");
        // ruleid: mois-2-04-weak-hash
        return MessageDigest.getInstance(alg, "SUN");
    }
}

package demo;

import java.util.Properties;
import javax.crypto.Cipher;

// 탐지돼야 하는 경우: 취약한 알고리즘·모드
public class Crypto {
    // ruleid: mois-2-04-weak-cipher
    Cipher des() throws Exception { return Cipher.getInstance("DES/CBC/PKCS5Padding"); }
    // ruleid: mois-2-04-weak-cipher
    Cipher rc4() throws Exception { return Cipher.getInstance("RC4"); }
    // ruleid: mois-2-04-weak-cipher
    Cipher ecb() throws Exception { return Cipher.getInstance("AES/ECB/PKCS5Padding"); }
    // ruleid: mois-2-04-weak-cipher
    Cipher aesDefault() throws Exception { return Cipher.getInstance("AES"); }   // 기본 모드가 ECB

    // 3DES, Blowfish, 소문자 표기, 제공자 지정
    // ruleid: mois-2-04-weak-cipher
    Cipher tripleDes() throws Exception { return Cipher.getInstance("DESede/CBC/PKCS5Padding"); }
    // ruleid: mois-2-04-weak-cipher
    Cipher blowfish() throws Exception { return Cipher.getInstance("Blowfish"); }
    // ruleid: mois-2-04-weak-cipher
    Cipher lower() throws Exception { return Cipher.getInstance("des"); }
    // ruleid: mois-2-04-weak-cipher
    Cipher withProvider() throws Exception { return javax.crypto.Cipher.getInstance("RC2", "BC"); }

    // 같은 알고리즘의 다른 이름: TripleDES(SunJCE 별칭), 3DES(IBM JCE 별칭), ARCFOUR(RC4 의 표준 이름)
    // ruleid: mois-2-04-weak-cipher
    Cipher tripleDesAlias() throws Exception { return Cipher.getInstance("TripleDES/CBC/PKCS5Padding"); }
    // ruleid: mois-2-04-weak-cipher
    Cipher tripleDesIbm() throws Exception { return Cipher.getInstance("3DES", "IBMJCE"); }
    // ruleid: mois-2-04-weak-cipher
    Cipher arcfour() throws Exception { return Cipher.getInstance("ARCFOUR"); }

    // 상수로 둔 알고리즘 이름
    private static final String ALG = "DES";
    // ruleid: mois-2-04-weak-cipher
    Cipher constant() throws Exception { return Cipher.getInstance(ALG); }

    // 설정에서 읽지만 기본값이 취약 (선언 형태)
    Cipher fromPropsDecl(Properties props) throws Exception {
        String alg = props.getProperty("cipher.alg", "DES/ECB/PKCS5Padding");
        // ruleid: mois-2-04-weak-cipher
        return Cipher.getInstance(alg);
    }

    // 설정에서 읽지만 기본값이 취약 (대입 형태)
    Cipher fromPropsAssign() throws Exception {
        String alg;
        alg = System.getProperty("cipher.alg", "AES");
        // ruleid: mois-2-04-weak-cipher
        return Cipher.getInstance(alg, "SunJCE");
    }
}

package demo;

import java.util.Properties;
import javax.crypto.Cipher;

// 탐지되면 안 되는 경우
public class Crypto {
    // ok: mois-2-04-weak-cipher — 인증 암호화 모드
    Cipher gcm() throws Exception { return Cipher.getInstance("AES/GCM/NoPadding"); }
    // ok: mois-2-04-weak-cipher — RSA/ECB/... 는 이름만 ECB 이고 블록 모드가 아니다
    Cipher oaep() throws Exception { return Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding"); }
    // ok: mois-2-04-weak-cipher — CBC 모드
    Cipher cbc() throws Exception { return Cipher.getInstance("AES/CBC/PKCS5Padding", "SunJCE"); }

    Cipher fromProps(Properties props) throws Exception {
        // ok: mois-2-04-weak-cipher — 설정이 없을 때의 기본값이 안전한 알고리즘
        String alg = props.getProperty("cipher.alg", "AES/GCM/NoPadding");
        return Cipher.getInstance(alg);
    }

    Cipher fromPropsAssign() throws Exception {
        String alg;
        // ok: mois-2-04-weak-cipher — 대입 형태, 기본값이 안전
        alg = System.getProperty("cipher.alg", "AES/CBC/PKCS5Padding");
        return Cipher.getInstance(alg);
    }
}

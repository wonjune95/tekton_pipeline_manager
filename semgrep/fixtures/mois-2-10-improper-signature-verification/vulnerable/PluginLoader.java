package demo;

import com.auth0.jwt.JWT;
import com.auth0.jwt.interfaces.DecodedJWT;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import java.io.File;
import java.io.IOException;
import java.security.GeneralSecurityException;
import java.security.PublicKey;
import java.security.Signature;
import java.util.jar.JarFile;

// 탐지돼야 하는 경우
public class PluginLoader {
    // 다운로드한 JAR 의 전자서명을 확인하지 않는다
    public JarFile open(String downloadedFilePath) throws IOException {
        // ruleid: mois-2-10-improper-signature-verification
        return new JarFile(new File(downloadedFilePath));
    }

    // 서명 확인 생성자를 쓰지만 서명 주체(getCodeSigners)를 검증하지 않는다
    public JarFile openVerified(File f) throws IOException {
        // ruleid: mois-2-10-improper-signature-verification
        return new JarFile(f, true);
    }

    // 서명 확인을 명시적으로 끈다
    public JarFile openUnverified(File f) throws IOException {
        // ruleid: mois-2-10-improper-signature-verification
        return new JarFile(f, false);
    }

    // 서명 주체 확인(getCodeSigners)은 다른 메서드에만 있고 여기서는 부르지 않는다
    public JarFile openWithMode(File f) throws IOException {
        // ruleid: mois-2-10-improper-signature-verification
        return new JarFile(f, true, java.util.zip.ZipFile.OPEN_READ);
    }

    public boolean signedEntry(java.util.jar.JarEntry en) {
        return en.getCodeSigners() != null;
    }

    // jjwt 0.12: 서명 없는 토큰용 파서 메서드
    public Object unsecured(String token) {
        // ruleid: mois-2-10-improper-signature-verification
        return Jwts.parser().build().parseUnsecuredClaims(token).getPayload();
    }

    // jjwt 0.11: parserBuilder() 로 만든 파서의 parse()
    public Object anyBuilder(String token, byte[] key) {
        // ruleid: mois-2-10-improper-signature-verification
        return Jwts.parserBuilder().setSigningKey(key).build().parse(token).getBody();
    }

    // 서명 없는 JWT 를 받아들인다
    public Claims claims(String token) {
        // ruleid: mois-2-10-improper-signature-verification
        return Jwts.parser().parseClaimsJwt(token).getBody();
    }

    // parse() 는 서명 없는 토큰도 그대로 받아들인다 (parseClaimsJws 를 써야 함)
    public Object any(String token, byte[] key) {
        // ruleid: mois-2-10-improper-signature-verification
        return Jwts.parser().setSigningKey(key).parse(token).getBody();
    }

    // 서명을 검증하지 않고 토큰 내용을 꺼낸다
    public String subject(String token) {
        // ruleid: mois-2-10-improper-signature-verification
        DecodedJWT jwt = JWT.decode(token);
        return jwt.getSubject();
    }

    // 서명 검증 결과를 버린다
    public byte[] load(byte[] data, byte[] sig, PublicKey key) throws GeneralSecurityException {
        Signature s = Signature.getInstance("SHA256withRSA");
        s.initVerify(key);
        s.update(data);
        // ruleid: mois-2-10-improper-signature-verification
        s.verify(sig);
        return data;
    }
}

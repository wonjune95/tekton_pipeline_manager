package demo;

import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;

// 탐지돼야 하는 경우: RSA 1024, EC 192, AES 64비트
public class KeyGen {
    public static final String ALGORITHM = "RSA";

    public KeyPair rsa() throws NoSuchAlgorithmException {
        final KeyPairGenerator keyGen = KeyPairGenerator.getInstance(ALGORITHM);
        // ruleid: mois-2-07-insufficient-key-length
        keyGen.initialize(1024);
        return keyGen.generateKeyPair();
    }

    public KeyPair ec() throws NoSuchAlgorithmException {
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("EC");
        // ruleid: mois-2-07-insufficient-key-length
        keyGen.initialize(192);
        return keyGen.generateKeyPair();
    }

    // 제공자 지정, 난수원 인자, DSA·DH
    public KeyPair dsa() throws java.security.GeneralSecurityException {
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("DSA", "SUN");
        // ruleid: mois-2-07-insufficient-key-length
        keyGen.initialize(1024, new java.security.SecureRandom());
        return keyGen.generateKeyPair();
    }

    public KeyPair dh() throws NoSuchAlgorithmException {
        KeyPairGenerator keyGen;
        keyGen = KeyPairGenerator.getInstance("DiffieHellman");
        // ruleid: mois-2-07-insufficient-key-length
        keyGen.initialize(2047);
        return keyGen.generateKeyPair();
    }

    // 상수로 둔 키 길이
    private static final int KEY_SIZE = 512;

    public KeyPair rsaConstant() throws NoSuchAlgorithmException {
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("rsa");
        // ruleid: mois-2-07-insufficient-key-length
        keyGen.initialize(KEY_SIZE);
        return keyGen.generateKeyPair();
    }

    // 파라미터 스펙으로 지정
    public KeyPair rsaSpec() throws java.security.GeneralSecurityException {
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
        // ruleid: mois-2-07-insufficient-key-length
        keyGen.initialize(new java.security.spec.RSAKeyGenParameterSpec(1024, java.security.spec.RSAKeyGenParameterSpec.F4));
        return keyGen.generateKeyPair();
    }

    public KeyPair ecdsa() throws NoSuchAlgorithmException {
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("ECDSA");
        // ruleid: mois-2-07-insufficient-key-length
        keyGen.initialize(224);
        return keyGen.generateKeyPair();
    }

    // 알고리즘 이름별: RSASSA-PSS(Java 11+), DH, ECDH(BouncyCastle)
    public KeyPair rsaPss() throws NoSuchAlgorithmException {
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSASSA-PSS");
        // ruleid: mois-2-07-insufficient-key-length
        keyGen.initialize(1024);
        return keyGen.generateKeyPair();
    }

    public KeyPair dhShort() throws NoSuchAlgorithmException {
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("DH");
        // ruleid: mois-2-07-insufficient-key-length
        keyGen.initialize(1024);
        return keyGen.generateKeyPair();
    }

    public KeyPair ecdh() throws java.security.GeneralSecurityException {
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("ECDH", "BC");
        // ruleid: mois-2-07-insufficient-key-length
        keyGen.initialize(192);
        return keyGen.generateKeyPair();
    }

    public SecretKey des() throws NoSuchAlgorithmException {
        KeyGenerator keyGen = KeyGenerator.getInstance("DES");
        // ruleid: mois-2-07-insufficient-key-length
        keyGen.init(56, new java.security.SecureRandom());
        return keyGen.generateKey();
    }

    // 2048 로 초기화한 것은 다른 생성기다
    public KeyPair otherGenerator() throws NoSuchAlgorithmException {
        KeyPairGenerator strong = KeyPairGenerator.getInstance("RSA");
        strong.initialize(2048);
        KeyPairGenerator weak = KeyPairGenerator.getInstance("RSA");
        // ruleid: mois-2-07-insufficient-key-length
        weak.initialize(1024);
        return weak.generateKeyPair();
    }

    public SecretKey aes() throws NoSuchAlgorithmException {
        KeyGenerator keyGen = KeyGenerator.getInstance("AES");
        // ruleid: mois-2-07-insufficient-key-length
        keyGen.init(64);
        return keyGen.generateKey();
    }
}

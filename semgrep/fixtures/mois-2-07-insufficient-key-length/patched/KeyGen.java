package demo;

import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;

// 탐지되면 안 되는 경우: RSA 2048, EC 256, AES 256비트
public class KeyGen {
    public static final String ALGORITHM = "RSA";

    public KeyPair rsa() throws NoSuchAlgorithmException {
        final KeyPairGenerator keyGen = KeyPairGenerator.getInstance(ALGORITHM);
        // ok: mois-2-07-insufficient-key-length — RSA 2048 (경계값)
        keyGen.initialize(2048);
        return keyGen.generateKeyPair();
    }

    public KeyPair ec() throws NoSuchAlgorithmException {
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("EC");
        // ok: mois-2-07-insufficient-key-length — EC 256 (경계값). RSA 기준(2048)을 EC 에 적용하지 않는다
        keyGen.initialize(256);
        return keyGen.generateKeyPair();
    }

    public SecretKey aes() throws NoSuchAlgorithmException {
        KeyGenerator keyGen = KeyGenerator.getInstance("AES");
        // ok: mois-2-07-insufficient-key-length — AES 256
        keyGen.init(256);
        return keyGen.generateKey();
    }

    public SecretKey aes128() throws NoSuchAlgorithmException {
        KeyGenerator keyGen = KeyGenerator.getInstance("AES");
        // ok: mois-2-07-insufficient-key-length — 대칭키 128 (경계값)
        keyGen.init(128);
        return keyGen.generateKey();
    }

    public KeyPair rsaSpec() throws java.security.GeneralSecurityException {
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
        // ok: mois-2-07-insufficient-key-length — 파라미터 스펙 3072
        keyGen.initialize(new java.security.spec.RSAKeyGenParameterSpec(3072, java.security.spec.RSAKeyGenParameterSpec.F4));
        return keyGen.generateKeyPair();
    }

    public KeyPair ec384() throws NoSuchAlgorithmException {
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("EC");
        // ok: mois-2-07-insufficient-key-length — EC 384 는 2048 보다 작지만 ECC 기준(256)으로 본다
        keyGen.initialize(384, new java.security.SecureRandom());
        return keyGen.generateKeyPair();
    }
}

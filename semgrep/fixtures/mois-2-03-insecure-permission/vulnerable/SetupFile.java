package demo;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.attribute.PosixFilePermission;
import java.nio.file.attribute.PosixFilePermissions;
import java.util.EnumSet;
import java.util.Set;

// 탐지돼야 하는 경우: 모든 사용자에게 권한을 줌
public class SetupFile {
    public void open() {
        File file = new File("/home/setup/system.ini");
        // 모든 사용자에게 실행·읽기·쓰기 권한
        // ruleid: mois-2-03-insecure-permission
        file.setExecutable(true, false);
        // ruleid: mois-2-03-insecure-permission
        file.setReadable(true, false);
        // ruleid: mois-2-03-insecure-permission
        file.setWritable(true, false);
    }

    public void share(Path path) throws IOException {
        // ruleid: mois-2-03-insecure-permission
        Files.setPosixFilePermissions(path, PosixFilePermissions.fromString("rwxrwxrwx"));
    }

    // 다른 사용자에게 쓰기만 열어도 탐지 (rw-rw-rw-, rw----rw-)
    public void worldWritable(Path path) throws IOException {
        // ruleid: mois-2-03-insecure-permission
        Files.setPosixFilePermissions(path, PosixFilePermissions.fromString("rw-rw-rw-"));
        // ruleid: mois-2-03-insecure-permission
        Files.createFile(path, PosixFilePermissions.asFileAttribute(PosixFilePermissions.fromString("rw----rw-")));
    }

    public void othersWrite(Path path) throws IOException {
        // ruleid: mois-2-03-insecure-permission
        Set<PosixFilePermission> perms = EnumSet.of(PosixFilePermission.OWNER_WRITE, PosixFilePermission.OTHERS_WRITE);
        Files.setPosixFilePermissions(path, perms);
    }

    public void umask() throws IOException {
        String cmd = "umask 0";
        // ruleid: mois-2-03-insecure-permission
        Runtime.getRuntime().exec(cmd);
    }

    public void chmod() throws IOException {
        // ruleid: mois-2-03-insecure-permission
        Runtime.getRuntime().exec("chmod 777 /home/setup/system.ini");
        // ruleid: mois-2-03-insecure-permission
        Runtime.getRuntime().exec("chmod -R 0666 /home/setup");
        // ruleid: mois-2-03-insecure-permission
        java.lang.Runtime.getRuntime().exec("chmod o+w /home/setup/system.ini");
        // ruleid: mois-2-03-insecure-permission
        Runtime.getRuntime().exec("chmod a+rw /home/setup/system.ini", null, new File("/home/setup"));
    }
}

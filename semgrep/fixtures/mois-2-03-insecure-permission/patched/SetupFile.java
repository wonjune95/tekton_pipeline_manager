package demo;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.attribute.PosixFilePermission;
import java.nio.file.attribute.PosixFilePermissions;
import java.util.EnumSet;

// 탐지되면 안 되는 경우: 소유자에게만 필요한 권한을 줌
public class SetupFile {
    public void open() {
        File file = new File("/home/setup/system.ini");
        // ok: mois-2-03-insecure-permission — 인자 하나짜리는 소유자에게만 적용된다
        file.setExecutable(false);
        file.setReadable(true);
        file.setWritable(false);
        // ok: mois-2-03-insecure-permission — 두 번째 인자 true = 소유자만
        file.setWritable(true, true);
        // ok: mois-2-03-insecure-permission — 모든 사용자의 권한을 "회수"
        file.setWritable(false, false);
    }

    public void restrict(Path path) throws IOException {
        // ok: mois-2-03-insecure-permission — 다른 사용자에게 쓰기 권한이 없다
        Files.setPosixFilePermissions(path, PosixFilePermissions.fromString("rw-r-----"));
        // ok: mois-2-03-insecure-permission — 다른 사용자는 읽기·실행만 (rwxr-xr-x)
        Files.setPosixFilePermissions(path, PosixFilePermissions.fromString("rwxr-xr-x"));
        // ok: mois-2-03-insecure-permission — 소유자·그룹 권한만
        Files.setPosixFilePermissions(path, EnumSet.of(PosixFilePermission.OWNER_WRITE, PosixFilePermission.GROUP_READ));
    }

    public void chmod() throws IOException {
        // ok: mois-2-03-insecure-permission — 600·750 은 다른 사용자에게 쓰기 권한을 주지 않는다
        Runtime.getRuntime().exec("chmod 600 /home/setup/system.ini");
        Runtime.getRuntime().exec("chmod -R 750 /home/setup");
        // ok: mois-2-03-insecure-permission — umask 077·022 는 권한을 줄인다
        Runtime.getRuntime().exec("umask 077");
        Runtime.getRuntime().exec("umask 022");
        // ok: mois-2-03-insecure-permission — 소유자에게만 쓰기 추가
        Runtime.getRuntime().exec("chmod u+w /home/setup/system.ini");
    }
}

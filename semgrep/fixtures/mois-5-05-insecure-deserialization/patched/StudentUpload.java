package demo;

import com.thoughtworks.xstream.XStream;
import com.thoughtworks.xstream.security.NoTypePermission;
import com.thoughtworks.xstream.security.NullPermission;
import com.thoughtworks.xstream.security.PrimitiveTypePermission;
import java.io.IOException;
import java.io.InputStream;
import java.io.InvalidClassException;
import java.io.ObjectInputFilter;
import java.io.ObjectInputStream;
import java.io.ObjectStreamClass;
import java.util.Collection;
import java.util.Set;
import javax.servlet.http.HttpServletRequest;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

// 탐지되면 안 되는 경우 (진단가이드 5-5 안전한 코드: 허용 클래스 목록으로 제한한 역직렬화)
public class StudentUpload {
    private static final String PATTERN = "demo.Student;java.lang.*;maxdepth=5;!*";
    private static final ObjectInputFilter STUDENT_ONLY = ObjectInputFilter.Config.createFilter("demo.Student;!*");

    static final class WhitelistedObjectInputStream extends ObjectInputStream {
        private final Set<String> whitelist;

        WhitelistedObjectInputStream(InputStream inputStream, Set<String> wl) throws IOException {
            super(inputStream);
            whitelist = wl;
        }

        @Override
        protected Class<?> resolveClass(ObjectStreamClass cls) throws IOException, ClassNotFoundException {
            // 허용 목록에 없는 클래스는 거부한다
            if (!whitelist.contains(cls.getName())) {
                throw new InvalidClassException("Unexpected serialized class", cls.getName());
            }
            return super.resolveClass(cls);
        }
    }

    @PostMapping("/upload")
    public Object upload(@RequestParam("file") MultipartFile multipartFile) throws IOException, ClassNotFoundException {
        try (InputStream fileStream = multipartFile.getInputStream();
             WhitelistedObjectInputStream ois = new WhitelistedObjectInputStream(fileStream, Set.of("demo.Student"))) {
            // ok: mois-5-05-insecure-deserialization — resolveClass 로 허용 클래스를 제한한 하위 클래스
            return ois.readObject();
        }
    }

    public Object filtered(HttpServletRequest req) throws IOException, ClassNotFoundException {
        try (ObjectInputStream ois = new ObjectInputStream(req.getInputStream())) {
            ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter("demo.Student;!*"));
            // ok: mois-5-05-insecure-deserialization — 같은 스트림에, 읽기 전에 ObjectInputFilter 를 걸었다
            return ois.readObject();
        }
    }

    public Object filteredBoth(HttpServletRequest req, MultipartFile file) throws IOException, ClassNotFoundException {
        ObjectInputFilter filter = ObjectInputFilter.Config.createFilter("demo.Student;!*");
        ObjectInputStream a = new ObjectInputStream(req.getInputStream());
        ObjectInputStream b = new ObjectInputStream(file.getInputStream());
        a.setObjectInputFilter(filter);
        b.setObjectInputFilter(filter);
        // ok: mois-5-05-insecure-deserialization — 두 스트림 각각에 필터를 걸었다
        Object first = a.readUnshared();
        Object second = b.readUnshared();
        return first == null ? second : first;
    }

    public Object filteredByConstants(HttpServletRequest req, MultipartFile file) throws IOException, ClassNotFoundException {
        ObjectInputStream a = new ObjectInputStream(req.getInputStream());
        ObjectInputStream b = new ObjectInputStream(file.getInputStream());
        // ok: mois-5-05-insecure-deserialization — 값이 `;!*` 로 끝나는 문자열 상수로 만든 필터
        a.setObjectInputFilter(ObjectInputFilter.Config.createFilter(PATTERN));
        // ok: mois-5-05-insecure-deserialization — 같은 클래스의 final 필드에 담아 둔 필터
        b.setObjectInputFilter(STUDENT_ONLY);
        Object first = a.readObject();
        Object second = b.readObject();
        return first == null ? second : first;
    }

    public Object filteredRejectUndecided(HttpServletRequest req) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        // ok: mois-5-05-insecure-deserialization — 끝에 `!*` 가 없어도 rejectUndecidedClass 가 목록 밖 클래스를 거부한다
        ois.setObjectInputFilter(ObjectInputFilter.rejectUndecidedClass(ObjectInputFilter.Config.createFilter("demo.Student")));
        return ois.readObject();
    }

    @PostMapping("/xml")
    public Object xstream(@RequestBody String xml) {
        // ok: mois-5-05-insecure-deserialization — 같은 XStream 객체를 "모두 거부"로 초기화한 뒤 허용 타입만 더했다
        XStream byClass = new XStream();
        byClass.addPermission(NoTypePermission.NONE);
        byClass.addPermission(NullPermission.NULL);
        byClass.addPermission(PrimitiveTypePermission.PRIMITIVES);
        byClass.allowTypeHierarchy(Collection.class);
        byClass.allowTypes(new Class[] {Student.class});
        Object a = byClass.fromXML(xml);
        XStream byWildcard = new XStream();
        byWildcard.addPermission(NoTypePermission.NONE);
        byWildcard.allowTypesByWildcard(new String[] {"demo.model.*", "demo.dto.**"});
        Object b = byWildcard.fromXML(xml);
        XStream byRegExp = new XStream();
        byRegExp.addPermission(NoTypePermission.NONE);
        byRegExp.allowTypesByRegExp(new String[] {"demo\\.model\\.[A-Z][a-z]+", "^demo\\.dto\\.[A-Za-z]+$"});
        Object c = byRegExp.fromXML(xml);
        // ok: mois-5-05-insecure-deserialization — XStream 이 제공하는 기본 허용 목록으로 초기화했다 (1.4.10~1.4.17)
        XStream byDefault = new XStream();
        XStream.setupDefaultSecurity(byDefault);
        byDefault.allowTypes(new String[] {"demo.Student", "demo.model.Course"});
        Object d = byDefault.fromXML(xml);
        return a == null ? (b == null ? (c == null ? d : c) : b) : a;
    }

    public static final class Student {
        private String name;

        public String getName() {
            return name;
        }
    }
}

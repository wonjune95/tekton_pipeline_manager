package demo;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.jsontype.BasicPolymorphicTypeValidator;
import com.fasterxml.jackson.databind.jsontype.PolymorphicTypeValidator;
import com.thoughtworks.xstream.XStream;
import com.thoughtworks.xstream.security.NoTypePermission;
import com.thoughtworks.xstream.security.NullPermission;
import com.thoughtworks.xstream.security.PrimitiveTypePermission;
import java.io.IOException;
import java.io.ObjectInputFilter;
import java.io.ObjectInputStream;
import java.io.Serializable;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Collection;

// 탐지되면 안 되는 경우: ObjectInputFilter 로 허용 클래스를 제한, JSON 은 정해진 타입으로만 읽음
public class MapStore {
    private static final String PATTERN = "demo.Student;java.lang.*;maxdepth=5;!*";
    private static final ObjectInputFilter STUDENT_ONLY = ObjectInputFilter.Config.createFilter("demo.Student;!*");

    public Object load(String path) throws IOException, ClassNotFoundException {
        try (ObjectInputStream in = new ObjectInputStream(Files.newInputStream(Paths.get(path)))) {
            in.setObjectInputFilter(ObjectInputFilter.Config.createFilter("demo.Student;!*"));
            // ok: mois-5-05-unsafe-deserializer — 같은 스트림에, 읽기 전에 필터를 걸었다
            return in.readObject();
        }
    }

    public Object loadTwo(String p1, String p2) throws IOException, ClassNotFoundException {
        ObjectInputFilter filter = ObjectInputFilter.Config.createFilter("demo.Student;!*");
        try (ObjectInputStream a = new ObjectInputStream(Files.newInputStream(Paths.get(p1)));
             ObjectInputStream b = new ObjectInputStream(Files.newInputStream(Paths.get(p2)))) {
            a.setObjectInputFilter(filter);
            b.setObjectInputFilter(filter);
            // ok: mois-5-05-unsafe-deserializer — 두 스트림 각각에 필터를 걸었다
            Object first = a.readUnshared();
            Object second = b.readUnshared();
            return first == null ? second : first;
        }
    }

    public Student parse(String json) throws IOException {
        // ok: mois-5-05-unsafe-deserializer — 정해진 타입으로만 읽는다
        return new ObjectMapper().readValue(json, Student.class);
    }

    public ObjectMapper polymorphic() {
        ObjectMapper om = new ObjectMapper();
        // ok: mois-5-05-unsafe-deserializer — 허용 하위 타입을 정한 검증기를 쓴다
        om.activateDefaultTyping(
                BasicPolymorphicTypeValidator.builder().allowIfSubType("demo.model.").build(),
                ObjectMapper.DefaultTyping.NON_FINAL);
        return om;
    }

    public ObjectMapper polymorphicViaLocal() {
        PolymorphicTypeValidator ptv = BasicPolymorphicTypeValidator.builder().allowIfSubType("demo.model.").build();
        ObjectMapper om = new ObjectMapper();
        // ok: mois-5-05-unsafe-deserializer — 빌더로 만든 검증기를 지역 변수에 담아 넘겼다
        om.activateDefaultTypingAsProperty(ptv, ObjectMapper.DefaultTyping.NON_FINAL, "@class");
        return om;
    }

    public Object loadByConstants(String p1, String p2) throws IOException, ClassNotFoundException {
        ObjectInputStream a = new ObjectInputStream(Files.newInputStream(Paths.get(p1)));
        ObjectInputStream b = new ObjectInputStream(Files.newInputStream(Paths.get(p2)));
        // ok: mois-5-05-unsafe-deserializer — 값이 `;!*` 로 끝나는 문자열 상수로 만든 필터
        a.setObjectInputFilter(ObjectInputFilter.Config.createFilter(PATTERN));
        // ok: mois-5-05-unsafe-deserializer — 같은 클래스의 final 필드에 담아 둔 필터
        b.setObjectInputFilter(STUDENT_ONLY);
        Object first = a.readObject();
        Object second = b.readObject();
        return first == null ? second : first;
    }

    public Object loadRejectUndecided(String path) throws IOException, ClassNotFoundException {
        ObjectInputStream in = new ObjectInputStream(Files.newInputStream(Paths.get(path)));
        // ok: mois-5-05-unsafe-deserializer — 끝에 `!*` 가 없어도 rejectUndecidedClass 가 목록 밖 클래스를 거부한다
        in.setObjectInputFilter(ObjectInputFilter.rejectUndecidedClass(ObjectInputFilter.Config.createFilter("demo.Student")));
        return in.readObject();
    }

    public Object xstream(String xml) {
        // ok: mois-5-05-unsafe-deserializer — 같은 XStream 객체를 "모두 거부"로 초기화한 뒤 허용 타입만 더했다
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
        // ok: mois-5-05-unsafe-deserializer — XStream 이 제공하는 기본 허용 목록으로 초기화했다 (1.4.10~1.4.17)
        XStream byDefault = new XStream();
        XStream.setupDefaultSecurity(byDefault);
        byDefault.allowTypes(new String[] {"demo.Student", "demo.model.Course"});
        Object d = byDefault.fromXML(xml);
        return a == null ? (b == null ? (c == null ? d : c) : b) : a;
    }

    public static final class Student implements Serializable {
        private static final long serialVersionUID = 1L;
        private String name;

        public String getName() {
            return name;
        }

        // ok: mois-5-05-unsafe-deserializer — 직렬화 훅 안의 읽기는 이미 진행 중인 역직렬화의 일부 (필터는 바깥 스트림에서 건다)
        private void readObject(ObjectInputStream in) throws IOException, ClassNotFoundException {
            in.defaultReadObject();
            Object extra = in.readObject();
            name = String.valueOf(extra);
        }
    }
}

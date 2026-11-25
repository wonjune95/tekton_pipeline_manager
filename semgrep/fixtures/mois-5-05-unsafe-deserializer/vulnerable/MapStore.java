package demo;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.json.JsonMapper;
import com.fasterxml.jackson.databind.jsontype.BasicPolymorphicTypeValidator;
import com.fasterxml.jackson.databind.jsontype.PolymorphicTypeValidator;
import com.fasterxml.jackson.databind.jsontype.impl.LaissezFaireSubTypeValidator;
import com.thoughtworks.xstream.XStream;
import com.thoughtworks.xstream.security.AnyTypePermission;
import com.thoughtworks.xstream.security.NoTypePermission;
import java.beans.XMLDecoder;
import java.io.ByteArrayInputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.ObjectInputFilter;
import java.io.ObjectInputStream;
import java.nio.charset.StandardCharsets;

// 탐지돼야 하는 경우 (진단가이드 5-5: 허용 클래스 제한 없는 역직렬화).
// 탐지 위치는 스트림을 만드는 줄이 아니라 실제로 객체를 읽는 줄이다
public class MapStore {
    // final 이 아닌 필드: 값은 좋아 보여도 다른 곳에서 바꿀 수 있다
    private ObjectInputFilter mutable = ObjectInputFilter.Config.createFilter("demo.Student;!*");
    private static final String FILTER = "demo.Student;!*";
    private static final String OPEN = "demo.dto.*";
    private static final ObjectInputFilter STRICT = ObjectInputFilter.Config.createFilter("demo.Student;!*");

    // ── 필터 없는 ObjectInputStream: readObject · readUnshared ──

    public Object load(String path) throws IOException, ClassNotFoundException {
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream(path))) {
            // ruleid: mois-5-05-unsafe-deserializer
            return in.readObject();
        }
    }

    public Object loadUnshared(String path) throws IOException, ClassNotFoundException {
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream(path))) {
            // ruleid: mois-5-05-unsafe-deserializer
            return in.readUnshared();
        }
    }

    // 스트림을 인자로 받은 경우에도 필터가 보이지 않으면 표시한다
    public Object read(ObjectInputStream in) throws IOException, ClassNotFoundException {
        // ruleid: mois-5-05-unsafe-deserializer
        return in.readObject();
    }

    // ── XMLDecoder ──

    // XMLDecoder 로 문자열 데이터를 역직렬화 (정탐 예)
    public Object byXmlString(String xml) {
        try (XMLDecoder xd = new XMLDecoder(new ByteArrayInputStream(xml.getBytes(StandardCharsets.UTF_8)))) {
            // ruleid: mois-5-05-unsafe-deserializer
            return xd.readObject();
        }
    }

    // ── Jackson 다형성 역직렬화 ──

    // JSON 안의 클래스 이름으로 아무 타입이나 만들 수 있다
    public ObjectMapper mapper() {
        ObjectMapper om = new ObjectMapper();
        // ruleid: mois-5-05-unsafe-deserializer
        om.enableDefaultTyping();
        return om;
    }

    public ObjectMapper laissezFaire() {
        ObjectMapper om = new ObjectMapper();
        // ruleid: mois-5-05-unsafe-deserializer
        om.activateDefaultTyping(LaissezFaireSubTypeValidator.instance, ObjectMapper.DefaultTyping.NON_FINAL);
        return om;
    }

    // 이름만 다른 같은 설정
    public ObjectMapper asProperty() {
        ObjectMapper om = new ObjectMapper();
        // ruleid: mois-5-05-unsafe-deserializer
        om.enableDefaultTypingAsProperty(ObjectMapper.DefaultTyping.NON_FINAL, "@class");
        return om;
    }

    // 검증기 자리에 무엇을 넣든 "검증기가 있다"로 보지 않는다. 기본 검증기는 모두 허용이다
    public ObjectMapper defaultValidator() {
        ObjectMapper om = new ObjectMapper();
        // ruleid: mois-5-05-unsafe-deserializer
        om.activateDefaultTyping(om.getPolymorphicTypeValidator(), ObjectMapper.DefaultTyping.NON_FINAL);
        return om;
    }

    // 검증기를 인자로 받았다: 무엇이 들어올지 알 수 없다
    public ObjectMapper validatorFromCaller(PolymorphicTypeValidator ptv) {
        ObjectMapper om = new ObjectMapper();
        // ruleid: mois-5-05-unsafe-deserializer
        om.activateDefaultTypingAsProperty(ptv, ObjectMapper.DefaultTyping.NON_FINAL, "@class");
        return om;
    }

    // 빌더로 만든 검증기지만 Object 를 허용했다 (모든 클래스)
    public ObjectMapper validatorAllowsObject() {
        ObjectMapper om = new ObjectMapper();
        // ruleid: mois-5-05-unsafe-deserializer
        om.activateDefaultTyping(
                BasicPolymorphicTypeValidator.builder().allowIfBaseType(Object.class).build(),
                ObjectMapper.DefaultTyping.NON_FINAL);
        return om;
    }

    // 같은 검증기를 지역 변수에 담아 JsonMapper 빌더에 넘겼다
    public ObjectMapper validatorAllowsObjectViaLocal() {
        PolymorphicTypeValidator ptv = BasicPolymorphicTypeValidator.builder().allowIfSubType(Object.class).build();
        // ruleid: mois-5-05-unsafe-deserializer
        return JsonMapper.builder().activateDefaultTyping(ptv).build();
    }

    // ── 허용 타입을 정하지 않은 XStream ──

    public Object byXStream(String xml) {
        XStream xstream = new XStream();
        // ruleid: mois-5-05-unsafe-deserializer
        return xstream.fromXML(xml);
    }

    // ── 필터·허용 목록이 있지만 이 객체를 보호하지 못하는 경우 ──

    // 같은 메서드의 다른 스트림(a)에만 필터를 걸었다
    public Object filterOnOtherStream(String p1, String p2) throws IOException, ClassNotFoundException {
        ObjectInputStream a = new ObjectInputStream(new FileInputStream(p1));
        ObjectInputStream b = new ObjectInputStream(new FileInputStream(p2));
        a.setObjectInputFilter(ObjectInputFilter.Config.createFilter(FILTER));
        Object first = a.readObject();
        // ruleid: mois-5-05-unsafe-deserializer
        Object second = b.readObject();
        return first == null ? second : first;
    }

    // 객체를 읽은 뒤에 필터를 걸었다
    public Object filterAfterRead(String path) throws IOException, ClassNotFoundException {
        ObjectInputStream in = new ObjectInputStream(new FileInputStream(path));
        // ruleid: mois-5-05-unsafe-deserializer
        Object o = in.readObject();
        in.setObjectInputFilter(ObjectInputFilter.Config.createFilter(FILTER));
        return o;
    }

    // 필터를 null 로 지웠다
    public Object filterCleared(String path) throws IOException, ClassNotFoundException {
        ObjectInputStream in = new ObjectInputStream(new FileInputStream(path));
        in.setObjectInputFilter(null);
        // ruleid: mois-5-05-unsafe-deserializer
        return in.readObject();
    }

    // ObjectInputStream 의 필터는 XMLDecoder·XStream 과 무관하다
    public Object filterDoesNotCoverOthers(String path, String xml) throws IOException, ClassNotFoundException {
        ObjectInputStream in = new ObjectInputStream(new FileInputStream(path));
        in.setObjectInputFilter(ObjectInputFilter.Config.createFilter(FILTER));
        Object first = in.readObject();
        XMLDecoder xd = new XMLDecoder(new FileInputStream(path));
        // ruleid: mois-5-05-unsafe-deserializer
        Object second = xd.readObject();
        XStream xstream = new XStream();
        // ruleid: mois-5-05-unsafe-deserializer
        Object third = xstream.fromXML(xml);
        return first == null ? (second == null ? third : second) : first;
    }

    // 다른 XStream 객체에만 허용 타입을 정했다 / fromXML 뒤에 정했다 / 모든 타입을 허용했다
    public Object xstreamNotRestricted(String xml) {
        XStream safe = new XStream();
        safe.addPermission(NoTypePermission.NONE);
        safe.allowTypes(new Class[] {String.class});
        XStream other = new XStream();
        // ruleid: mois-5-05-unsafe-deserializer
        Object first = other.fromXML(xml);
        other.addPermission(NoTypePermission.NONE);
        other.allowTypes(new Class[] {String.class});
        XStream any = new XStream();
        any.addPermission(AnyTypePermission.ANY);
        // ruleid: mois-5-05-unsafe-deserializer
        Object second = any.fromXML(xml);
        return first == null ? second : first;
    }

    // ── 필터를 걸었지만 "목록에 없는 클래스는 거부"가 아닌 경우 ──
    // JEP 290 필터는 판단하지 않은(UNDECIDED) 클래스를 통과시킨다. 필터가 있다는 것만으로는 증명이 아니다

    // 한도만 둔 패턴: 클래스는 하나도 거르지 않는다
    public Object filterLimitsOnly(String path) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(path));
        ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter("maxdepth=5;maxrefs=100"));
        // ruleid: mois-5-05-unsafe-deserializer
        return ois.readObject();
    }

    // 허용 항목만 있고 끝에 `!*` 가 없다: 목록 밖 클래스는 미결정으로 통과한다
    public Object filterWithoutRejectAll(String path) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(path));
        ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter("demo.dto.*"));
        // ruleid: mois-5-05-unsafe-deserializer
        return ois.readObject();
    }

    // 모두 허용하는 `*` 항목이 `!*` 보다 앞에 있다 (앞 항목이 먼저 적용된다)
    public Object filterAllowAllFirst(String path) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(path));
        ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter("*;!*"));
        // ruleid: mois-5-05-unsafe-deserializer
        return ois.readObject();
    }

    // 가운데에 `*` 항목이 있다
    public Object filterAllowAllInMiddle(String path) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(path));
        ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter("demo.dto.*;*;!*"));
        // ruleid: mois-5-05-unsafe-deserializer
        return ois.readObject();
    }

    // 구분자를 `;` 가 아니라 `,` 로 썼다: 전체가 한 항목이 되어 아무것도 거부하지 않는다
    public Object filterWrongSeparator(String path) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(path));
        ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter("demo.dto.*,!*"));
        // ruleid: mois-5-05-unsafe-deserializer
        return ois.readObject();
    }

    // 앞부분이 변수: `*;` 가 들어오면 뒤의 `!*` 는 소용없다
    public Object filterPrefixFromVariable(String path, String prefix) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(path));
        ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter(prefix + "demo.Student;!*"));
        // ruleid: mois-5-05-unsafe-deserializer
        return ois.readObject();
    }

    // 이어 붙인 패턴: 끝 항목이 `!*x` 가 되어 x 로 시작하는 클래스만 거부한다
    public Object filterConcatenated(String path) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(path));
        ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter("demo.Student;!*" + "x"));
        // ruleid: mois-5-05-unsafe-deserializer
        return ois.readObject();
    }

    // 패턴 문자열이 변수: 무엇이 들어올지 알 수 없다
    public Object filterFromVariable(String path, String pattern) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(path));
        ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter(pattern));
        // ruleid: mois-5-05-unsafe-deserializer
        return ois.readObject();
    }

    // 상수지만 값이 `!*` 로 끝나지 않는다
    public Object filterFromOpenConstant(String path) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(path));
        ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter(OPEN));
        // ruleid: mois-5-05-unsafe-deserializer
        return ois.readObject();
    }

    // 무조건 허용하는 람다
    public Object filterLambda(String path) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(path));
        ois.setObjectInputFilter(info -> ObjectInputFilter.Status.ALLOWED);
        // ruleid: mois-5-05-unsafe-deserializer
        return ois.readObject();
    }

    // JVM 전역 필터를 다시 건다: 설정하지 않았으면 null 이고 내용도 알 수 없다
    public Object filterProcessWide(String path) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(path));
        ois.setObjectInputFilter(ObjectInputFilter.Config.getSerialFilter());
        // ruleid: mois-5-05-unsafe-deserializer
        return ois.readObject();
    }

    // 지역 변수에 담은 뒤 다른 필터로 바꿨다
    public Object filterReassigned(String path) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(path));
        ObjectInputFilter filter = ObjectInputFilter.Config.createFilter("demo.Student;!*");
        filter = info -> ObjectInputFilter.Status.UNDECIDED;
        ois.setObjectInputFilter(filter);
        // ruleid: mois-5-05-unsafe-deserializer
        return ois.readObject();
    }

    // final 필드 STRICT 를 같은 이름의 지역 변수가 가렸다
    public Object filterShadowedByLocal(String path) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(path));
        ObjectInputFilter STRICT = info -> ObjectInputFilter.Status.ALLOWED;
        ois.setObjectInputFilter(STRICT);
        // ruleid: mois-5-05-unsafe-deserializer
        return ois.readObject();
    }

    // final 필드 STRICT 를 같은 이름의 매개변수가 가렸다
    public Object filterShadowedByParameter(String path, ObjectInputFilter STRICT) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(path));
        ois.setObjectInputFilter(STRICT);
        // ruleid: mois-5-05-unsafe-deserializer
        return ois.readObject();
    }

    // final 이 아닌 필드: 다른 곳에서 바꿀 수 있다
    public Object filterFromMutableField(String path) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(path));
        ois.setObjectInputFilter(mutable);
        // ruleid: mois-5-05-unsafe-deserializer
        return ois.readObject();
    }

    // 필터를 건 뒤 변수에 다른 스트림을 넣었다: 새 스트림에는 필터가 없다
    public Object filterThenStreamReplaced(String p1, String p2) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(p1));
        ois.setObjectInputFilter(STRICT);
        Object first = ois.readObject();
        ois = new ObjectInputStream(new FileInputStream(p2));
        // ruleid: mois-5-05-unsafe-deserializer
        Object second = ois.readObject();
        return first == null ? second : first;
    }

    // rejectUndecidedClass 로 감쌌지만 안쪽 필터가 무조건 허용이라 거부할 미결정 클래스가 없다
    public Object rejectUndecidedAroundAllowAll(String path) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(path));
        ois.setObjectInputFilter(ObjectInputFilter.rejectUndecidedClass(info -> ObjectInputFilter.Status.ALLOWED));
        // ruleid: mois-5-05-unsafe-deserializer
        return ois.readObject();
    }

    // 안쪽이 "모든 클래스 허용" 조건
    public Object rejectUndecidedAroundTruePredicate(String path) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(path));
        ois.setObjectInputFilter(ObjectInputFilter.rejectUndecidedClass(
                ObjectInputFilter.allowFilter(c -> true, ObjectInputFilter.Status.UNDECIDED)));
        // ruleid: mois-5-05-unsafe-deserializer
        return ois.readObject();
    }

    // 안쪽 패턴이 `*` (모두 허용)
    public Object rejectUndecidedAroundStar(String path) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(path));
        ois.setObjectInputFilter(ObjectInputFilter.rejectUndecidedClass(ObjectInputFilter.Config.createFilter("*")));
        // ruleid: mois-5-05-unsafe-deserializer
        return ois.readObject();
    }

    // ── 직렬화 훅처럼 보이지만 훅이 아닌 메서드 ──

    // private 이 아니면 JVM 이 부르는 훅이 아니다. 필터 없는 스트림을 넘겨받아 직접 읽는 메서드다
    public void readObject(ObjectInputStream in) throws IOException, ClassNotFoundException {
        // ruleid: mois-5-05-unsafe-deserializer
        Object extra = in.readObject();
        if (extra == null) {
            throw new IOException("empty");
        }
    }

    // ── XStream: 허용 목록을 정하는 호출은 있지만 "허용 목록만 남았다"는 증명이 아닌 경우 ──

    // 모두 거부로 초기화하지 않았다: XStream 1.4.17 이하는 기본이 모두 허용이라 allowTypes 는 목록을 더할 뿐이다
    public Object xstreamAllowWithoutReset(String xml) {
        XStream xs = new XStream();
        xs.allowTypes(new Class[] {Student.class});
        // ruleid: mois-5-05-unsafe-deserializer
        return xs.fromXML(xml);
    }

    // 모두 거부한 뒤 다시 모두 허용했다 (나중에 넣은 권한이 먼저 적용된다)
    public Object xstreamAnyAfterNone(String xml) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.addPermission(AnyTypePermission.ANY);
        // ruleid: mois-5-05-unsafe-deserializer
        return xs.fromXML(xml);
    }

    // 직접 만든 권한: 무엇을 허용하는지 알 수 없다
    public Object xstreamCustomPermission(String xml) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.addPermission(type -> true);
        // ruleid: mois-5-05-unsafe-deserializer
        return xs.fromXML(xml);
    }

    // 모든 클래스의 상위 타입을 허용했다
    public Object xstreamObjectHierarchy(String xml) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypeHierarchy(Object.class);
        // ruleid: mois-5-05-unsafe-deserializer
        return xs.fromXML(xml);
    }

    // 역직렬화 공격에 쓰이는 클래스는 대부분 Serializable 이다
    public Object xstreamSerializableHierarchy(String xml) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypeHierarchy(java.io.Serializable.class);
        // ruleid: mois-5-05-unsafe-deserializer
        return xs.fromXML(xml);
    }

    // 와일드카드 "**" 는 모든 클래스다
    public Object xstreamWildcardAll(String xml) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypesByWildcard(new String[] {"demo.model.*", "**"});
        // ruleid: mois-5-05-unsafe-deserializer
        return xs.fromXML(xml);
    }

    // 정규식 ".*" 는 모든 클래스다
    public Object xstreamRegExpAll(String xml) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypesByRegExp(new String[] {".*"});
        // ruleid: mois-5-05-unsafe-deserializer
        return xs.fromXML(xml);
    }

    // 패키지 이름으로 시작하지만 `|` 뒤가 모두 허용이다
    public Object xstreamRegExpAlternation(String xml) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypesByRegExp(new String[] {"demo\\.model\\..*|.*"});
        // ruleid: mois-5-05-unsafe-deserializer
        return xs.fromXML(xml);
    }

    // 첫 글자가 있어도 `?` 로 선택 사항이면 모든 클래스다 (패키지 이름 + 점으로 시작해야 제한으로 본다)
    public Object xstreamRegExpOptionalPrefix(String xml) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypesByRegExp(new String[] {"d?.*"});
        // ruleid: mois-5-05-unsafe-deserializer
        return xs.fromXML(xml);
    }

    // 조건문 안에서 다시 모두 허용했다
    public Object xstreamConditionalAny(String xml, boolean dev) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        if (dev) {
            xs.addPermission(AnyTypePermission.ANY);
        }
        // ruleid: mois-5-05-unsafe-deserializer
        return xs.fromXML(xml);
    }

    // 초기화한 뒤 변수에 새 XStream 객체를 넣었다: 새 객체는 초기화되지 않았다
    public Object xstreamReplacedAfterReset(String xml) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs = new XStream();
        // ruleid: mois-5-05-unsafe-deserializer
        return xs.fromXML(xml);
    }

    // 기본 허용 목록으로 초기화한 뒤에도 마찬가지
    public Object xstreamReplacedAfterDefault(String xml) {
        XStream xs = new XStream();
        XStream.setupDefaultSecurity(xs);
        xs = new XStream();
        // ruleid: mois-5-05-unsafe-deserializer
        return xs.fromXML(xml);
    }

    // 상위 타입이 변수: Object.class 가 들어오면 모든 클래스다
    public Object xstreamHierarchyFromVariable(String xml, Class<?> base) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypeHierarchy(base);
        // ruleid: mois-5-05-unsafe-deserializer
        return xs.fromXML(xml);
    }

    // 허용 클래스 배열이 변수
    public Object xstreamTypesFromVariable(String xml, Class[] types) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypes(types);
        // ruleid: mois-5-05-unsafe-deserializer
        return xs.fromXML(xml);
    }

    // 허용할 클래스 이름을 호출한 쪽이 고른다
    public Object xstreamTypeChosenByCaller(String xml, String type) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypes(new String[] {"demo.Student", type});
        // ruleid: mois-5-05-unsafe-deserializer
        return xs.fromXML(xml);
    }

    // 허용 목록이 변수: 무엇이 들어올지 알 수 없다
    public Object xstreamWildcardFromVariable(String xml, String[] patterns) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypesByWildcard(patterns);
        // ruleid: mois-5-05-unsafe-deserializer
        return xs.fromXML(xml);
    }

    // 정규식 목록이 변수
    public Object xstreamRegExpFromVariable(String xml, String[] patterns) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypesByRegExp(patterns);
        // ruleid: mois-5-05-unsafe-deserializer
        return xs.fromXML(xml);
    }

    // 실행 중에 만든 항목
    public Object xstreamWildcardBuilt(String xml, String prefix) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypesByWildcard(new String[] {prefix + ".**"});
        // ruleid: mois-5-05-unsafe-deserializer
        return xs.fromXML(xml);
    }

    public static final class Student {
    }
}

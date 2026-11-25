package demo;

import com.thoughtworks.xstream.XStream;
import com.thoughtworks.xstream.security.AnyTypePermission;
import com.thoughtworks.xstream.security.NoTypePermission;
import java.beans.XMLDecoder;
import java.io.BufferedInputStream;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectInput;
import java.io.ObjectInputFilter;
import java.io.ObjectInputStream;
import java.net.Socket;
import java.util.Base64;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

// 탐지돼야 하는 경우 (진단가이드 5-5: 요청 본문·업로드 파일·소켓 입력을 검증 없이 역직렬화).
// 탐지 위치는 스트림을 만드는 줄이 아니라 실제로 객체를 읽는 줄(readObject·readUnshared·fromXML)이다
public class ImageServlet extends HttpServlet {
    // final 이 아닌 필드: 값은 좋아 보여도 다른 곳에서 바꿀 수 있다
    private ObjectInputFilter mutable = ObjectInputFilter.Config.createFilter("demo.Student;!*");
    private static final String FILTER = "demo.Student;!*";
    private static final String OPEN = "demo.dto.*";
    private static final ObjectInputFilter STRICT = ObjectInputFilter.Config.createFilter("demo.Student;!*");

    // ── sink: ObjectInputStream.readObject / readUnshared, ObjectInput, XMLDecoder, XStream ──

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse res) throws IOException {
        // HttpServletRequest 의 InputStream 은 사용자 입력값이다
        try (ObjectInputStream ois = new ObjectInputStream(req.getInputStream())) {
            // ruleid: mois-5-05-insecure-deserialization
            res.setStatus(ois.readObject() == null ? 400 : 200);
        } catch (ClassNotFoundException e) {
            res.setStatus(400);
        }
    }

    // 다른 스트림으로 감싸도 같다
    protected Object wrapped(HttpServletRequest req) throws IOException, ClassNotFoundException {
        InputStream in = new BufferedInputStream(req.getInputStream());
        ObjectInputStream ois = new ObjectInputStream(in);
        // ruleid: mois-5-05-insecure-deserialization
        return ois.readUnshared();
    }

    // 파라미터로 받은 Base64 문자열을 풀어 역직렬화
    protected Object fromParameter(HttpServletRequest req) throws IOException, ClassNotFoundException {
        byte[] raw = Base64.getDecoder().decode(req.getParameter("data"));
        // ruleid: mois-5-05-insecure-deserialization
        return new ObjectInputStream(new ByteArrayInputStream(raw)).readObject();
    }

    // 인터페이스 타입(ObjectInput)으로 받은 경우
    protected Object byInterface(HttpServletRequest req) throws IOException, ClassNotFoundException {
        ObjectInput in = new ObjectInputStream(req.getInputStream());
        // ruleid: mois-5-05-insecure-deserialization
        return in.readObject();
    }

    protected Object byXmlDecoder(HttpServletRequest req) throws IOException {
        try (XMLDecoder decoder = new XMLDecoder(req.getInputStream())) {
            // ruleid: mois-5-05-insecure-deserialization
            return decoder.readObject();
        }
    }

    @PostMapping("/xml")
    public Object byXStream(@RequestBody String xml) {
        XStream xstream = new XStream();
        // ruleid: mois-5-05-insecure-deserialization
        return xstream.fromXML(xml);
    }

    // ── 이 규칙에만 있는 입력 지점: 업로드 파일의 스트림, 소켓 ──

    @PostMapping("/upload")
    public Object upload(@RequestParam("file") MultipartFile multipartFile) throws IOException, ClassNotFoundException {
        try (ObjectInputStream ois = new ObjectInputStream(multipartFile.getInputStream())) {
            // ruleid: mois-5-05-insecure-deserialization
            return ois.readObject();
        }
    }

    public Object fromPart(MultipartFile part) throws IOException, ClassNotFoundException {
        try (InputStream in = part.getInputStream(); ObjectInputStream ois = new ObjectInputStream(in)) {
            // ruleid: mois-5-05-insecure-deserialization
            return ois.readObject();
        }
    }

    public Object fromSocket(Socket socket) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(socket.getInputStream());
        // ruleid: mois-5-05-insecure-deserialization
        return ois.readObject();
    }

    // ── 필터가 있지만 이 스트림을 보호하지 못하는 경우 ──

    // 같은 메서드의 다른 스트림(a)에만 필터를 걸었다
    protected Object filterOnOtherStream(HttpServletRequest req, MultipartFile file) throws IOException, ClassNotFoundException {
        ObjectInputStream a = new ObjectInputStream(req.getInputStream());
        ObjectInputStream b = new ObjectInputStream(file.getInputStream());
        a.setObjectInputFilter(ObjectInputFilter.Config.createFilter(FILTER));
        Object first = a.readObject();
        // ruleid: mois-5-05-insecure-deserialization
        Object second = b.readObject();
        return first == null ? second : first;
    }

    // 객체를 읽은 뒤에 필터를 걸었다
    protected Object filterAfterRead(HttpServletRequest req) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        // ruleid: mois-5-05-insecure-deserialization
        Object o = ois.readObject();
        ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter(FILTER));
        return o;
    }

    // 필터를 null 로 지웠다
    protected Object filterCleared(HttpServletRequest req) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        ois.setObjectInputFilter(null);
        // ruleid: mois-5-05-insecure-deserialization
        return ois.readObject();
    }

    // ObjectInputStream 의 필터는 XMLDecoder 와 무관하다
    protected Object filterDoesNotCoverXmlDecoder(HttpServletRequest req) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter(FILTER));
        Object first = ois.readObject();
        XMLDecoder decoder = new XMLDecoder(req.getInputStream());
        // ruleid: mois-5-05-insecure-deserialization
        Object second = decoder.readObject();
        return first == null ? second : first;
    }

    // 다른 XStream 객체에만 허용 타입을 정했다 / fromXML 뒤에 정했다 / 모든 타입을 허용했다
    @PostMapping("/xml2")
    public Object xstreamNotRestricted(@RequestBody String xml) {
        XStream safe = new XStream();
        safe.addPermission(NoTypePermission.NONE);
        safe.allowTypes(new Class[] {String.class});
        XStream other = new XStream();
        // ruleid: mois-5-05-insecure-deserialization
        Object first = other.fromXML(xml);
        other.addPermission(NoTypePermission.NONE);
        other.allowTypes(new Class[] {String.class});
        XStream any = new XStream();
        any.addPermission(AnyTypePermission.ANY);
        // ruleid: mois-5-05-insecure-deserialization
        Object second = any.fromXML(xml);
        return first == null ? second : first;
    }

    // ── 필터를 걸었지만 "목록에 없는 클래스는 거부"가 아닌 경우 ──
    // JEP 290 필터는 판단하지 않은(UNDECIDED) 클래스를 통과시킨다. 필터가 있다는 것만으로는 증명이 아니다

    // 한도만 둔 패턴: 클래스는 하나도 거르지 않는다
    protected Object filterLimitsOnly(HttpServletRequest req) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter("maxdepth=5;maxrefs=100"));
        // ruleid: mois-5-05-insecure-deserialization
        return ois.readObject();
    }

    // 허용 항목만 있고 끝에 `!*` 가 없다: 목록 밖 클래스는 미결정으로 통과한다
    protected Object filterWithoutRejectAll(HttpServletRequest req) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter("demo.dto.*"));
        // ruleid: mois-5-05-insecure-deserialization
        return ois.readObject();
    }

    // 모두 허용하는 `*` 항목이 `!*` 보다 앞에 있다 (앞 항목이 먼저 적용된다)
    protected Object filterAllowAllFirst(HttpServletRequest req) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter("*;!*"));
        // ruleid: mois-5-05-insecure-deserialization
        return ois.readObject();
    }

    // 가운데에 `*` 항목이 있다
    protected Object filterAllowAllInMiddle(HttpServletRequest req) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter("demo.dto.*;*;!*"));
        // ruleid: mois-5-05-insecure-deserialization
        return ois.readObject();
    }

    // 구분자를 `;` 가 아니라 `,` 로 썼다: 전체가 한 항목이 되어 아무것도 거부하지 않는다
    protected Object filterWrongSeparator(HttpServletRequest req) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter("demo.dto.*,!*"));
        // ruleid: mois-5-05-insecure-deserialization
        return ois.readObject();
    }

    // 앞부분이 변수: `*;` 가 들어오면 뒤의 `!*` 는 소용없다
    protected Object filterPrefixFromVariable(HttpServletRequest req, String prefix) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter(prefix + "demo.Student;!*"));
        // ruleid: mois-5-05-insecure-deserialization
        return ois.readObject();
    }

    // 이어 붙인 패턴: 끝 항목이 `!*x` 가 되어 x 로 시작하는 클래스만 거부한다
    protected Object filterConcatenated(HttpServletRequest req) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter("demo.Student;!*" + "x"));
        // ruleid: mois-5-05-insecure-deserialization
        return ois.readObject();
    }

    // 패턴 문자열이 변수: 무엇이 들어올지 알 수 없다
    protected Object filterFromVariable(HttpServletRequest req, String pattern) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter(pattern));
        // ruleid: mois-5-05-insecure-deserialization
        return ois.readObject();
    }

    // 상수지만 값이 `!*` 로 끝나지 않는다
    protected Object filterFromOpenConstant(HttpServletRequest req) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter(OPEN));
        // ruleid: mois-5-05-insecure-deserialization
        return ois.readObject();
    }

    // 무조건 허용하는 람다
    protected Object filterLambda(HttpServletRequest req) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        ois.setObjectInputFilter(info -> ObjectInputFilter.Status.ALLOWED);
        // ruleid: mois-5-05-insecure-deserialization
        return ois.readObject();
    }

    // JVM 전역 필터를 다시 건다: 설정하지 않았으면 null 이고 내용도 알 수 없다
    protected Object filterProcessWide(HttpServletRequest req) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        ois.setObjectInputFilter(ObjectInputFilter.Config.getSerialFilter());
        // ruleid: mois-5-05-insecure-deserialization
        return ois.readObject();
    }

    // 지역 변수에 담은 뒤 다른 필터로 바꿨다
    protected Object filterReassigned(HttpServletRequest req) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        ObjectInputFilter filter = ObjectInputFilter.Config.createFilter("demo.Student;!*");
        filter = info -> ObjectInputFilter.Status.UNDECIDED;
        ois.setObjectInputFilter(filter);
        // ruleid: mois-5-05-insecure-deserialization
        return ois.readObject();
    }

    // final 필드 STRICT 를 같은 이름의 지역 변수가 가렸다
    protected Object filterShadowedByLocal(HttpServletRequest req) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        ObjectInputFilter STRICT = info -> ObjectInputFilter.Status.ALLOWED;
        ois.setObjectInputFilter(STRICT);
        // ruleid: mois-5-05-insecure-deserialization
        return ois.readObject();
    }

    // final 필드 STRICT 를 같은 이름의 매개변수가 가렸다
    protected Object filterShadowedByParameter(HttpServletRequest req, ObjectInputFilter STRICT) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        ois.setObjectInputFilter(STRICT);
        // ruleid: mois-5-05-insecure-deserialization
        return ois.readObject();
    }

    // final 이 아닌 필드: 다른 곳에서 바꿀 수 있다
    protected Object filterFromMutableField(HttpServletRequest req) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        ois.setObjectInputFilter(mutable);
        // ruleid: mois-5-05-insecure-deserialization
        return ois.readObject();
    }

    // 필터를 건 뒤 변수에 다른 스트림을 넣었다: 새 스트림에는 필터가 없다
    protected Object filterThenStreamReplaced(HttpServletRequest req, MultipartFile file) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        ois.setObjectInputFilter(STRICT);
        Object first = ois.readObject();
        ois = new ObjectInputStream(file.getInputStream());
        // ruleid: mois-5-05-insecure-deserialization
        Object second = ois.readObject();
        return first == null ? second : first;
    }

    // rejectUndecidedClass 로 감쌌지만 안쪽 필터가 무조건 허용이라 거부할 미결정 클래스가 없다
    protected Object rejectUndecidedAroundAllowAll(HttpServletRequest req) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        ois.setObjectInputFilter(ObjectInputFilter.rejectUndecidedClass(info -> ObjectInputFilter.Status.ALLOWED));
        // ruleid: mois-5-05-insecure-deserialization
        return ois.readObject();
    }

    // 안쪽이 "모든 클래스 허용" 조건
    protected Object rejectUndecidedAroundTruePredicate(HttpServletRequest req) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        ois.setObjectInputFilter(ObjectInputFilter.rejectUndecidedClass(
                ObjectInputFilter.allowFilter(c -> true, ObjectInputFilter.Status.UNDECIDED)));
        // ruleid: mois-5-05-insecure-deserialization
        return ois.readObject();
    }

    // 안쪽 패턴이 `*` (모두 허용)
    protected Object rejectUndecidedAroundStar(HttpServletRequest req) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
        ois.setObjectInputFilter(ObjectInputFilter.rejectUndecidedClass(ObjectInputFilter.Config.createFilter("*")));
        // ruleid: mois-5-05-insecure-deserialization
        return ois.readObject();
    }

    // ── XStream: 허용 목록을 정하는 호출은 있지만 "허용 목록만 남았다"는 증명이 아닌 경우 ──

    // 모두 거부로 초기화하지 않았다: XStream 1.4.17 이하는 기본이 모두 허용이라 allowTypes 는 목록을 더할 뿐이다
    @PostMapping("/xml/xstreamAllowWithoutReset")
    public Object xstreamAllowWithoutReset(@RequestBody String xml) {
        XStream xs = new XStream();
        xs.allowTypes(new Class[] {Student.class});
        // ruleid: mois-5-05-insecure-deserialization
        return xs.fromXML(xml);
    }

    // 모두 거부한 뒤 다시 모두 허용했다 (나중에 넣은 권한이 먼저 적용된다)
    @PostMapping("/xml/xstreamAnyAfterNone")
    public Object xstreamAnyAfterNone(@RequestBody String xml) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.addPermission(AnyTypePermission.ANY);
        // ruleid: mois-5-05-insecure-deserialization
        return xs.fromXML(xml);
    }

    // 직접 만든 권한: 무엇을 허용하는지 알 수 없다
    @PostMapping("/xml/xstreamCustomPermission")
    public Object xstreamCustomPermission(@RequestBody String xml) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.addPermission(type -> true);
        // ruleid: mois-5-05-insecure-deserialization
        return xs.fromXML(xml);
    }

    // 모든 클래스의 상위 타입을 허용했다
    @PostMapping("/xml/xstreamObjectHierarchy")
    public Object xstreamObjectHierarchy(@RequestBody String xml) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypeHierarchy(Object.class);
        // ruleid: mois-5-05-insecure-deserialization
        return xs.fromXML(xml);
    }

    // 역직렬화 공격에 쓰이는 클래스는 대부분 Serializable 이다
    @PostMapping("/xml/xstreamSerializableHierarchy")
    public Object xstreamSerializableHierarchy(@RequestBody String xml) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypeHierarchy(java.io.Serializable.class);
        // ruleid: mois-5-05-insecure-deserialization
        return xs.fromXML(xml);
    }

    // 와일드카드 "**" 는 모든 클래스다
    @PostMapping("/xml/xstreamWildcardAll")
    public Object xstreamWildcardAll(@RequestBody String xml) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypesByWildcard(new String[] {"demo.model.*", "**"});
        // ruleid: mois-5-05-insecure-deserialization
        return xs.fromXML(xml);
    }

    // 정규식 ".*" 는 모든 클래스다
    @PostMapping("/xml/xstreamRegExpAll")
    public Object xstreamRegExpAll(@RequestBody String xml) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypesByRegExp(new String[] {".*"});
        // ruleid: mois-5-05-insecure-deserialization
        return xs.fromXML(xml);
    }

    // 패키지 이름으로 시작하지만 `|` 뒤가 모두 허용이다
    @PostMapping("/xml/xstreamRegExpAlternation")
    public Object xstreamRegExpAlternation(@RequestBody String xml) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypesByRegExp(new String[] {"demo\\.model\\..*|.*"});
        // ruleid: mois-5-05-insecure-deserialization
        return xs.fromXML(xml);
    }

    // 첫 글자가 있어도 `?` 로 선택 사항이면 모든 클래스다 (패키지 이름 + 점으로 시작해야 제한으로 본다)
    @PostMapping("/xml/xstreamRegExpOptionalPrefix")
    public Object xstreamRegExpOptionalPrefix(@RequestBody String xml) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypesByRegExp(new String[] {"d?.*"});
        // ruleid: mois-5-05-insecure-deserialization
        return xs.fromXML(xml);
    }

    // 조건문 안에서 다시 모두 허용했다
    @PostMapping("/xml/xstreamConditionalAny")
    public Object xstreamConditionalAny(@RequestBody String xml, boolean dev) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        if (dev) {
            xs.addPermission(AnyTypePermission.ANY);
        }
        // ruleid: mois-5-05-insecure-deserialization
        return xs.fromXML(xml);
    }

    // 초기화한 뒤 변수에 새 XStream 객체를 넣었다: 새 객체는 초기화되지 않았다
    @PostMapping("/xml/xstreamReplacedAfterReset")
    public Object xstreamReplacedAfterReset(@RequestBody String xml) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs = new XStream();
        // ruleid: mois-5-05-insecure-deserialization
        return xs.fromXML(xml);
    }

    // 기본 허용 목록으로 초기화한 뒤에도 마찬가지
    @PostMapping("/xml/xstreamReplacedAfterDefault")
    public Object xstreamReplacedAfterDefault(@RequestBody String xml) {
        XStream xs = new XStream();
        XStream.setupDefaultSecurity(xs);
        xs = new XStream();
        // ruleid: mois-5-05-insecure-deserialization
        return xs.fromXML(xml);
    }

    // 상위 타입이 변수: Object.class 가 들어오면 모든 클래스다
    @PostMapping("/xml/xstreamHierarchyFromVariable")
    public Object xstreamHierarchyFromVariable(@RequestBody String xml, Class<?> base) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypeHierarchy(base);
        // ruleid: mois-5-05-insecure-deserialization
        return xs.fromXML(xml);
    }

    // 허용 클래스 배열이 변수
    @PostMapping("/xml/xstreamTypesFromVariable")
    public Object xstreamTypesFromVariable(@RequestBody String xml, Class[] types) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypes(types);
        // ruleid: mois-5-05-insecure-deserialization
        return xs.fromXML(xml);
    }

    // 허용할 클래스 이름을 호출한 쪽이 고른다
    @PostMapping("/xml/xstreamTypeChosenByCaller")
    public Object xstreamTypeChosenByCaller(@RequestBody String xml, String type) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypes(new String[] {"demo.Student", type});
        // ruleid: mois-5-05-insecure-deserialization
        return xs.fromXML(xml);
    }

    // 허용 목록이 변수: 무엇이 들어올지 알 수 없다
    @PostMapping("/xml/xstreamWildcardFromVariable")
    public Object xstreamWildcardFromVariable(@RequestBody String xml, String[] patterns) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypesByWildcard(patterns);
        // ruleid: mois-5-05-insecure-deserialization
        return xs.fromXML(xml);
    }

    // 정규식 목록이 변수
    @PostMapping("/xml/xstreamRegExpFromVariable")
    public Object xstreamRegExpFromVariable(@RequestBody String xml, String[] patterns) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypesByRegExp(patterns);
        // ruleid: mois-5-05-insecure-deserialization
        return xs.fromXML(xml);
    }

    // 실행 중에 만든 항목
    @PostMapping("/xml/xstreamWildcardBuilt")
    public Object xstreamWildcardBuilt(@RequestBody String xml, String prefix) {
        XStream xs = new XStream();
        xs.addPermission(NoTypePermission.NONE);
        xs.allowTypesByWildcard(new String[] {prefix + ".**"});
        // ruleid: mois-5-05-insecure-deserialization
        return xs.fromXML(xml);
    }

    public static final class Student {
    }
}

package demo;

import java.io.IOException;
import javax.annotation.PostConstruct;
import javax.annotation.Resource;
import javax.servlet.ServletConfig;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Controller;
import org.springframework.stereotype.Service;
import org.springframework.web.context.annotation.RequestScope;
import org.springframework.web.context.annotation.SessionScope;

// 탐지되면 안 되는 경우 (진단가이드 6-1 안전한 코드와 오탐 예: 지역 변수 사용, final 상수, 주입 필드, 초기화 때 정하는 설정값)
public class U488 extends HttpServlet {
    private static final long serialVersionUID = 1L;
    private final String greeting = "thanks for visiting";
    // ok: mois-6-01-shared-field-in-singleton — 요청 처리 중에는 바뀌지 않는 설정값 (init() 에서 한 번 정함)
    private String uploadDir;
    private int maxSize;
    // ok: mois-6-01-shared-field-in-singleton — 어디서도 쓰지 않는 멤버 변수는 표시하지 않는다
    private String name;

    public U488() {
        // ok: mois-6-01-shared-field-in-singleton — 생성자
        this.maxSize = 1024;
    }

    @Override
    public void init(ServletConfig config) {
        // ok: mois-6-01-shared-field-in-singleton — 서블릿 초기화
        uploadDir = config.getInitParameter("uploadDir");
    }

    @Override
    public void destroy() {
        uploadDir = null;
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-6-01-shared-field-in-singleton — 필드와 이름이 같은 지역 변수
        String name = request.getParameter("name");
        name = name == null ? "" : name.trim();
        int maxSize;
        maxSize = name.length();
        response.setStatus(name.isEmpty() || maxSize > 20 ? 400 : 200);
    }

    // ok: mois-6-01-shared-field-in-singleton — 필드와 이름이 같은 인자에 다시 대입 (this 없음)
    private String normalize(String uploadDir) {
        uploadDir = uploadDir.trim();
        return uploadDir + greeting;
    }
}

@Controller
class TrendForecastController {
    @Resource(name = "forecastService")
    private Object forecastService;
    private Object mailer;
    private String region;
    private String zone;

    public int doSomething(HttpServletRequest request) {
        // 지역변수로 사용하여 스레드 간 공유되지 않도록 한다
        int currentPage = Integer.valueOf(request.getParameter("page")).intValue();
        return currentPage;
    }

    // ok: mois-6-01-shared-field-in-singleton — setter 주입
    public void setMailer(Object mailer) {
        this.mailer = mailer;
    }

    // ok: mois-6-01-shared-field-in-singleton — 주입용 메서드
    @Autowired
    public void configure(Object mailer) {
        this.mailer = mailer;
    }

    // ok: mois-6-01-shared-field-in-singleton — 빈 초기화
    @PostConstruct
    public void start() {
        region = "kr";
    }

    public void afterPropertiesSet() {
        zone = "kr-1";
    }
}

// ok: mois-6-01-shared-field-in-singleton — 요청·세션마다, 또는 주입할 때마다 새로 만드는 빈은 공유되지 않는다
@Component
@Scope("prototype")
class ImportJob {
    private String fileName;

    public void start(String fileName) {
        this.fileName = fileName;
    }
}

@Component
@RequestScope
class RequestContext {
    private String userId;

    public void bind(String id) {
        userId = id;
    }
}

@Component
@SessionScope
class Cart {
    private int items;

    public void add() {
        items++;
    }
}

// ok: mois-6-01-shared-field-in-singleton — 서블릿도 빈도 아닌 일반 객체
class PageRequest {
    private int page;

    public void next() {
        page++;
    }
}

@Service
class ForecastService {
    private final String region;

    ForecastService() {
        this.region = "kr";
    }

    public String regionOf(HttpServletRequest request) {
        String override = request.getParameter("region");
        return override == null ? region : override;
    }
}

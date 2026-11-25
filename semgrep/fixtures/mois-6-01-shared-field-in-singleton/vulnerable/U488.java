package demo;

import java.io.IOException;
import javax.servlet.GenericServlet;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Controller;
import org.springframework.stereotype.Repository;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.RestController;

// 탐지돼야 하는 경우 (진단가이드 6-1: 서블릿·Controller 의 멤버 변수에 요청 값 저장).
// 탐지 위치는 멤버 변수 선언이 아니라, 요청 처리 메서드에서 멤버 변수에 쓰는 줄이다
public class U488 extends HttpServlet {
    private String name;
    private int hits = 0;

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-6-01-shared-field-in-singleton
        name = request.getParameter("name");
        // ruleid: mois-6-01-shared-field-in-singleton
        hits++;
        response.setStatus(name == null ? 400 : 200);
    }

    // 인자 이름이 필드와 같아도 this.name 은 필드다
    private void remember(String name) {
        // ruleid: mois-6-01-shared-field-in-singleton
        this.name = name;
    }
}

class LegacyServlet extends GenericServlet {
    private String lastUser;

    @Override
    public void service(ServletRequest req, ServletResponse res) {
        // ruleid: mois-6-01-shared-field-in-singleton
        lastUser = req.getParameter("user");
    }
}

@Controller
class TrendForecastController {
    // Controller 의 int 필드가 멤버 변수로 선언되어 스레드 간에 공유됨
    private int currentPage = 1;

    public void doSomething(HttpServletRequest request) {
        // ruleid: mois-6-01-shared-field-in-singleton
        currentPage = Integer.valueOf(request.getParameter("page")).intValue();
    }
}

@RestController
class CounterApi {
    private long total;
    private int open;

    public long add(long amount) {
        // ruleid: mois-6-01-shared-field-in-singleton
        total += amount;
        // ruleid: mois-6-01-shared-field-in-singleton
        ++open;
        return total;
    }

    public void done() {
        // ruleid: mois-6-01-shared-field-in-singleton
        open--;
        // ruleid: mois-6-01-shared-field-in-singleton
        --open;
    }
}

@Service("orderService")
class OrderService {
    private String currentUser;
    private long total;
    private int open;

    public void begin(String userId, long amount) {
        // ruleid: mois-6-01-shared-field-in-singleton
        this.currentUser = userId;
        // ruleid: mois-6-01-shared-field-in-singleton
        this.total += amount;
        // ruleid: mois-6-01-shared-field-in-singleton
        this.open++;
        // ruleid: mois-6-01-shared-field-in-singleton
        ++this.open;
    }

    public void end() {
        // ruleid: mois-6-01-shared-field-in-singleton
        this.open--;
        // ruleid: mois-6-01-shared-field-in-singleton
        --this.open;
    }

    // set 으로 시작하지만 setter 가 아니다 (set 뒤가 대문자가 아님)
    public void settle(String userId) {
        // ruleid: mois-6-01-shared-field-in-singleton
        currentUser = userId;
    }
}

@Component
class RequestContextHolder {
    private String tenant;

    public void bind(String tenantId) {
        // ruleid: mois-6-01-shared-field-in-singleton
        tenant = tenantId;
    }
}

@Repository
class AuditRepository {
    private String lastQuery;

    public void find(String keyword) {
        // ruleid: mois-6-01-shared-field-in-singleton
        lastQuery = keyword;
    }
}

// 범위를 명시했지만 싱글톤이다
@Component
@Scope("singleton")
class ExplicitSingleton {
    private String tenant;

    public void bind(String tenantId) {
        // ruleid: mois-6-01-shared-field-in-singleton
        tenant = tenantId;
    }
}

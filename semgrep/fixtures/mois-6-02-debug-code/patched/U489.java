package demo;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;

// 탐지되면 안 되는 경우: 디버그 출력 대신 로거, main() 은 Spring Boot 시작 클래스에만
public class U489 extends HttpServlet {
    private static final Logger LOG = LoggerFactory.getLogger(U489.class);

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) {
        // ok: mois-6-02-debug-code — 콘솔이 아니라 로거로 남긴다
        LOG.debug("요청 처리");
        response.setStatus(200);
    }
}

@SpringBootApplication
class DemoApplication {
    // ok: mois-6-02-debug-code — Spring Boot 시작 클래스의 main
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}

@SpringBootApplication(scanBasePackages = "demo")
class AdminApplication {
    // ok: mois-6-02-debug-code — 애너테이션에 인자가 있는 시작 클래스 (SpringApplicationBuilder 로 시작)
    public static void main(String[] args) {
        new SpringApplicationBuilder(AdminApplication.class).run(args);
    }
}

@SpringBootApplication
class BatchApplication {
    // ok: mois-6-02-debug-code — 인자 없는 애너테이션 + SpringApplicationBuilder
    public static void main(String[] args) {
        new SpringApplicationBuilder(BatchApplication.class).run(args);
    }
}

class Launcher {
    // ok: mois-6-02-debug-code — 애너테이션은 다른 클래스에 있어도 SpringApplication.run 으로 시작하는 main
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}

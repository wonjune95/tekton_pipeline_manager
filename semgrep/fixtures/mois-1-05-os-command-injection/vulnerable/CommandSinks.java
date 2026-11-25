package demo;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import javax.servlet.http.HttpServletRequest;

// sink 가지마다 한 줄씩: Runtime·ProcessBuilder 를 짧은 이름과 전체 이름으로, 변수에 담은 경우와 바로 쓰는 경우
public class CommandSinks {
    public void runtime(HttpServletRequest request) throws IOException {
        String cmd = request.getParameter("cmd");
        Runtime runtime = Runtime.getRuntime();
        // ruleid: mois-1-05-os-command-injection
        runtime.exec(cmd);
        java.lang.Runtime qualified = java.lang.Runtime.getRuntime();
        // ruleid: mois-1-05-os-command-injection
        qualified.exec(cmd);
        // ruleid: mois-1-05-os-command-injection
        java.lang.Runtime.getRuntime().exec(cmd);
        // 환경변수 인자로 들어가는 경우도 같은 호출로 본다
        // ruleid: mois-1-05-os-command-injection
        Runtime.getRuntime().exec("env", new String[] {"TARGET=" + cmd});
    }

    public void processBuilder(HttpServletRequest request) throws IOException {
        String cmd = request.getParameter("cmd");
        // ruleid: mois-1-05-os-command-injection
        new java.lang.ProcessBuilder("sh", "-c", cmd).start();
        ProcessBuilder builder = new ProcessBuilder();
        // ruleid: mois-1-05-os-command-injection
        builder.command("sh", "-c", cmd);
        java.lang.ProcessBuilder qualified = new java.lang.ProcessBuilder();
        // ruleid: mois-1-05-os-command-injection
        qualified.command("sh", "-c", cmd);
    }

    // 명령어를 리스트로 조립: add 로 넣은 값이 리스트 전체를 오염시킨다
    public void commandList(HttpServletRequest request) throws IOException {
        List<String> args = new ArrayList<>();
        args.add("sh");
        args.add("-c");
        args.add(request.getParameter("cmd"));
        ProcessBuilder builder = new ProcessBuilder();
        // ruleid: mois-1-05-os-command-injection
        builder.command(args);
        // ruleid: mois-1-05-os-command-injection
        new ProcessBuilder(args).start();
        // ruleid: mois-1-05-os-command-injection
        new ProcessBuilder(Arrays.asList("sh", "-c", request.getParameter("script"))).start();
    }
}

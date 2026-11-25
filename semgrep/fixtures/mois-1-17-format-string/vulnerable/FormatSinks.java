package demo;

import java.io.IOException;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.text.MessageFormat;
import java.util.Formatter;
import java.util.Locale;
import javax.servlet.http.HttpServletRequest;

// sink 가지마다 한 줄씩: 외부 입력이 각 API 의 형식 문자열 자리에 들어감
public class FormatSinks {
    private PrintStream stream;
    private PrintWriter writer;
    private Formatter formatter;

    public void stringFormat(HttpServletRequest request, Locale lang) {
        String fmt = request.getParameter("fmt");
        // Locale 을 첫 인자로 받는 형태: Locale 타입 변수(이름에 locale 이 없어도 타입으로 안다), 상수, 요청의 Locale
        // ruleid: mois-1-17-format-string
        String.format(lang, fmt, "value");
        // ruleid: mois-1-17-format-string
        String.format(Locale.KOREA, fmt, "value");
        // ruleid: mois-1-17-format-string
        String.format(request.getLocale(), fmt, "value");
        // ruleid: mois-1-17-format-string
        fmt.formatted("value");
        // ruleid: mois-1-17-format-string
        ("결과: " + fmt).formatted("value");
    }

    public void printStreams(HttpServletRequest request) {
        String fmt = request.getParameter("fmt");
        // ruleid: mois-1-17-format-string
        stream.printf(fmt, "value");
        // ruleid: mois-1-17-format-string
        stream.format(fmt, "value");
        // ruleid: mois-1-17-format-string
        writer.printf(fmt, "value");
        // ruleid: mois-1-17-format-string
        writer.format(fmt, "value");
        // ruleid: mois-1-17-format-string
        System.out.printf(fmt, "value");
        // ruleid: mois-1-17-format-string
        System.out.format(fmt, "value");
        // ruleid: mois-1-17-format-string
        System.err.printf(fmt, "value");
        // ruleid: mois-1-17-format-string
        System.err.format(fmt, "value");
    }

    public void responseWriter(HttpServletRequest request, javax.servlet.http.HttpServletResponse response,
            jakarta.servlet.http.HttpServletResponse jakartaResponse) throws IOException {
        String fmt = request.getParameter("fmt");
        // ruleid: mois-1-17-format-string
        response.getWriter().printf(fmt, "value");
        // ruleid: mois-1-17-format-string
        response.getWriter().format(fmt, "value");
        // ruleid: mois-1-17-format-string
        jakartaResponse.getWriter().printf(fmt, "value");
        // ruleid: mois-1-17-format-string
        jakartaResponse.getWriter().format(fmt, "value");
    }

    public void formatterAndMessageFormat(HttpServletRequest request) {
        String fmt = request.getParameter("fmt");
        // ruleid: mois-1-17-format-string
        formatter.format(fmt, "value");
        // ruleid: mois-1-17-format-string
        new Formatter().format(fmt, "value");
        // ruleid: mois-1-17-format-string
        MessageFormat.format(fmt, "value");
        // ruleid: mois-1-17-format-string
        new MessageFormat(fmt);
    }
}

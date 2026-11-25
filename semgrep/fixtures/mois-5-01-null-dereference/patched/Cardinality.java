package demo;

import java.util.Collection;
import java.util.Iterator;
import java.util.Objects;
import javax.servlet.http.HttpServletRequest;

// 탐지되면 안 되는 경우 (진단가이드 5-1 안전한 코드와 오탐 예)
public class Cardinality {

    // ok: mois-5-01-null-dereference — obj 가 null 이 아닌 경우에만 obj.equals 를 실행 (진단가이드 안전한 코드)
    public static int cardinality(Object obj, final Collection<?> col) {
        int count = 0;
        if (col == null) {
            return count;
        }
        Iterator<?> it = col.iterator();
        while (it.hasNext()) {
            Object elt = it.next();
            if ((null == obj && null == elt) || (null != obj && obj.equals(elt))) {
                count++;
            }
        }
        return count;
    }

    // ok: mois-5-01-null-dereference — null 을 오른쪽에 쓴 형태도 같다
    public static boolean same(Object obj, Object elt) {
        return (obj == null && elt == null) || (obj != null && obj.equals(elt));
    }

    // ok: mois-5-01-null-dereference — null 인 분기 안이지만 사용하기 전에 새 값을 대입한다
    public int sizeOrEmpty(Collection<?> items) {
        if (items == null) {
            items = java.util.List.of();
            return items.size();
        }
        return items.size();
    }

    // ok: mois-5-01-null-dereference — null 검사가 && 의 왼쪽에서 먼저 평가된다
    public boolean isBlankUrl(HttpServletRequest request) {
        String url = request.getParameter("url");
        return url != null && url.isEmpty();
    }

    // ok: mois-5-01-null-dereference — null 이면 return 한 뒤 사용
    public String command() {
        String cmd = System.getProperty("cmd");
        if (cmd == null) {
            return "";
        }
        return cmd.trim();
    }

    // ok: mois-5-01-null-dereference — 앞의 null 검사가 참이면 뒤 조건은 평가하지 않는다 (오탐 예)
    public boolean isEmpty(String str) {
        return str == null || str.length() == 0;
    }

    // ok: mois-5-01-null-dereference — null 이면 빈 목록으로 바꾼 새 변수를 사용
    public int size(Collection<?> items) {
        Collection<?> safe = Objects.requireNonNullElse(items, java.util.List.of());
        return safe.size();
    }
}

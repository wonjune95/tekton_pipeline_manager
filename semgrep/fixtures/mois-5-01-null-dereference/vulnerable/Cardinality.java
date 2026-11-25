package demo;

import java.util.Collection;
import java.util.Iterator;
import javax.servlet.http.HttpServletRequest;

// 탐지돼야 하는 경우 (진단가이드 5-1: null 검사 순서 오류, 검사 없는 사용, null 분기 안에서 사용)
public class Cardinality {

    // obj 가 null 이고 elt 가 null 이 아니면 obj.equals 에서 역참조
    public static int cardinality(Object obj, final Collection<?> col) {
        int count = 0;
        if (col == null) {
            return count;
        }
        Iterator<?> it = col.iterator();
        while (it.hasNext()) {
            Object elt = it.next();
            // ruleid: mois-5-01-null-dereference
            if ((null == obj && null == elt) || obj.equals(elt)) {
                count++;
            }
        }
        return count;
    }

    public static boolean same(Object obj, Object elt) {
        // ruleid: mois-5-01-null-dereference
        return (obj == null && elt == null) || obj.equals(elt);
    }

    // 요청 파라미터는 없으면 null 이다
    public boolean isBlankUrl(HttpServletRequest request) {
        String url = request.getParameter("url");
        // ruleid: mois-5-01-null-dereference
        return url.equals("");
    }

    // 시스템 속성도 없으면 null 이다 (일반적인 진단의 예)
    public String command() {
        String cmd = System.getProperty("cmd");
        // ruleid: mois-5-01-null-dereference
        return cmd.trim();
    }

    // ── 조건식 안에서 null 검사보다 사용이 먼저이거나, null 일 때 사용 (null 을 왼쪽에 쓴 형태 포함) ──

    // null 검사보다 사용이 먼저다 (정탐 예)
    public boolean isEmpty(String str) {
        // ruleid: mois-5-01-null-dereference
        return str.length() == 0 || str == null;
    }

    public boolean isEmptyYoda(String str) {
        // ruleid: mois-5-01-null-dereference
        return str.isEmpty() || null == str;
    }

    public boolean hasText(String str) {
        // ruleid: mois-5-01-null-dereference
        return str.length() > 0 && str != null;
    }

    public boolean hasTextYoda(String str) {
        // ruleid: mois-5-01-null-dereference
        return str.length() > 0 && null != str;
    }

    // && 를 || 로 잘못 쓴 경우: null 일 때 오른쪽이 평가된다
    public boolean nullAndUse(String str) {
        // ruleid: mois-5-01-null-dereference
        return str == null && str.isEmpty();
    }

    public boolean nullAndUseYoda(String str) {
        // ruleid: mois-5-01-null-dereference
        return null == str && str.isEmpty();
    }

    public boolean notNullOrUse(String str) {
        // ruleid: mois-5-01-null-dereference
        return str != null || str.isEmpty();
    }

    public boolean notNullOrUseYoda(String str) {
        // ruleid: mois-5-01-null-dereference
        return null != str || str.isEmpty();
    }

    // ── null 로 확인된 분기 안에서 사용 (탐지 위치는 역참조하는 줄) ──

    public int size(Collection<?> items) {
        if (items == null) {
            // ruleid: mois-5-01-null-dereference
            return items.size();
        }
        return 0;
    }

    public int sizeYoda(Collection<?> items) {
        if (null == items) {
            // ruleid: mois-5-01-null-dereference
            items.clear();
        } else {
            return items.size();
        }
        return 0;
    }

    // != null 의 else 쪽은 null 인 분기다
    public int sizeElse(Collection<?> items) {
        if (items != null) {
            return items.size();
        } else {
            // ruleid: mois-5-01-null-dereference
            return items.hashCode();
        }
    }

    public int sizeElseYoda(Collection<?> items) {
        if (null != items) {
            return items.size();
        } else {
            // ruleid: mois-5-01-null-dereference
            return items.hashCode();
        }
    }
}

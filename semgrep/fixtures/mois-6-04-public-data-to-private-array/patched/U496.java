package demo;

import java.util.Arrays;

// 탐지되면 안 되는 경우 (진단가이드 6-4 안전한 코드: 인자 배열의 복사본을 저장)
public class U496 {
    private String[] userRoles;
    private int[] limits;
    private byte[] secret = new byte[0];

    public U496(String[] userRoles) {
        // ok: mois-6-04-public-data-to-private-array — 생성자에서도 복사본을 저장
        this.userRoles = userRoles.clone();
    }

    public void setUserRoles(String[] userRoles) {
        // ok: mois-6-04-public-data-to-private-array — 새 배열에 원소를 옮겨 담는다
        this.userRoles = new String[userRoles.length];
        for (int i = 0; i < userRoles.length; ++i) {
            this.userRoles[i] = userRoles[i];
        }
    }

    public void configure(int[] values) {
        // ok: mois-6-04-public-data-to-private-array — clone·Arrays.copyOf 로 만든 복사본
        limits = values.clone();
    }

    public void rotate(byte[] next) {
        secret = Arrays.copyOf(next, next.length);
    }

    // ok: mois-6-04-public-data-to-private-array — public 이 아닌 메서드는 같은 클래스·패키지 안에서만 부른다
    void adopt(int[] values) {
        limits = values;
    }

    private void adoptRoles(String[] roles) {
        this.userRoles = roles;
    }

    public int roleCount() {
        return userRoles.length + limits.length + secret.length;
    }
}

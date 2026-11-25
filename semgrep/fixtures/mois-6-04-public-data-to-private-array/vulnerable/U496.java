package demo;

// 탐지돼야 하는 경우 (진단가이드 6-4: public 메서드의 배열 인자를 private 배열에 그대로 저장)
public class U496 {
    private String[] userRoles;
    private int[] limits;
    private byte[] secret = new byte[0];
    private String[] tags;

    // public 생성자도 같다
    public U496(String[] tags) {
        // ruleid: mois-6-04-public-data-to-private-array
        this.tags = tags;
    }

    public void setUserRoles(String[] userRoles) {
        // ruleid: mois-6-04-public-data-to-private-array
        this.userRoles = userRoles;
    }

    public void configure(int[] values) {
        // ruleid: mois-6-04-public-data-to-private-array
        limits = values;
    }

    // 초기값이 있는 필드, 인자가 여러 개인 메서드
    public void rotate(String reason, byte[] next) {
        // ruleid: mois-6-04-public-data-to-private-array
        secret = next;
    }

    // 복사본을 만들었지만 저장한 것은 인자 그대로다
    public void copyButStoreArgument(int[] values) {
        int[] copy = values.clone();
        copy[0] = 0;
        // ruleid: mois-6-04-public-data-to-private-array
        this.limits = values;
    }

    public int roleCount() {
        return userRoles.length + limits.length + secret.length + tags.length;
    }
}

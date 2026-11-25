from rest_framework import serializers


class OrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    memo = serializers.CharField(max_length=200)

    def validate_memo(self, value):
        # ruleid: mois-6-02-debug-code-py
        print("memo:", value)
        return value.strip()


# DRF 모듈에 남은 확인용 블록
# ruleid: mois-6-02-debug-code-py
if __name__ == "__main__":
    serializer = OrderSerializer(data={"order_id": 1, "memo": " x "})
    assert serializer.is_valid()

class RoleRegistry:
    def __init__(self):
        self.__roles = ["viewer"]
        self._grants = {}

    def get_roles(self):
        # 비공개 list 의 참조를 그대로 반환: 호출자가 append 로 권한을 추가할 수 있음
        # ruleid: mois-6-03-private-array-returned-py
        return self.__roles

    @property
    def grants(self):
        # ruleid: mois-6-03-private-array-returned-py
        return self._grants  # 비공개 dict 를 그대로 반환

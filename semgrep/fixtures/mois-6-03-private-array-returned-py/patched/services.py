class RoleRegistry:
    def __init__(self, owner):
        self.__roles = ["viewer"]
        self._grants = {}
        self._owner = owner

    def get_roles(self):
        # 복사본을 반환
        return list(self.__roles)

    @property
    def grants(self):
        return dict(self._grants)

    @property
    def owner(self):
        return self._owner

    def _raw_roles(self):
        return self.__roles

from ..enums import ScopesIntEnum


def get_scopes_from_scopes_sum(scopes_sum: int) -> list[str]:
    scopes = []
    for pow in range(4, 0, -1):
        if not (scopes_sum - (2 ** pow) < 0):
            scope_value = 2 ** pow
            scopes.append(ScopesIntEnum(scope_value).name)
            scopes_sum -= scope_value
    return scopes


def get_scopes_sum_from_scopes(scopes: list[str]) -> int:
    sum = 0
    for scope in scopes:
        scope_int_value = ScopesIntEnum._member_map_[scope].value
        sum += scope_int_value
    return sum

    


from ..enums import ScopesEnum


def get_scopes_from_scopes_sum(scopes_sum: int) -> list[str]:
    scopes = []
    for pow in range(3, 0, -1):
        if scopes_sum - 2 ** pow < 0:
            continue
        scope_value = scopes_sum - 2 ** pow
        scopes.append(ScopesEnum(scope_value).value)
    return scopes
